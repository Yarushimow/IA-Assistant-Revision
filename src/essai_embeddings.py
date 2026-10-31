from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

phrases = [
    "Une pile est une structure LIFO",                                                          # 0
    "Le dernier élément empilé sort en premier",                                                # 1
    "L'effet photoélectrique",                                                                  # 2
    "Une pile est une structure de données où le dernier élément ajouté est le premier retiré", # 3
    "Une pile électrique fournit du courant",                                                   # 4
]

vecteurs = model.encode(phrases, normalize_embeddings=True)
print(vecteurs.shape)

scores = vecteurs @ vecteurs.T      # toutes les paires d'un coup
print(np.round(scores, 2))