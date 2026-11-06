"""v3 : classifieur de matière (TF-IDF + régression logistique)."""
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
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


# ---------- 3. Évaluer ----------

def afficher_matrice(y_vrai: list[str], y_predit: list[str], matieres: list[str]):
    """Matrice de confusion : lignes = vraie matière, colonnes = matière prédite."""
    matrice = confusion_matrix(y_vrai, y_predit, labels=matieres)
    print("vraie \\ prédite " + "".join(f"{m:>7}" for m in matieres))
    for i, ligne in enumerate(matrice):
        print(f"{matieres[i]:>15} " + "".join(f"{n:>7}" for n in ligne))


def expliquer(modele, question: str):
    """Pour chaque mot connu de la question : la matière pour laquelle il vote le plus, et son poids."""
    tfidf = modele[0]                           # 1re étape du pipeline : le TfidfVectorizer
    reglog = modele[1]                          # 2e étape : la régression logistique
    vocabulaire = tfidf.vocabulary_             # dictionnaire mot → numéro de colonne

    print(f"\n« {question} »  →  prédit : {modele.predict([question])[0]}")
    for mot in tfidf.build_analyzer()(question):          # découpe la question en mots, comme TF-IDF
        if mot not in vocabulaire:
            print(f"   {mot:15} (inconnu : jamais vu dans les fiches, ignoré)")
            continue
        colonne = vocabulaire[mot]
        poids_par_matiere = reglog.coef_[:, colonne]       # un poids par matière pour ce mot
        meilleure = poids_par_matiere.argmax()                # l'indice de la matière au plus grand poids
        print(f"   {mot:15} vote {reglog.classes_[meilleure]}  (poids {poids_par_matiere[meilleure]:+.2f})")


if __name__ == "__main__":
    X_train, y_train = preparer_entrainement()
    X_test, y_test = preparer_test()
    matieres = sorted(compter(y_train))

    # On garde le meilleur modèle de mercredi : l'équilibré
    modele = creer_modele(equilibre=True)
    modele.fit(X_train, y_train)
    predictions = modele.predict(X_test)
    print(f"Précision : {100 * accuracy_score(y_test, predictions):.0f} %\n")

    # 1. Matrice de confusion
    afficher_matrice(y_test, predictions, matieres)

    # 2. Les erreurs
    print("\nERREURS :")
    for question, vraie, predite in zip(X_test, y_test, predictions):
        if vraie != predite:
            print(f"  ❌ {vraie} prédit {predite} : {question}")

    # 3. Pourquoi « variance » part vers Linux ?
    expliquer(modele, "Comment calculer la variance ?")