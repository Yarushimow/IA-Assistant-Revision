"""Mini-évaluation : est-ce que la bonne section arrive dans le top 3 ?"""
from load import load_fiches, chunk_fiche
from search import build_index, search

# (question, morceau du titre de la section attendue)
TESTS = [
    # --- Faciles : les mots du titre sont dans la question ---
    ("Qu'est-ce qu'une bascule JK ?", "Bascule JK"),
    ("Qu'est-ce qu'une pile ?", "Piles et files"),
    ("Comment calculer le gradient et la dérivée directionnelle ?", "Gradient"),
    ("Comment fonctionne la transformation de Lorentz ?", "Transformation de Lorentz"),
    # --- Difficiles : formulées autrement, il faut comprendre le sens ---
    ("Comment on enlève des droits par défaut à la création d'un fichier sous Linux ?", "umask"),
    ("Pourquoi le temps passe plus lentement pour un objet qui va très vite ?", "Dilatation du temps"),
    ("Comment montrer qu'une limite en deux variables existe en changeant de coordonnées ?", "polaires"),
    ("Comment créer un raccourci qui pointe vers un autre fichier ?", "Liens physiques"),
    ("Comment diviser la fréquence d'une horloge par deux ?", "diviseur de fréquence"),
    ("Comment envoyer la sortie d'une commande dans l'entrée d'une autre ?", "Tubes"),
]

# Préparer les passages et l'index (une seule fois pour toutes les questions)
chunks = []
for fiche in load_fiches():
    chunks.extend(chunk_fiche(fiche))
embeddings = build_index(chunks)

reussites = 0
for question, attendu in TESTS:
    resultats = search(question, chunks, embeddings)

    trouve = False
    sections_trouvees = []
    for score, passage in resultats:
        sections_trouvees.append(passage["section"])
        if attendu in passage["section"]:      # le morceau attendu est-il dans le titre de ce passage ?
            trouve = True

    if trouve:
        reussites = reussites + 1
        print("✅", question)
    else:
        print("❌", question)
        print("     trouvé à la place :", sections_trouvees)

print(f"\nScore : {reussites}/{len(TESTS)}")