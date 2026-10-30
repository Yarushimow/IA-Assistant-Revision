"""Étape 2 : embeddings + recherche sémantique."""
import hashlib
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from load import load_fiches, chunk_fiche

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"  # 6/10 au mini-test
# Ancien : "paraphrase-multilingual-MiniLM-L12-v2" → 5/10

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_PATH = DATA_DIR / "index.npy"                  # les vecteurs
EMPREINTE_PATH = DATA_DIR / "index_empreinte.txt"    # l'empreinte des textes qui ont servi à les calculer

# On charge le modèle UNE seule fois, au lancement du fichier
model = SentenceTransformer(MODEL_NAME)


def texte_a_encoder(passage: dict) -> str:
    """Le texte réellement encodé pour un passage : titre de section + texte."""
    return passage["section"] + " : " + passage["text"]


def build_index(chunks: list[dict]):
    """Encode chaque passage en un vecteur. Renvoie une matrice (nb_passages x dimension du modèle)."""
    textes = []
    for passage in chunks:
        textes.append(texte_a_encoder(passage))
    embeddings = model.encode(textes, normalize_embeddings=True, show_progress_bar=True)
    return embeddings


def calculer_empreinte(chunks: list[dict]) -> str:
    """Empreinte SHA-256 du nom du modèle + de tous les textes encodés."""
    h = hashlib.sha256()
    h.update(MODEL_NAME.encode("utf-8"))           # on « nourrit » le hash avec des octets
    for passage in chunks:
        h.update(texte_a_encoder(passage).encode("utf-8"))     # le texte réellement encodé de chaque passage
    return h.hexdigest()                            # l'empreinte sous forme de texte


def load_or_build_index(chunks: list[dict]):
    """Recharge l'index si l'empreinte n'a pas changé, sinon le reconstruit et le sauvegarde."""
    empreinte = calculer_empreinte(chunks)

    if INDEX_PATH.exists() and EMPREINTE_PATH.exists():
        ancienne = EMPREINTE_PATH.read_text(encoding="utf-8")
        if empreinte == ancienne:                              # rien n'a changé ?
            print("Index chargé depuis le disque")
            return np.load(INDEX_PATH)
        print("Index périmé (fiches ou modèle modifiés) : on le reconstruit")

    embeddings = build_index(chunks)
    np.save(INDEX_PATH, embeddings)
    EMPREINTE_PATH.write_text(empreinte, encoding="utf-8")   # on sauvegarde l'empreinte avec l'index
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

    # 3. Charger l'index (ou le construire s'il est absent ou périmé)
    embeddings = load_or_build_index(chunks)

    # 4. Chercher et afficher
    print("\nQuestion :", question, "\n")
    for score, passage in search(question, chunks, embeddings):
        print(f"[{score:.2f}] {passage['source']} › {passage['section']}")
        print(passage["text"][:200], "...\n")