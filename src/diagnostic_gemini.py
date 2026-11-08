"""Diagnostic : appeler Gemini UNE fois par modèle, avec une limite de temps, et afficher la vraie erreur."""
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        timeout=20_000,                                        # 20 secondes maximum (en millisecondes)
        retry_options=types.HttpRetryOptions(attempts=1),      # un seul essai : pas de réessai silencieux
    ),
)

MODELES_A_TESTER = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]

for modele in MODELES_A_TESTER:
    debut = time.time()
    try:
        reponse = client.models.generate_content(model=modele, contents="Réponds juste : OK")
        print(f"{modele:25} ✅ en {time.time() - debut:.1f} s : {reponse.text.strip()}")
    except errors.APIError as e:                     # Google a répondu avec un code d'erreur (4xx ou 5xx)
        print(f"{modele:25} ❌ erreur {e.code} : {str(e)[:200]}")
    except Exception as e:                           # autre problème, par exemple la limite de temps dépassée
        print(f"{modele:25} ❌ {type(e).__name__} après {time.time() - debut:.1f} s : {str(e)[:200]}")