"""Premier appel à un LLM local avec Ollama (le modèle tourne sur ma carte graphique)."""
import ollama

MODELE = "mistral"     # le nom du modèle téléchargé avec « ollama pull »

reponse = ollama.chat(
    model=MODELE,
    messages=[
        {"role": "user", "content": "Qu'est-ce qu'une bascule JK ?"},   # ta question au LLM
    ],
)

print(reponse.message.content)