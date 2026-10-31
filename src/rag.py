"""Étape 3 : RAG = recherche dans les fiches + génération avec un LLM local (Ollama)."""
import sys

import ollama

from load import load_fiches, chunk_fiche
from search import load_or_build_index, search

MODELE_LLM = "mistral"     # le modèle Ollama (téléchargé avec « ollama pull mistral »)

# Les règles du jeu : envoyées dans un message « system », séparé de la demande
CONSIGNES = """Tu es un assistant de révision pour un étudiant ingénieur.
Réponds à la question en utilisant UNIQUEMENT les extraits de fiches fournis.
- L'étudiant ne voit pas les extraits : recopie dans ta réponse les informations utiles qu'ils contiennent (tables, formules, commandes, définitions).
- Si les extraits ne contiennent pas la réponse, dis : « Je ne trouve pas la réponse dans tes fiches. »
- N'invente rien et n'ajoute aucune connaissance extérieure.
- À la fin, indique entre crochets les extraits utilisés, par exemple [Extrait 1].
- Réponds en français, de façon claire et concise."""


def construire_prompt(question: str, resultats: list[tuple[float, dict]]) -> str:
    """Assemble les extraits trouvés et la question (les consignes sont à part, dans CONSIGNES)."""
    # 1. Les extraits, chacun avec une étiquette « fiche › section »
    extraits = ""
    numero = 1
    for score, passage in resultats:
        extraits += f"[Extrait {numero} — {passage['source']} › {passage['section']}]\n"
        extraits += passage['text'] + "\n\n"                 # le texte du passage
        numero += 1

    # 2. La demande : extraits + question
    prompt = f"""EXTRAITS :
{extraits}

QUESTION : {question}
"""
    return prompt


def repondre(question: str, chunks: list[dict], embeddings) -> tuple[str, list]:
    """Pipeline RAG complet : chercher les passages, construire le prompt, faire répondre le LLM."""
    resultats = search(question, chunks, embeddings)          # R : Retrieval
    prompt = construire_prompt(question, resultats)            # A : Augmentation

    reponse = ollama.chat(                                     # G : Generation
        model=MODELE_LLM,
        messages=[
            {"role": "???", "content": CONSIGNES},             # les règles du jeu
            {"role": "user", "content": prompt},               # la demande
        ],
    )
    return reponse.message.content, resultats


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Qu'est-ce qu'une bascule JK ?"

    chunks = []
    for fiche in load_fiches():
        chunks.extend(chunk_fiche(fiche))
    embeddings = load_or_build_index(chunks)

    texte, resultats = repondre(question, chunks, embeddings)

    print("\nRÉPONSE :\n")
    print(texte)
    print("\nSOURCES :")
    for score, passage in resultats:
        print(f"  [{score:.2f}] {passage['source']} › {passage['section']}")