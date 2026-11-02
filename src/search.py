"""Étape 2 : embeddings + recherche sémantique."""
import hashlib
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from load import load_fiches, chunk_fiche

# Modèle conçu pour la recherche (question courte → passage long). Il attend des préfixes.
MODEL_NAME = "intfloat/multilingual-e5-base"
PREFIXE_QUESTION = "query: "
PREFIXE_PASSAGE = "passage: "
# Historique : MiniLM → 5/10 (mini-test) ; MPNet (sans préfixes) → 75 % de recall@3 (jeu de test)

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_PATH = DATA_DIR / "index.npy"                  # les vecteurs
EMPREINTE_PATH = DATA_DIR / "index_empreinte.txt"    # l'empreinte des textes qui ont servi à les calculer

# On charge le modèle UNE seule fois, au lancement du fichier
model = SentenceTransformer(MODEL_NAME)


def texte_a_encoder(passage: dict) -> str:
    """Le texte réellement encodé pour un passage : préfixe + titre de section + texte."""
    return PREFIXE_PASSAGE + passage["section"] + " : " + passage["text"]


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
    h.update(MODEL_NAME.encode("utf-8"))
    for passage in chunks:
        h.update(texte_a_encoder(passage).encode("utf-8"))
    return h.hexdigest()


def load_or_build_index(chunks: list[dict]):
    """Recharge l'index si l'empreinte n'a pas changé, sinon le reconstruit et le sauvegarde."""
    empreinte = calculer_empreinte(chunks)

    if INDEX_PATH.exists() and EMPREINTE_PATH.exists():
        ancienne = EMPREINTE_PATH.read_text(encoding="utf-8")
        if empreinte == ancienne:
            print("Index chargé depuis le disque")
            return np.load(INDEX_PATH)
        print("Index périmé (fiches ou modèle modifiés) : on le reconstruit")

    embeddings = build_index(chunks)
    np.save(INDEX_PATH, embeddings)
    EMPREINTE_PATH.write_text(empreinte, encoding="utf-8")
    print("Index construit et sauvegardé")
    return embeddings


def search(question: str, chunks: list[dict], embeddings, top_k: int = 3,
           une_par_section: bool = True) -> list[tuple[float, dict]]:
    """Renvoie les top_k passages les plus proches de la question : [(score, passage), ...].

    Si une_par_section est vrai, une section ne peut occuper qu'une seule place dans le résultat.
    """
    q = model.encode(PREFIXE_QUESTION + question, normalize_embeddings=True)
    scores = embeddings @ q

    ordre = np.argsort(scores)[::-1]           # TOUS les passages, du meilleur au moins bon
    resultats = []
    sections_vues = set()                       # les (fiche, section) qui ont déjà une place

    for i in ordre:
        passage = chunks[i]
        cle = (passage["source"], passage["section"])
        if une_par_section and cle in sections_vues:     # section déjà prise → on saute ce passage
            continue
        sections_vues.add(cle)                           # on retient cette section
        resultats.append((float(scores[i]), passage))
        if len(resultats) == top_k:                      # on a assez de passages : on s'arrête
            break
    return resultats


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Qu'est-ce qu'une bascule JK ?"

    chunks = []
    for fiche in load_fiches():
        chunks.extend(chunk_fiche(fiche))
    embeddings = load_or_build_index(chunks)

    print("\nQuestion :", question, "\n")
    for score, passage in search(question, chunks, embeddings):
        print(f"[{score:.2f}] {passage['source']} › {passage['section']}")
        print(passage["text"][:200], "...\n")