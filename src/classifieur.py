"""v3 : classifieur de matière (TF-IDF + régression logistique). Étape 1 : préparer les données."""
import json
from pathlib import Path

from load import load_fiches, chunk_fiche

QUESTIONS_PATH = Path(__file__).parent.parent / "data" / "questions_test.json"


def code_matiere(nom_fichier: str) -> str:
    """'TE302_systemes_numeriques.md' → 'TE302' (tout ce qui est avant le premier _)."""
    return nom_fichier.split("_")[0]


def preparer_entrainement() -> tuple[list[str], list[str]]:
    """Données d'entraînement : chaque passage de fiche, étiqueté par le code de sa fiche."""
    textes = []
    etiquettes = []
    for fiche in load_fiches():
        for passage in chunk_fiche(fiche):
            textes.append(passage["section"] + " : " + passage["text"])
            etiquettes.append(code_matiere(passage["source"]))
    return textes, etiquettes


def preparer_test() -> tuple[list[str], list[str]]:
    """Données de test : les 40 questions de la v2, étiquetées par leur fiche."""
    with open(QUESTIONS_PATH, encoding="utf-8") as fichier:
        questions = json.load(fichier)
    textes = []
    etiquettes = []
    for q in questions:
        textes.append(q["question"])
        etiquettes.append(q["fiche"])
    return textes, etiquettes


def compter(etiquettes: list[str]) -> dict:
    """Combien d'exemples par matière."""
    compte = {}
    for e in etiquettes:
        compte[e] = compte.get(e, 0) + 1
    return compte


if __name__ == "__main__":
    X_train, y_train = preparer_entrainement()
    X_test, y_test = preparer_test()

    print(f"Entraînement : {len(X_train)} passages")
    print(f"Test         : {len(X_test)} questions\n")

    print("Exemples par matière :")
    compte_train = compter(y_train)
    compte_test = compter(y_test)
    for matiere in sorted(compte_train):
        print(f"  {matiere}   entraînement : {compte_train[matiere]:3}   test : {compte_test.get(matiere, 0)}")

    print("\nUn exemple d'entraînement :")
    print("  y =", y_train[0])
    print("  X =", X_train[0][:150], "...")