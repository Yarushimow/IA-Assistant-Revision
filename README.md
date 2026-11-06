# Assistant de révision IA – EFREI P2-PLUS

Un assistant qui répond à mes questions de cours **à partir de mes propres fiches de révision** : il retrouve les passages pertinents, puis un LLM rédige la réponse en citant la fiche et la section d'où elle vient. Un classifieur entraîné par moi devine aussi la matière d'une question.

> Projet perso de Yoan DAI (EFREI Paris, P2-PLUS), en cours de construction. Version actuelle : **v3, classifieur de matière (88 % de précision)**.

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
3. **Recherche (R)** : la question devient un vecteur ; on garde les 3 passages les plus proches (similarité cosinus), avec **une seule place par section**.
4. **Augmentation (A)** : ces 3 passages, étiquetés `[Extrait n — fiche › section]`, sont placés dans le prompt avec la question.
5. **Génération (G)** : un LLM rédige la réponse en suivant des consignes « system » : utiliser **uniquement** les extraits, recopier les informations utiles, citer les extraits, et répondre « Je ne trouve pas » si la réponse n'y est pas.

Deux LLM sont branchés derrière une seule fonction `generer()` :
- **Gemini** (API Google, en ligne) : avec `--gemini`, et bascule automatique sur un modèle de secours si le serveur est surchargé (erreur 503) ;
- **Mistral 7B** (via Ollama, **en local** sur ma carte graphique) : gratuit, privé, fonctionne sans Internet.

**Classifieur de matière** (`src/classifieur.py`) : une régression logistique (scikit-learn) entraînée par moi pour deviner la matière d'une question parmi les 7.

## Résultats

### v3 : un classifieur de matière, entraîné par moi

**Apprentissage supervisé** : le modèle est entraîné sur les **260 passages** de mes fiches, chacun étiqueté par sa fiche (des données étiquetées « gratuitement »), et testé sur les **40 questions** du jeu de test de la v2, qu'il n'a jamais vues. La difficulté : il apprend sur des passages de cours, mais doit reconnaître des questions courtes, écrites autrement.

| Modèle | Précision globale | Probas (SM301) | FDPV (SM302) | Linux (TI307) |
|---|---|---|---|---|
| Au hasard (référence) | 14 % | | | |
| Toujours « Linux » (référence) | 12 % | | | |
| TF-IDF + régression logistique | 42 % | | | |
| + rééquilibrage des classes | 78 % | 43 % | 40 % | 100 % |
| + suppression des mots vides | 82 % | 57 % | 40 % | 100 % |
| **Embeddings e5 + régression logistique** | **88 %** | 57 % | **100 %** | 80 % |

**Ce que la matrice de confusion et l'analyse des poids m'ont appris :**
- **Le déséquilibre des données coûtait 36 points** : Linux avait 73 passages, les probas seulement 16. Avec `class_weight="balanced"`, le modèle ne répond plus « Linux » dès qu'il hésite.
- **Le 78 % global cachait 40 % sur les deux matières de maths.** En regardant les poids de la régression logistique, « Comment calculer la variance ? » partait vers Linux parce que le mot « variance » pesait +0,15 et le mot « la » +0,63 : mes fiches de maths sont pleines de formules que TF-IDF ne sait pas lire.
- **Les embeddings e5 de la v2, réutilisés comme entrée du classifieur**, font passer FDPV de 40 % à 100 % : comprendre le sens bat compter les mots. Les erreurs restantes sont « raisonnables » (probas confondues avec FDPV), mais Linux recule de 100 % à 80 % : un gain global peut cacher un recul sur une classe.

### v2 : une évaluation honnête de la recherche

Le mini-jeu de la v0 (12 questions) avait servi à **prendre mes décisions** : son score était donc trop optimiste. Pour la v2, j'ai écrit un **jeu de test séparé** de 40 nouvelles questions (`data/questions_test.json`), réparties sur les 7 fiches, faciles, moyennes et difficiles, sans regarder les résultats de la recherche. Une réponse compte si un passage de la **bonne fiche** et d'une **section acceptée** arrive dans le top 3 : c'est le **recall@3** (`src/evaluation.py`).

| Méthode | recall@3 | Facile | Moyen | Difficile |
|---|---|---|---|---|
| MPNet (référence) | 75 % | 12/12 | 10/14 | 8/14 |
| MPNet + une place par section | 75 % | 12/12 | 10/14 | 8/14 |
| e5, modèle conçu pour la recherche | 82 % | 12/12 | 11/14 | 10/14 |
| **e5 + une place par section** | **85 %** | 12/12 | 12/14 | 10/14 |

