"""Premier contact avec l'API Gemini : lister les modèles disponibles, puis un premier appel."""
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()                                   # lit le fichier .env
cle = os.getenv("GEMINI_API_KEY")                # le nom de la variable écrite dans .env

if cle is None:
    print("Clé introuvable : vérifie ton fichier .env")
    raise SystemExit

client = genai.Client(api_key=cle)

# 1. Les modèles accessibles avec ta clé (on garde ceux qui contiennent « flash » : rapides et gratuits)
print("Modèles disponibles :")
for modele in client.models.list():
    if "flash" in modele.name:
        print("  ", modele.name)

# 2. Un premier appel (on choisira le modèle après avoir vu la liste)
MODELE_GEMINI = "gemini-2.5-flash"                       # à remplir après le premier lancement

reponse = client.models.generate_content(
    model=MODELE_GEMINI,
    contents="Qu'est-ce qu'une bascule JK ?",
)
print("\nRéponse :\n", reponse.text)