# Assistant de révision IA – EFREI P2-PLUS

Un assistant qui répond à mes questions de cours **à partir de mes propres fiches de révision** : il retrouve les passages pertinents, puis un LLM rédige la réponse en citant la fiche et la section d'où elle vient.

> Projet perso de Yoan DAI (EFREI Paris, P2-PLUS), en cours de construction. Version actuelle : **v2, recherche évaluée et améliorée (recall@3 : 75 % → 85 %)**.

## Démo

```
$ python src/rag.py --gemini "Qu'est-ce qu'une bascule JK ?"

RÉPONSE (gemini) :
D'après tes fiches, le fonctionnement d'une bascule JK est défini par son comportement au front actif :

| J | K | Q(t+Δt) | Fonction    |
|---|---|---------|-------------|
| 0 | 0 | Q(t)    | M (mémoire) |
| 0 | 1 | 0       | R (reset)   |
| 1 | 0 | 1       | S (set)     |
| 1 | 1 | Q̄(t)    | T (toggle)  |
...
[Extrait 1, Extrait 2]

SOURCES :
  TE302_systemes_numeriques.md › Bascule JK
  TE302_systemes_numeriques.md › Montage diviseur de fréquence (toggle)
```

Et quand la réponse n'est pas dans mes fiches, il le dit au lieu d'inventer :

```
$ python src/rag.py --gemini "Quelles sont les 7 couches du modèle OSI ?"
Je ne trouve pas la réponse dans tes fiches.
```

## Pourquoi ce projet

Je fais une fiche par matière avant chaque contrôle. Quand je révise, je perds du temps à retrouver « où était la formule de Bayes » ou « comment on supprime dans une liste circulaire ». L'objectif : poser la question en langage naturel et obtenir une réponse fiable, tirée de **mes** fiches et de **mon** cours.

## Comment ça marche (architecture RAG)

**R**etrieval-**A**ugmented **G**eneration : on cherche d'abord, on rédige ensuite.

1. **Chargement et découpage** : les 7 fiches Markdown de `data/fiches/` sont coupées par section, puis par paragraphes (800 caractères max) → 260 passages.
2. **Embeddings** : chaque passage (titre de section + texte) devient un vecteur de 768 dimensions avec `multilingual-e5-base`, un modèle entraîné pour la **recherche asymétrique** (question courte → passage long) : les passages sont préfixés par `passage: ` et les questions par `query: `. L'index est sauvegardé sur disque avec une empreinte SHA-256 des textes et du modèle : il n'est recalculé que si une fiche ou le modèle change.
3. **Recherche (R)** : la question devient un vecteur ; on garde les 3 passages les plus proches (similarité cosinus), avec **une seule place par section**, pour donner au LLM trois endroits différents des fiches.
4. **Augmentation (A)** : ces 3 passages, étiquetés `[Extrait n — fiche › section]`, sont placés dans le prompt avec la question.
5. **Génération (G)** : un LLM rédige la réponse en suivant des consignes « system » : utiliser **uniquement** les extraits, recopier les informations utiles, citer les extraits, et répondre « Je ne trouve pas » si la réponse n'y est pas.

Deux LLM sont branchés derrière une seule fonction `generer()` :
- **Gemini** (API Google, en ligne) : avec `--gemini`, et bascule automatique sur un modèle de secours si le serveur est surchargé (erreur 503) ;
- **Mistral 7B** (via Ollama, **en local** sur ma carte graphique) : gratuit, privé, fonctionne sans Internet.

## Résultats

### v2 : une évaluation honnête de la recherche

Le mini-jeu de la v0 (12 questions) avait servi à **prendre mes décisions** (choix du modèle, sections acceptées) : son score était donc trop optimiste. Pour la v2, j'ai écrit un **jeu de test séparé** de 40 nouvelles questions (`data/questions_test.json`), réparties sur les 7 fiches, faciles, moyennes et difficiles (reformulées), sans regarder les résultats de la recherche. Une réponse compte si un passage de la **bonne fiche** et d'une **section acceptée** arrive dans le top 3 : c'est le **recall@3** (`src/evaluation.py`).

| Méthode | recall@3 | Facile | Moyen | Difficile |
|---|---|---|---|---|
| MPNet (référence) | 75 % | 12/12 | 10/14 | 8/14 |
| MPNet + une place par section | 75 % | 12/12 | 10/14 | 8/14 |
| e5, modèle conçu pour la recherche | 82 % | 12/12 | 11/14 | 10/14 |
| **e5 + une place par section** | **85 %** | 12/12 | 12/14 | 10/14 |

**Conclusions :**
- **Le choix du modèle compte le plus** (+7 points) : un modèle entraîné sur des paires question → passage comprend mieux les questions reformulées.
- **« Une place par section » ne sert à rien seule, mais aide une fois combinée au bon modèle** (+3 points) : avec MPNet, la bonne section était trop loin dans le classement ; avec e5, elle arrive souvent juste derrière et récupère la place libérée.
- Sur les 6 échecs restants, 5 tombent dans la bonne fiche, mais pas dans la bonne section.

### v0 : la recherche, mesurée avant d'être améliorée

Un mini-jeu de 12 questions (`src/test_questions.py`, devenu mon jeu de développement), en corrigeant **une seule chose à la fois** :