Le choix du modèle compte le plus (+7 points). « Une place par section » ne sert à rien seule, mais aide une fois combinée au bon modèle (+3 points).

### v1 : la génération, et le problème des hallucinations

Sans RAG, Mistral 7B répond à « Qu'est-ce qu'une bascule JK ? » avec assurance… et **0 ligne juste sur 4** dans la table de vérité. Avec le RAG, il retrouve les bons comportements, et Gemini recopie la table complète en citant ses sources.

Comparaison sur 4 questions (`src/comparer_llm.py`), mêmes extraits et mêmes consignes, seul le LLM change :

| Question | Mistral 7B (local) | Gemini (en ligne) |
|---|---|---|
| Bascule JK | juste, mais incomplète | ✅ table complète, sources citées |
| Formule de Bayes | formule juste, mais citation d'un extrait qui n'existe pas | juste, mais sans formule (absente de l'extrait trouvé) |
| `umask` (recherche ratée) | répond de mémoire, avec un exemple faux | ✅ « Je ne trouve pas » |
| Modèle OSI (absent des fiches) | ❌ invente 7 couches, dont 2 qui n'existent pas | ✅ « Je ne trouve pas » |
| **Réponses avec invention** | **3 sur 4** | **0 sur 4** |

Un RAG ne peut pas être meilleur que sa recherche : c'est ce qui a motivé la v2.

### v0 : la recherche, mesurée avant d'être améliorée

Un mini-jeu de 12 questions (`src/test_questions.py`, devenu mon jeu de développement), en corrigeant **une seule chose à la fois** : de 3/10 (MiniLM) à 8/12 (MPNet), en passant par un test plus juste et un nettoyage des données (des commentaires shell `# umask 022` étaient pris pour des titres de section).

## Limites connues

- **Recherche** : 6 questions sur 40 ratent encore la bonne section, surtout quand la question ne reprend aucun mot de la fiche ou parle de formules.
- **Classifieur** : probas et FDPV restent parfois confondues ; il n'est pas encore branché dans la recherche (prochaine étape possible : restreindre la recherche à la matière prédite).
- **Jeu de test** : 40 questions, donc une question vaut 2,5 points ; les sections acceptées ont été choisies par moi.
- **Mistral 7B en local** : invente souvent malgré les consignes ; ses réponses sont à vérifier.
- **Gemini** : dépend des serveurs de Google (erreurs 503 aux heures de pointe, quotas du niveau gratuit).

## Ce que j'ai appris

- **Un embedding capte le sens, mais pas toujours celui qu'on croit.** Mon premier modèle trouvait « une pile est une structure LIFO » plus proche de « une pile électrique fournit du courant » que de sa propre définition.
- **Mesurer avant d'améliorer, et séparer développement et test.** Un jeu de questions qui a servi à prendre des décisions donne un score trop optimiste.
- **Toujours regarder ses données brutes**, et leur répartition : un export avait créé de faux titres de section, et un déséquilibre entre matières coûtait 36 points au classifieur.
- **Un LLM peut se tromper avec assurance.** Le RAG et la consigne « dis-le si tu ne sais pas » rendent les réponses vérifiables, mais leur qualité dépend d'abord de la recherche.
- **Un chiffre global ne suffit pas.** 78 % de précision cachait 40 % sur les matières de maths : il faut toujours regarder le détail par classe et comprendre **pourquoi** le modèle se trompe.

## Lancer le projet

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (source .venv/bin/activate sur Linux/Mac)
pip install -r requirements.txt

# Recherche
python src/search.py "comment supprimer une cellule dans une liste circulaire ?"
python src/evaluation.py                                       # recall@3 sur le jeu de test (40 questions)

# RAG
python src/rag.py "Qu'est-ce qu'une bascule JK ?"             # Mistral 7B en local (Ollama)
python src/rag.py --gemini "Qu'est-ce qu'une bascule JK ?"    # Gemini en ligne
python src/comparer_llm.py                                     # compare les deux

# Classifieur de matière
python src/classifieur.py                                      # entraîne et compare les 3 modèles
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
- [x] v3 – Classifieur de matière entraîné (scikit-learn) : 42 % → 88 % de précision
- [ ] v4 – Intégration à mon site de révision P2-PLUS et mise en ligne