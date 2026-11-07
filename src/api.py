"""v4 : l'API web de l'assistant (premier essai)."""
from fastapi import FastAPI

app = FastAPI(title="Assistant de révision IA")


@app.get("/")
def accueil():
    """Route d'accueil : vérifie que l'API répond."""
    return {"message": "L'assistant de révision est en ligne"}


@app.get("/bonjour/{prenom}")
def bonjour(prenom: str):
    """Le {prenom} de l'adresse devient le paramètre prenom de la fonction."""
    return {"message": f"Bonjour {prenom} !"}