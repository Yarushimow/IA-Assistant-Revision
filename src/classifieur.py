"""v3 : classifieur de matière (TF-IDF + régression logistique)."""
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline

from load import load_fiches, chunk_fiche

QUESTIONS_PATH = Path(__file__).parent.parent / "data" / "questions_test.json"


# ---------- 1. Préparer les données ----------

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


# ---------- 2. Entraîner ----------

def creer_modele(equilibre: bool):
    """TF-IDF puis régression logistique, enchaînés dans un pipeline."""
    poids = "balanced" if equilibre else None      # "balanced" : plus de poids aux matières rares
    return make_pipeline(
        TfidfVectorizer(),                          # texte → vecteur TF-IDF (une case par mot)
        LogisticRegression(max_iter=1000, class_weight=poids),
    )


if __name__ == "__main__":
    X_train, y_train = preparer_entrainement()
    X_test, y_test = preparer_test()
    print(f"Entraînement : {len(X_train)} passages   |   Test : {len(X_test)} questions\n")

    # Références naïves
    nb_matieres = len(compter(y_train))
    print(f"Référence « au hasard »                 : {100 / nb_matieres:.0f} %")
    plus_frequente = max(compter(y_train), key=compter(y_train).get)
    toujours_meme = [plus_frequente] * len(y_test)
    print(f"Référence « toujours {plus_frequente} »            : {100 * accuracy_score(y_test, toujours_meme):.0f} %\n")

    # Les deux modèles
    for nom, equilibre in [("Normal", False), ("Équilibré", True)]:
        modele = creer_modele(equilibre)
        modele.fit(X_train, y_train)                # ENTRAÎNER sur les passages
        predictions = modele.predict(X_test)            # PRÉDIRE sur les questions jamais vues
        precision = accuracy_score(y_test, predictions)
        print(f"{nom:10} : précision = {100 * precision:.0f} %  ({sum(p == v for p, v in zip(predictions, y_test))}/{len(y_test)})")

    # Le modèle équilibré sur 3 questions, avec ses probabilités
    print("\nExemples (modèle équilibré) :")
    for question in ["Qu'est-ce qu'une bascule JK ?",
                     "Comment calculer la variance ?",
                     "Comment arrêter un processus avec un signal ?"]:
        probas = modele.predict_proba([question])[0]          # une probabilité par matière
        meilleure = probas.argmax()
        print(f"  {question:50} → {modele.classes_[meilleure]} ({100 * probas[meilleure]:.0f} %)")