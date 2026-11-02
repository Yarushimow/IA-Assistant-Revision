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


def evaluer(questions: list[dict], chunks: list[dict], embeddings, k: int = K):
    """Pose chaque question à la recherche et compte les réussites (au moins un passage pertinent dans le top k)."""
    reussites = 0
    total_par_diff = {}        # ex. {"facile": 12, "moyen": 15, "difficile": 13}
    ok_par_diff = {}           # combien de réussites par difficulté
    echecs = []                # pour regarder ensuite ce qui a raté

    for q in questions:
        resultats = search(q["question"], chunks, embeddings, top_k=k)

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


if __name__ == "__main__":
    # 1. Charger le jeu de test (fichier JSON → liste de dictionnaires Python)
    with open(QUESTIONS_PATH, encoding="utf-8") as fichier:
        questions = json.load(fichier)

    # 2. Charger les passages et l'index
    chunks = []
    for fiche in load_fiches():
        chunks.extend(chunk_fiche(fiche))
    embeddings = load_or_build_index(chunks)

    # 3. Évaluer
    reussites, total_par_diff, ok_par_diff, echecs = evaluer(questions, chunks, embeddings)

    # 4. Afficher les résultats
    print(f"\nrecall@{K} : {reussites}/{len(questions)} = {100 * reussites / len(questions):.0f} %\n")
    for diff in ["facile", "moyen", "difficile"]:
        ok = ok_par_diff.get(diff, 0)
        total = total_par_diff.get(diff, 0)
        print(f"  {diff:10} {ok}/{total}")

    print(f"\nÉCHECS ({len(echecs)}) :")
    for q, resultats in echecs:
        print(f"\n❌ [{q['fiche']}] {q['question']}")
        for score, passage in resultats:
            print(f"     [{score:.2f}] {passage['source']} › {passage['section']}")