"""v3 : classifieur de matière (TF-IDF ou embeddings e5 + régression logistique)."""
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.pipeline import make_pipeline

from load import load_fiches, chunk_fiche

QUESTIONS_PATH = Path(__file__).parent.parent / "data" / "questions_test.json"

# Mots vides français : fréquents partout, ils ne disent rien sur la matière
MOTS_VIDES = [
    "le", "la", "les", "un", "une", "des", "de", "du", "au", "aux", "et", "ou", "en", "dans",
    "sur", "par", "pour", "avec", "sans", "que", "qu", "qui", "quoi", "ce", "ces", "cette",
    "est", "sont", "il", "elle", "on", "se", "sa", "son", "ses", "ne", "pas", "plus",
    "comment", "pourquoi", "quand", "quel", "quelle", "quels", "quelles", "faut", "peut",
]


# ---------- 1. Préparer les données ----------

def code_matiere(nom_fichier: str) -> str:
    """'TE302_systemes_numeriques.md' → 'TE302' (tout ce qui est avant le premier _)."""
    return nom_fichier.split("_")[0]


def charger_passages() -> list[dict]:
    """Les passages des fiches, dans le même ordre que l'index de search.py."""
    chunks = []
    for fiche in load_fiches():
        chunks.extend(chunk_fiche(fiche))
    return chunks


def preparer_entrainement(chunks: list[dict]) -> tuple[list[str], list[str]]:
    """Données d'entraînement : chaque passage de fiche, étiqueté par le code de sa fiche."""
    textes = []
    etiquettes = []
    for passage in chunks:
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


# ---------- 2. Les modèles ----------

def modele_tfidf(sans_mots_vides: bool):
    """TF-IDF (éventuellement sans les mots vides) puis régression logistique équilibrée."""
    return make_pipeline(
        TfidfVectorizer(stop_words=MOTS_VIDES if sans_mots_vides else None),
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    )


def predire_avec_e5(chunks: list[dict], y_train: list[str], X_test: list[str]) -> list[str]:
    """Régression logistique équilibrée, nourrie avec les embeddings e5 (l'index de la v2)."""
    # Import ici : search.py charge e5 au démarrage, inutile pour les modèles TF-IDF
    from search import load_or_build_index, model, PREFIXE_QUESTION

    X_train_vecteurs = load_or_build_index(chunks)          # les 260 passages, déjà encodés (cache)
    questions = []
    for q in X_test:
        questions.append(PREFIXE_QUESTION + q)              # e5 attend un préfixe devant une question
    X_test_vecteurs = model.encode(questions, normalize_embeddings=True)

    classifieur = LogisticRegression(max_iter=1000, class_weight="balanced")
    classifieur.fit(X_train_vecteurs, y_train)              # entraîner
    return list(classifieur.predict(X_test_vecteurs))


# ---------- 3. Évaluer ----------

def score_par_matiere(y_vrai: list[str], y_predit: list[str], matieres: list[str]) -> dict:
    """Pour chaque matière : part de ses questions bien classées (diagonale / total de la ligne)."""
    matrice = confusion_matrix(y_vrai, y_predit, labels=matieres)
    scores = {}
    for i, matiere in enumerate(matieres):
        scores[matiere] = matrice[i, i] / matrice[i].sum()
    return scores


def afficher_matrice(y_vrai: list[str], y_predit: list[str], matieres: list[str]):
    """Matrice de confusion : lignes = vraie matière, colonnes = matière prédite."""
    matrice = confusion_matrix(y_vrai, y_predit, labels=matieres)
    print("vraie \\ prédite " + "".join(f"{m:>7}" for m in matieres))
    for i, ligne in enumerate(matrice):
        print(f"{matieres[i]:>15} " + "".join(f"{n:>7}" for n in ligne))


if __name__ == "__main__":
    chunks = charger_passages()
    X_train, y_train = preparer_entrainement(chunks)
    X_test, y_test = preparer_test()
    matieres = sorted(compter(y_train))

    resultats = {}       # nom du modèle → ses prédictions sur les 40 questions

    for nom, sans_mots_vides in [("TF-IDF", False), ("TF-IDF sans mots vides", True)]:
        modele = modele_tfidf(sans_mots_vides)
        modele.fit(X_train, y_train)
        resultats[nom] = list(modele.predict(X_test))

    resultats["e5 (sens)"] = predire_avec_e5(chunks, y_train, X_test)

    # Tableau comparatif : global, puis par matière
    print(f"\n{'Modèle':25} {'Global':>7}" + "".join(f"{m:>7}" for m in matieres))
    for nom, predictions in resultats.items():
        scores = score_par_matiere(y_test, predictions, matieres)
        ligne = f"{nom:25} {100 * accuracy_score(y_test, predictions):>6.0f}%"
        ligne += "".join(f"{100 * scores[m]:>6.0f}%" for m in matieres)
        print(ligne)

    print("\nMatrice de confusion du modèle e5 :")
    afficher_matrice(y_test, resultats["e5 (sens)"], matieres)