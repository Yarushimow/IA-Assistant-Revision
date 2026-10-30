# Assistant de révision IA – EFREI P2-PLUS

Un assistant qui retrouve, dans **mes propres fiches de révision**, les passages qui répondent à une question de cours posée en langage naturel, en citant la fiche et la section d'où ils viennent.

> Projet perso de Yoan DAI (EFREI Paris, P2-PLUS), en cours de construction. Version actuelle : **v0, recherche sémantique**.

## Démo

```
$ python src/search.py "Qu'est-ce qu'une bascule JK ?"

[0.41] TE302_systemes_numeriques.md › Bascule JK
**Table de vérité** (au front actif) | J | K | Q(t+Δt) | Fonction | ...

[0.39] TE302_systemes_numeriques.md › Montage diviseur de fréquence (toggle)
Bascule D avec D = Q̄, ou JK avec J = K = 1 : la sortie s'inverse à chaque front actif ...
```

La recherche se fait **par le sens**, pas par mots-clés : « Comment retrouver la probabilité d'une cause quand on connaît l'effet observé ? » trouve la section sur la formule de Bayes, sans que le mot « Bayes » soit dans la question.

## Pourquoi ce projet

Je fais une fiche par matière avant chaque contrôle. Quand je révise, je perds du temps à retrouver « où était la formule de Bayes » ou « comment on supprime dans une liste circulaire ». L'objectif : poser la question en langage naturel et retrouver tout de suite le bon passage, puis (v1) obtenir une réponse rédigée.

## Comment ça marche (architecture RAG)

1. **Chargement** : lecture des fiches Markdown dans `data/fiches/` (7 fiches).
2. **Découpage** : chaque fiche est coupée par section, puis les sections trop longues sont recoupées par paragraphes (800 caractères max) → 260 passages.
3. **Embeddings** : chaque passage (titre de section + texte) est transformé en vecteur de 768 dimensions avec le modèle multilingue `paraphrase-multilingual-mpnet-base-v2`.
4. **Index sur disque** : les vecteurs sont calculés une fois et sauvegardés (`data/index.npy`), puis rechargés instantanément.
5. **Recherche** : la question est transformée en vecteur ; on garde les 3 passages les plus proches (similarité cosinus = produit scalaire de vecteurs normalisés).
6. **Génération** (v1, à venir) : un LLM rédige la réponse à partir de ces passages uniquement, en citant ses sources.

## Résultats : mesurer avant d'améliorer

J'ai écrit un mini-jeu de test (`src/test_questions.py`) : des questions dont je connais la bonne section, faciles (les mots du titre sont dans la question) ou difficiles (reformulées). Le score compte les questions dont une bonne section arrive dans le top 3. J'ai corrigé **une seule chose à la fois** en recalculant le score après chacune :

| Étape | Score | Ce qui a changé |
|---|---|---|
| Départ (MiniLM, 384 dim.) | 3/10 | Faciles 3/4, difficiles 0/6 : le modèle cherchait surtout par mots |
| Test plus juste | 5/10 | Plusieurs sections acceptées par question, choisies en relisant les fiches |
| Nettoyage des données | 5/10 | L'export avait supprimé les blocs de code de la fiche Linux : des commentaires shell (`# umask 022`) étaient pris pour des titres. Score inchangé : le vrai problème était le modèle |
| Modèle plus gros (MPNet, 768 dim.) | **6/10** | Plus aucune réponse hors sujet ; les erreurs restantes tombent dans la bonne fiche |
| + 2 fiches et 2 questions | **8/12** | Pas de régression sur les anciennes questions, les 2 nouvelles passent |

## Limites connues

- **Reformulations difficiles** : 4 questions sur 12 ratent encore la bonne section (souvent de peu : bon chapitre, mauvaise section).
- **Sigles techniques** : le modèle comprend mal les sigles comme « LIFO ».
- **Cache** : l'index n'est reconstruit que si le nombre de passages change. Corriger un texte sans changer ce nombre laisse un index périmé (pour l'instant : supprimer `data/index.npy`). Prochaine amélioration : une empreinte des textes et du modèle.

## Ce que j'ai appris

- **Un embedding capte le sens, mais pas toujours celui qu'on croit.** Mon premier modèle trouvait « une pile est une structure LIFO » plus proche de « une pile électrique fournit du courant » que de sa propre définition : un petit modèle se fie beaucoup aux mots.
- **Mesurer avant d'améliorer.** Sans mini-jeu de test, je n'aurais pas su quelle correction aidait vraiment. En changeant une seule chose à la fois, j'ai aussi vu qu'une correction juste (nettoyer les données) peut ne rien changer au score, et que c'est une information en soi.
- **Toujours regarder ses données brutes.** Un export avait transformé des commentaires shell en faux titres de section : un bug invisible tant qu'on n'ouvre pas le fichier.

## Lancer le projet

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (source .venv/bin/activate sur Linux/Mac)
pip install -r requirements.txt
python src/search.py "comment supprimer une cellule dans une liste circulaire ?"
python src/test_questions.py   # le mini-jeu de test
```

Le premier lancement télécharge le modèle (environ 1,1 Go) et construit l'index ; les suivants sont rapides.

## Données

`data/fiches/` contient mes 7 fiches de révision personnelles : structures de données, Linux, systèmes numériques, physique moderne, fonctions de plusieurs variables, probabilités, électrostatique. Les supports de cours des enseignants ne sont pas inclus.

## Feuille de route

- [x] v0 – Recherche sémantique en ligne de commande, avec mini-jeu de test
- [ ] v1 – Réponse rédigée par un LLM (RAG) avec citation des sources
- [ ] v2 – Évaluation complète : 40 questions, recall@3, comparaison de modèles
- [ ] v3 – Classifieur scikit-learn : ranger automatiquement une question par matière
- [ ] v4 – Interface web (site de révision) et mise en ligne