| Étape | Score | Ce qui a changé |
|---|---|---|
| Départ (MiniLM, 384 dim.) | 3/10 | Faciles 3/4, difficiles 0/6 : le modèle cherchait surtout par mots |
| Test plus juste | 5/10 | Plusieurs sections acceptées par question, choisies en relisant les fiches |
| Nettoyage des données | 5/10 | Des commentaires shell (`# umask 022`) étaient pris pour des titres. Score inchangé : le vrai problème était le modèle |
| Modèle plus gros (MPNet, 768 dim.) | 6/10 | Plus aucune réponse hors sujet |
| + 2 fiches et 2 questions | 8/12 | Pas de régression, les 2 nouvelles passent |

### v1 : la génération, et le problème des hallucinations

Sans RAG, Mistral 7B répond à « Qu'est-ce qu'une bascule JK ? » avec assurance… et **0 ligne juste sur 4** dans la table de vérité. Avec le RAG, il retrouve les bons comportements, et Gemini recopie la table complète en citant ses sources.

Comparaison sur 4 questions (`src/comparer_llm.py`, recherche MPNet), mêmes extraits et mêmes consignes, seul le LLM change :

| Question | Mistral 7B (local) | Gemini (en ligne) |
|---|---|---|
| Bascule JK | juste, mais incomplète | ✅ table complète, sources citées |
| Formule de Bayes | formule juste, mais citation d'un extrait qui n'existe pas | juste, mais sans formule (absente de l'extrait trouvé) |
| `umask` (recherche ratée) | répond de mémoire, avec un exemple faux | ✅ « Je ne trouve pas » |
| Modèle OSI (absent des fiches) | ❌ invente 7 couches, dont 2 qui n'existent pas | ✅ « Je ne trouve pas » |
| **Réponses avec invention** | **3 sur 4** | **0 sur 4** |

**Conclusion :** un RAG ne peut pas être meilleur que sa recherche. Quand la recherche rate le bon passage, même un excellent LLM ne peut que dire « je ne trouve pas ». C'est ce qui a motivé la v2.

## Limites connues

- **Recherche** : 6 questions sur 40 ratent encore la bonne section, surtout quand la question ne reprend aucun mot de la fiche ou parle de formules (« dériver f(x(t), y(t)) »).
- **Jeu de test** : 40 questions, donc une question vaut 2,5 points ; les sections acceptées ont été choisies par moi et peuvent être trop strictes ou trop larges dans quelques cas.
- **Mistral 7B en local** : invente souvent malgré les consignes ; ses réponses sont à vérifier.
- **Gemini** : dépend des serveurs de Google (erreurs 503 aux heures de pointe, quotas du niveau gratuit).
- **Vitesse** : l'index e5 se construit en environ 1 min 30 sur le processeur (une seule fois grâce au cache).

## Ce que j'ai appris

- **Un embedding capte le sens, mais pas toujours celui qu'on croit.** Mon premier modèle trouvait « une pile est une structure LIFO » plus proche de « une pile électrique fournit du courant » que de sa propre définition.
- **Mesurer avant d'améliorer, et séparer développement et test.** Un jeu de questions qui a servi à prendre des décisions donne un score trop optimiste ; il faut un jeu de test que le système n'a jamais influencé.
- **Toujours regarder ses données brutes.** Un export avait transformé des commentaires shell en faux titres de section : un bug invisible tant qu'on n'ouvre pas le fichier.
- **Un LLM peut se tromper avec assurance.** Le RAG et la consigne « dis-le si tu ne sais pas » rendent les réponses vérifiables, mais leur qualité dépend d'abord de la recherche.
- **Une idée logique n'est pas une idée qui marche.** « Une place par section » semblait évidente, et n'a rien changé seule ; c'est la mesure qui l'a montré, et qui a montré qu'elle aidait combinée à un meilleur modèle.

## Lancer le projet

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (source .venv/bin/activate sur Linux/Mac)
pip install -r requirements.txt

# Recherche seule
python src/search.py "comment supprimer une cellule dans une liste circulaire ?"
python src/evaluation.py                                       # recall@3 sur le jeu de test (40 questions)
python src/test_questions.py                                   # mini-jeu de développement (12 questions)

# RAG
python src/rag.py "Qu'est-ce qu'une bascule JK ?"             # Mistral 7B en local (Ollama)
python src/rag.py --gemini "Qu'est-ce qu'une bascule JK ?"    # Gemini en ligne
python src/comparer_llm.py                                     # compare les deux
```

- **Ollama** : installer [Ollama](https://ollama.com), puis `ollama pull mistral`.
- **Gemini** : créer une clé gratuite sur Google AI Studio et l'ajouter dans un fichier `.env` à la racine : `GEMINI_API_KEY=...`. Ce fichier est ignoré par Git.

Le premier lancement télécharge le modèle d'embeddings (environ 1,1 Go) et construit l'index ; les suivants sont rapides.

## Données

`data/fiches/` contient mes 7 fiches de révision personnelles : structures de données, Linux, systèmes numériques, physique moderne, fonctions de plusieurs variables, probabilités, électrostatique. `data/questions_test.json` contient le jeu de test. Les supports de cours des enseignants ne sont pas inclus.

## Feuille de route

- [x] v0 – Recherche sémantique en ligne de commande, avec mini-jeu de test
- [x] v1 – Réponse rédigée par un LLM (RAG) avec citation des sources, Gemini et Mistral 7B en local
- [x] v2 – Évaluation sur un jeu de test de 40 questions (recall@3) et amélioration de la recherche : 75 % → 85 %
- [ ] v3 – Classifieur scikit-learn : ranger automatiquement une question par matière
- [ ] v4 – Intégration à mon site de révision P2-PLUS et mise en ligne