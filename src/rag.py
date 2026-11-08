"""Étape 3 : RAG = recherche dans les fiches + génération avec un LLM (Ollama en local, ou Gemini en ligne)."""
import os
import sys

import ollama
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from load import load_fiches, chunk_fiche
from search import load_or_build_index, search

load_dotenv()                                  # lit le fichier .env (clé Gemini)

MODELE_OLLAMA = "mistral"                      # local, téléchargé avec « ollama pull mistral »
# En ligne, du préféré au dernier recours, TESTÉS le 8 nov. avec diagnostic_gemini.py
# (3.8 retiré : 503 et 504 à répétition ; 2.5 retiré par Google : 404 pour les nouveaux comptes)
MODELES_GEMINI = ["gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]

# Les règles du jeu : envoyées comme consignes « system », séparées de la demande
CONSIGNES = """Tu es un assistant de révision pour un étudiant ingénieur.
Réponds à la question en utilisant UNIQUEMENT les extraits de fiches fournis.
- L'étudiant ne voit pas les extraits : recopie dans ta réponse les informations utiles qu'ils contiennent (tables, formules, commandes, définitions).
- Si les extraits ne contiennent pas la réponse, dis : « Je ne trouve pas la réponse dans tes fiches. »
- N'invente rien et n'ajoute aucune connaissance extérieure.
- À la fin, indique entre crochets les extraits utilisés, par exemple [Extrait 1].
- Réponds en français, de façon claire et concise."""


class GeminiIndisponible(Exception):
    """Notre propre erreur : aucun modèle Gemini n'a pu répondre."""
    pass


def construire_prompt(question: str, resultats: list[tuple[float, dict]]) -> str:
    """Assemble les extraits trouvés et la question (les consignes sont à part, dans CONSIGNES)."""
    extraits = ""
    numero = 1
    for score, passage in resultats:
        extraits += f"[Extrait {numero} — {passage['source']} › {passage['section']}]\n"
        extraits += passage['text'] + "\n\n"
        numero += 1

    prompt = f"""EXTRAITS :
{extraits}

QUESTION : {question}
"""
    return prompt


def generer_gemini(consignes: str, prompt: str) -> str:
    """Essaie chaque modèle Gemini dans l'ordre ; passe au suivant s'il est surchargé, retiré ou à court de quota."""
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        http_options=types.HttpOptions(
            timeout=30_000,                                       # 30 s maximum par appel : jamais d'attente infinie
            retry_options=types.HttpRetryOptions(attempts=2),     # 2 essais par modèle, puis on passe au suivant
        ),
    )
    for modele in MODELES_GEMINI:
        try:
            reponse = client.models.generate_content(
                model=modele,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=consignes),
            )
            return reponse.text                                   # ça a marché : on sort tout de suite
        except errors.APIError as e:
            # 404 = modèle retiré, 429 = quota atteint, 5xx = surcharge : un autre modèle peut marcher
            if e.code in (404, 429) or e.code >= 500:
                print(f"  ({modele} : erreur {e.code}, on essaie le modèle suivant)")
            else:
                raise                                             # ex. clé invalide : inutile de changer de modèle
        except Exception as e:
            # Autres problèmes réseau, par exemple la limite de 30 s dépassée
            print(f"  ({modele} : {type(e).__name__}, on essaie le modèle suivant)")
    raise GeminiIndisponible("Aucun modèle Gemini n'a pu répondre")   # tous ont échoué


def generer(consignes: str, prompt: str, fournisseur: str) -> str:
    """Envoie les consignes et le prompt au LLM choisi, et renvoie sa réponse (texte)."""
    if fournisseur == "ollama":
        reponse = ollama.chat(
            model=MODELE_OLLAMA,
            messages=[
                {"role": "system", "content": consignes},
                {"role": "user", "content": prompt},
            ],
        )
        return reponse.message.content

    elif fournisseur == "gemini":
        return generer_gemini(consignes, prompt)

    else:
        raise ValueError(f"Fournisseur inconnu : {fournisseur}")


def repondre(question: str, chunks: list[dict], embeddings, fournisseur: str = "ollama") -> tuple[str, list]:
    """Pipeline RAG complet : chercher les passages, construire le prompt, faire répondre le LLM."""
    resultats = search(question, chunks, embeddings)          # R : Retrieval
    prompt = construire_prompt(question, resultats)            # A : Augmentation
    texte = generer(CONSIGNES, prompt, fournisseur)            # G : Generation
    return texte, resultats


if __name__ == "__main__":
    # On lit les arguments : « --gemini » choisit le modèle, le reste forme la question
    arguments = sys.argv[1:]
    fournisseur = "ollama"
    if "--gemini" in arguments:
        fournisseur = "gemini"
        arguments.remove("--gemini")
    question = " ".join(arguments) or "Qu'est-ce qu'une bascule JK ?"

    chunks = []
    for fiche in load_fiches():
        chunks.extend(chunk_fiche(fiche))
    embeddings = load_or_build_index(chunks)

    texte, resultats = repondre(question, chunks, embeddings, fournisseur)

    print(f"\nRÉPONSE ({fournisseur}) :\n")
    print(texte)
    print("\nSOURCES :")
    for score, passage in resultats:
        print(f"  [{score:.2f}] {passage['source']} › {passage['section']}")