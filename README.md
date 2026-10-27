# Assistant de révision IA – EFREI P2-PLUS

Un assistant qui répond à des questions de cours **à partir de mes propres fiches de révision**, en citant la fiche et la section d'où vient la réponse.

> Projet perso de Yoan DAI (EFREI Paris, P2-PLUS) – en cours de construction.

## Pourquoi ce projet

Je fais une fiche par matière avant chaque contrôle. Quand je révise, je perds du temps à retrouver « où était la formule de Bayes » ou « comment on supprime dans une liste circulaire ». L'objectif : poser la question en langage naturel et retrouver tout de suite le bon passage, puis obtenir une réponse rédigée.

## Comment ça marche (architecture RAG)

1. **Chargement** : lecture des fiches Markdown dans `data/fiches/`.
2. **Découpage (chunking)** : chaque fiche est coupée en petits passages, par section.
3. **Embeddings** : chaque passage est transformé en vecteur avec un modèle multilingue (sentence-transformers).
4. **Recherche sémantique** : la question est aussi transformée en vecteur ; on garde les passages les plus proches (similarité cosinus).
5. **Génération** (étape suivante) : un LLM rédige la réponse à partir de ces passages uniquement, en citant ses sources.

## Feuille de route

- [ ] v0 – Recherche sémantique en ligne de commande
- [ ] v1 – Réponse rédigée par un LLM (RAG) avec citation des sources
- [ ] v2 – Jeu de questions de test pour mesurer la qualité de la recherche
- [ ] v3 – Classifieur scikit-learn : ranger automatiquement une question par matière
- [ ] v4 – Interface web (site de révision) et mise en ligne

## Lancer le projet

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (source .venv/bin/activate sur Linux/Mac)
pip install -r requirements.txt
python src/search.py "comment supprimer une cellule dans une liste circulaire ?"
```

## Données

`data/fiches/` contient mes fiches de révision personnelles (Linux, systèmes numériques, physique moderne, fonctions de plusieurs variables, structures de données). Les supports de cours des enseignants ne sont pas inclus.
