"""Mini-évaluation : est-ce qu'une des bonnes sections arrive dans le top 3 ?"""
from load import load_fiches, chunk_fiche
from search import load_or_build_index, search

# (question, [morceaux de titres de sections acceptées])
TESTS = [
    # --- Faciles : les mots du titre sont dans la question ---
    ("Qu'est-ce qu'une bascule JK ?", ["Bascule JK"]),
    ("Qu'est-ce qu'une pile ?", ["Piles et files", "Fiche CE : listes, piles, files"]),
    ("Comment calculer le gradient et la dérivée directionnelle ?", ["Gradient"]),
    ("Comment fonctionne la transformation de Lorentz ?", ["Transformation de Lorentz"]),
    # --- Difficiles : formulées autrement, il faut comprendre le sens ---
    ("Comment on enlève des droits par défaut à la création d'un fichier sous Linux ?", ["umask"]),
    ("Pourquoi le temps passe plus lentement pour un objet qui va très vite ?", ["Dilatation du temps", "Ch. 2 · Relativité restreinte"]),
    ("Comment montrer qu'une limite en deux variables existe en changeant de coordonnées ?", ["polaires", "La méthode", "Au contrôle"]),
    ("Comment créer un raccourci qui pointe vers un autre fichier ?", ["Liens physiques"]),
    ("Comment diviser la fréquence d'une horloge par deux ?", ["diviseur de fréquence"]),
    ("Comment envoyer la sortie d'une commande dans l'entrée d'une autre ?", ["Tubes"]),
    # --- Nouvelles fiches (difficiles) ---
    ("Comment retrouver la probabilité d'une cause quand on connaît l'effet observé ?", ["Chapitre 2"]),
    ("Comment calculer la force totale exercée par plusieurs charges sur une seule ?", ["superposition"]),
]

# Préparer les passages et l'index (rechargé depuis le disque s'il est à jour)
chunks = []
for fiche in load_fiches():
    chunks.extend(chunk_fiche(fiche))
embeddings = load_or_build_index(chunks)

reussites = 0
for question, attendus in TESTS:
    resultats = search(question, chunks, embeddings)

    trouve = False
    sections_trouvees = []
    for score, passage in resultats:
        sections_trouvees.append(passage["section"])
        for attendu in attendus:                       # on teste chaque section acceptée
            if attendu in passage["section"]:
                trouve = True

    if trouve:
        reussites = reussites + 1
        print("✅", question)
    else:
        print("❌", question)
        print("     trouvé à la place :", sections_trouvees)

print(f"\nScore : {reussites}/{len(TESTS)}")