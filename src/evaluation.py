"""v2 : évaluation de la recherche (recall@3) sur le jeu de test (40 questions jamais utilisées pour régler le système)."""
import json
from pathlib import Path

from load import load_fiches, chunk_fiche
from search import load_or_build_index, search

QUESTIONS_PATH = Path(__file__).parent.parent / "data" / "questions_test.json"
K = 3      # nombre de passages regardés (= ceux qu'on donne au LLM)


def est_pertinent(passage: dict, q: dict) -> bool:
    """Un passage est pertinent s'il vient de la bonne fiche ET d'une des sections acceptées."""
    if not passage["source"].startswith(q["fiche"]):
        return False
    for attendu in q["attendus"]:
        if attendu in passage["section"]:
            return True
    return False


def evaluer(questions: list[dict], chunks: list[dict], embeddings, k: int = K, une_par_section: bool = True):
    """Pose chaque question à la recherche et compte les réussites (au moins un passage pertinent dans le top k)."""
    reussites = 0
    total_par_diff = {}
    ok_par_diff = {}
    echecs = []

    for q in questions:
        resultats = search(q["question"], chunks, embeddings, top_k=k, une_par_section=une_par_section)

        trouve = False
        for score, passage in resultats:
            if est_pertinent(passage, q):
                trouve = True

        diff = q["difficulte"]
        total_par_diff[diff] = total_par_diff.get(diff, 0) + 1
        if trouve:
            reussites += 1
            ok_par_diff[diff] = ok_par_diff.get(diff, 0) + 1
        else:
            echecs.append((q, resultats))

    return reussites, total_par_diff, ok_par_diff, echecs


def afficher(nom: str, questions: list[dict], reussites: int, total_par_diff: dict, ok_par_diff: dict):
    """Affiche le recall@k global puis par difficulté."""
    print(f"\n=== {nom} ===")
    print(f"recall@{K} : {reussites}/{len(questions)} = {100 * reussites / len(questions):.0f} %")
    for diff in ["facile", "moyen", "difficile"]:
        print(f"  {diff:10} {ok_par_diff.get(diff, 0)}/{total_par_diff.get(diff, 0)}")


if __name__ == "__main__":
    with open(QUESTIONS_PATH, encoding="utf-8") as fichier:
        questions = json.load(fichier)

    chunks = []
    for fiche in load_fiches():
        chunks.extend(chunk_fiche(fiche))
    embeddings = load_or_build_index(chunks)

    # On compare les méthodes : (nom affiché, valeur de une_par_section)
    METHODES = [
        ("Référence (top 3 brut)", False),
        ("A : une place par section", True),
    ]

    for nom, une_par_section in METHODES:
        reussites, total_par_diff, ok_par_diff, echecs = evaluer(
            questions, chunks, embeddings, une_par_section=une_par_section
        )
        afficher(nom, questions, reussites, total_par_diff, ok_par_diff)

    # Les échecs de la DERNIÈRE méthode évaluée (la meilleure, en principe)
    print(f"\nÉCHECS restants ({len(echecs)}) :")
    for q, resultats in echecs:
        print(f"\n❌ [{q['fiche']}] {q['question']}")
        for score, passage in resultats:
            print(f"     [{score:.2f}] {passage['source']} › {passage['section']}")