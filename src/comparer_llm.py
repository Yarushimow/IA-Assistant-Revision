"""Compare les réponses du RAG avec Ollama (local) et Gemini (en ligne) sur quelques questions."""
from load import load_fiches, chunk_fiche
from search import load_or_build_index
from rag import repondre

QUESTIONS = [
    "Comment retrouver la probabilité d'une cause quand on connaît l'effet observé ?",   # Bayes : la recherche trouve
    "Comment on enlève des droits par défaut à la création d'un fichier sous Linux ?",  # umask : la recherche rate
    "Quelles sont les 7 couches du modèle OSI ?",                                        # absent de mes fiches
]
FOURNISSEURS = ["ollama", "gemini"]

chunks = []
for fiche in load_fiches():
    chunks.extend(chunk_fiche(fiche))
embeddings = load_or_build_index(chunks)

for question in QUESTIONS:
    print("\n" + "#" * 70)
    print("QUESTION :", question)
    for fournisseur in FOURNISSEURS:                            # on pose la question à chaque modèle
        texte, resultats = repondre(question, chunks, embeddings, fournisseur)
        print(f"\n--- {fournisseur} ---\n")
        print(texte)