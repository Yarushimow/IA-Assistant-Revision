"""Étape 2 : embeddings + recherche sémantique."""
import sys

from sentence_transformers import SentenceTransformer

from load import load_fiches, chunk_fiche

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"  # petit modèle qui comprend le français

# On charge le modèle UNE seule fois, au lancement du fichier
model = SentenceTransformer(MODEL_NAME)


def build_index(chunks: list[dict]):
    """Encode chaque passage (titre de section + texte) en un vecteur.

    Renvoie une matrice numpy (nb_passages x 384).
    """
    textes = []
    for passage in chunks:
        texte_complet = passage["section"] + " : " + passage["text"]     # le titre de la section, puis le texte
        textes.append(texte_complet)
    embeddings = model.encode(textes, normalize_embeddings=True, show_progress_bar=True)
    return embeddings


def search(question: str, chunks: list[dict], embeddings, top_k: int = 3) -> list[tuple[float, dict]]:
    """TODO (séance de demain) : encoder la question, calculer la similarité cosinus
    avec tous les passages, et renvoyer les top_k meilleurs sous forme [(score, passage), ...].
    """
    raise NotImplementedError


if __name__ == "__main__":
    # 1. Charger les fiches
    fiches = load_fiches()

    # 2. Découper chaque fiche et tout mettre dans UNE seule liste de passages
    chunks = []
    for fiche in fiches:
        chunks.extend(chunk_fiche(fiche))     # ajouter PLUSIEURS éléments d'un coup à une liste

    # 3. Construire l'index
    embeddings = build_index(chunks)
    print(len(chunks), "passages")
    print("Index :", embeddings.shape)