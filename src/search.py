"""Étape 2 : embeddings + recherche sémantique."""
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from load import load_fiches, chunk_fiche

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"  # 6/10 au mini-test
# Ancien : "paraphrase-multilingual-MiniLM-L12-v2" → 5/10

INDEX_PATH = Path(__file__).parent.parent / "data" / "index.npy"   # où on sauvegarde l'index

# On charge le modèle UNE seule fois, au lancement du fichier
model = SentenceTransformer(MODEL_NAME)


def build_index(chunks: list[dict]):
    """Encode chaque passage (titre de section + texte) en un vecteur.

    Renvoie une matrice numpy (nb_passages x dimension du modèle).
    """
    textes = []
    for passage in chunks:
        texte_complet = passage["section"] + " : " + passage["text"]     # le titre de la section, puis le texte
        textes.append(texte_complet)
    embeddings = model.encode(textes, normalize_embeddings=True, show_progress_bar=True)
    return embeddings


def load_or_build_index(chunks: list[dict]):
    """Recharge l'index depuis le disque s'il est à jour, sinon le reconstruit et le sauvegarde."""
    if INDEX_PATH.exists():                               # le fichier existe-t-il ?
        embeddings = np.load(INDEX_PATH)
        if embeddings.shape[0] == len(chunks):                  # autant de lignes que de passages ?
            print("Index chargé depuis le disque")
            return embeddings
        print("Index périmé (les fiches ont changé) : on le reconstruit")

    embeddings = build_index(chunks)
    np.save(INDEX_PATH, embeddings)                                   # on sauvegarde pour la prochaine fois
    print("Index construit et sauvegardé")
    return embeddings


def search(question: str, chunks: list[dict], embeddings, top_k: int = 3) -> list[tuple[float, dict]]:
    """Renvoie les top_k passages les plus proches de la question : [(score, passage), ...]."""
    # 1. Encoder la question (même modèle, normalisée aussi)
    q = model.encode(question, normalize_embeddings=True)

    # 2. Un score par passage
    scores = embeddings @ q

    # 3. Les indices des top_k meilleurs scores, du plus grand au plus petit
    meilleurs = np.argsort(scores)[::-1][:top_k]

    resultats = []
    for i in meilleurs:
        resultats.append((float(scores[i]), chunks[i]))
    return resultats


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Qu'est-ce qu'une bascule JK ?"

    # 1. Charger les fiches
    fiches = load_fiches()

    # 2. Découper chaque fiche et tout mettre dans UNE seule liste de passages
    chunks = []
    for fiche in fiches:
        chunks.extend(chunk_fiche(fiche))     # ajouter PLUSIEURS éléments d'un coup à une liste

    # 3. Charger l'index (ou le construire la première fois)
    embeddings = load_or_build_index(chunks)

    # 4. Chercher et afficher
    print("\nQuestion :", question, "\n")
    for score, passage in search(question, chunks, embeddings):
        print(f"[{score:.2f}] {passage['source']} › {passage['section']}")
        print(passage["text"][:200], "...\n")