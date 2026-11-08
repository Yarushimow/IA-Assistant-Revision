"""v4 : l'API web de l'assistant de révision."""
from fastapi import FastAPI, HTTPException

from load import load_fiches, chunk_fiche
from search import load_or_build_index
from rag import repondre, GeminiIndisponible

app = FastAPI(title="Assistant de révision IA")

# ---------- Chargé UNE seule fois, au démarrage du serveur ----------
chunks = []
for fiche in load_fiches():
    chunks.extend(chunk_fiche(fiche))
embeddings = load_or_build_index(chunks)

FOURNISSEURS = ["gemini", "ollama"]


@app.get("/")
def accueil():
    """Route d'accueil : vérifie que l'API répond, et combien de passages sont chargés."""
    return {"message": "L'assistant de révision est en ligne", "passages": len(chunks)}


@app.get("/question")
def question(q: str, fournisseur: str = "gemini"):
    """Pose une question à l'assistant. Exemple : /question?q=Qu'est-ce qu'une bascule JK ?"""
    # 1. Vérifier la demande : sinon, erreur 400 (la faute vient du client)
    if fournisseur not in FOURNISSEURS:
        raise HTTPException(status_code=400, detail=f"Fournisseur inconnu : {fournisseur} (choix : {FOURNISSEURS})")

    # 2. Faire tourner le RAG ; si aucun modèle Gemini ne répond, erreur 503 au lieu d'un plantage
    try:
        texte, resultats = repondre(q, chunks, embeddings, fournisseur)
    except GeminiIndisponible:
        raise HTTPException(status_code=503, detail="L'assistant est surchargé, réessaie dans quelques instants.")

    # 3. Mettre les sources sous une forme simple pour le site
    sources = []
    for score, passage in resultats:
        sources.append({
            "fiche": passage["source"],
            "section": passage["section"],
            "score": round(score, 2),
        })

    return {"question": q, "fournisseur": fournisseur, "reponse": texte, "sources": sources}