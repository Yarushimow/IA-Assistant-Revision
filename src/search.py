"""Étape 2 : embeddings + recherche sémantique."""
import sys

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"  # petit modèle qui comprend le français


def build_index(chunks: list[dict]):
    """TODO : encoder le texte de chaque passage avec SentenceTransformer(MODEL_NAME).

    Renvoie une matrice numpy (nb_passages x dimension).
    Astuce : normalize_embeddings=True simplifie le calcul de similarité.
    """
    raise NotImplementedError


def search(question: str, chunks: list[dict], embeddings, top_k: int = 3) -> list[tuple[float, dict]]:
    """TODO : encoder la question, calculer la similarité cosinus avec tous les passages,
    et renvoyer les top_k meilleurs sous forme [(score, passage), ...].
    """
    raise NotImplementedError


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Qu'est-ce qu'une bascule JK ?"
    # TODO : charger les fiches, les découper, construire l'index, chercher, afficher
    #        chaque résultat avec son score, sa source et sa section.
