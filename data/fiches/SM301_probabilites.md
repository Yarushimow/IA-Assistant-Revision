# Fiche formulaire — CE Probabilités (chap 1, 2, 3)

Oct 6, 2026 · @Yoan

## Chapitre 1 — Espace probabilisé

On modélise une expérience aléatoire par un univers Ω, des événements (parties de Ω) et une probabilité P.

| Notation | Langage probabiliste |
| --- | --- |
| Ω | univers (ensemble des issues possibles) |
| ω ∈ Ω | issue / résultat |
| A ⊂ Ω | événement |
| Ā (ou Aᶜ) | événement contraire de A |
| A ∩ B | A et B se réalisent |
| A ∪ B | A ou B (au moins un des deux) |
| A ∩ B = ∅ | A et B incompatibles |
| A ⊂ B | A implique B |

**Lois de De Morgan**

```latex
\overline{A \cup B} = \bar{A} \cap \bar{B} \qquad \overline{A \cap B} = \bar{A} \cup \bar{B}
```

**Axiomes d'une probabilité**

```latex
P(\Omega) = 1, \qquad 0 \le P(A) \le 1, \qquad P\Big(\bigcup_{i} A_i\Big) = \sum_{i} P(A_i) \ \text{si les } A_i \text{ sont 2 à 2 incompatibles}
```

**Propriétés à connaître par cœur**

```latex
P(\bar{A}) = 1 - P(A) \qquad P(\emptyset) = 0 \qquad A \subset B \Rightarrow P(A) \le P(B)
```

```latex
P(A \cup B) = P(A) + P(B) - P(A \cap B)
```

```latex
P(A \cup B \cup C) = P(A) + P(B) + P(C) - P(A \cap B) - P(A \cap C) - P(B \cap C) + P(A \cap B \cap C)
```

```latex
P(A) = P(A \cap B) + P(A \cap \bar{B})
```

**Équiprobabilité** (Ω fini, toutes les issues ont la même probabilité)

```latex
P(A) = \frac{\operatorname{card}(A)}{\operatorname{card}(\Omega)} = \frac{\text{nb de cas favorables}}{\text{nb de cas possibles}}
```

**Rappels de dénombrement**

| Situation | Nombre | Formule |
| --- | --- | --- |
| Ordonner n objets | permutations | n! |
| p-uplet avec répétition parmi n | p-listes | nᵖ |
| p objets ordonnés sans répétition parmi n | arrangements | n! / (n−p)! |
| p objets non ordonnés sans répétition parmi n | combinaisons « p parmi n » | n! / (p!(n−p)!) |

## Chapitre 2 — Probabilités conditionnelles

P(A | B) est la probabilité de A sachant que B est réalisé (notée aussi P\_B(A)), avec P(B) > 0.

**Définition**

```latex
P(A \mid B) = \frac{P(A \cap B)}{P(B)}
```

P(· | B) est une probabilité à part entière, donc : P(Ā | B) = 1 − P(A | B). Attention, en général P(A | B̄) ≠ 1 − P(A | B).

**Probabilités composées** (formule du produit)

```latex
P(A \cap B) = P(B)\,P(A \mid B) = P(A)\,P(B \mid A)
```

```latex
P(A_1 \cap A_2 \cap \dots \cap A_n) = P(A_1)\,P(A_2 \mid A_1)\,P(A_3 \mid A_1 \cap A_2) \cdots P(A_n \mid A_1 \cap \dots \cap A_{n-1})
```

**Système complet d'événements** : B₁, …, Bₙ deux à deux incompatibles et de réunion Ω (cas le plus courant : B et B̄).

**Formule des probabilités totales**

```latex
P(A) = \sum_{i=1}^{n} P(A \cap B_i) = \sum_{i=1}^{n} P(B_i)\,P(A \mid B_i)
```

```latex
P(A) = P(B)\,P(A \mid B) + P(\bar{B})\,P(A \mid \bar{B})
```

**Formule de Bayes** (« inverser » le conditionnement)

```latex
P(B \mid A) = \frac{P(A \mid B)\,P(B)}{P(A)}
```

```latex
P(B_k \mid A) = \frac{P(B_k)\,P(A \mid B_k)}{\sum_{i=1}^{n} P(B_i)\,P(A \mid B_i)}
```

**Indépendance**

```latex
A \text{ et } B \text{ indépendants} \iff P(A \cap B) = P(A)\,P(B) \iff P(A \mid B) = P(A) \ (\text{si } P(B) > 0)
```

- Si A et B sont indépendants, alors A et B̄, Ā et B, Ā et B̄ le sont aussi.
- Indépendance mutuelle de A, B, C : il faut P(A∩B) = P(A)P(B), P(A∩C) = P(A)P(C), P(B∩C) = P(B)P(C) **et** P(A∩B∩C) = P(A)P(B)P(C). Deux à deux ne suffit pas.
- Incompatibles ≠ indépendants : si P(A) > 0 et P(B) > 0, deux événements incompatibles ne sont jamais indépendants.

**Tableau de contingence** : passer des effectifs aux probabilités en divisant par le bon total.

| Ce qu'on cherche | Calcul à partir des effectifs |
| --- | --- |
| P(A ∩ B) | effectif de la case A∩B / effectif total |
| P(A) | total de la ligne (ou colonne) A / effectif total |
| P(A \| B) | effectif de la case A∩B / total de B (pas le total général) |

## Chapitre 3 (3.1 → 3.3) — Variables aléatoires discrètes

Une variable aléatoire discrète X associe un nombre à chaque issue ; sa loi est la liste des valeurs xᵢ ∈ X(Ω) avec leurs probabilités P(X = xᵢ).

**Loi de probabilité** — vérification obligatoire

```latex
P(X = x_i) \ge 0 \quad \text{et} \quad \sum_{x_i \in X(\Omega)} P(X = x_i) = 1
```

**Loi de Y = g(X)**

1. Trouver Y(Ω) = g(X(Ω)).
2. Pour chaque y, regrouper les x qui donnent g(x) = y.

```latex
P(Y = y) = \sum_{x \,:\, g(x) = y} P(X = x)
```

**Couple (X, Y)** — loi conjointe = tableau des P(X = x, Y = y)

```latex
P(X = x) = \sum_{y \in Y(\Omega)} P(X = x, Y = y) \qquad P(Y = y) = \sum_{x \in X(\Omega)} P(X = x, Y = y)
```

Les lois marginales se lisent en sommant les lignes et les colonnes du tableau. Elles ne suffisent pas à retrouver la loi conjointe.

**Indépendance de X et Y** — à vérifier pour **toutes** les cases

```latex
\forall (x, y),\ P(X = x, Y = y) = P(X = x)\,P(Y = y)
```

Une seule case qui ne marche pas (par exemple une case à 0 alors que les marginales sont non nulles) suffit à prouver la non-indépendance. Astuce : lignes proportionnelles ⇔ indépendance.

**Espérance**

```latex
E(X) = \sum_{x \in X(\Omega)} x\,P(X = x)
```

```latex
E(aX + b) = a\,E(X) + b \qquad E(\alpha X + \beta Y) = \alpha\,E(X) + \beta\,E(Y)
```

**Théorème du transfert** (pas besoin de la loi de g(X))

```latex
E(g(X)) = \sum_{x \in X(\Omega)} g(x)\,P(X = x) \qquad \text{ex. } E(X^2) = \sum x^2\,P(X = x)
```

**Variance et écart-type**

```latex
V(X) = E\big((X - E(X))^2\big) = E(X^2) - E(X)^2 \qquad \sigma(X) = \sqrt{V(X)}
```

```latex
V(aX + b) = a^2\,V(X) \qquad V(X) \ge 0
```

```latex
X, Y \text{ indépendantes} \Rightarrow V(X + Y) = V(X) + V(Y)
```

La réciproque est fausse. Sans indépendance, V(X + Y) ≠ V(X) + V(Y) en général.

**Variable centrée réduite**

```latex
Z = \frac{X - E(X)}{\sigma(X)} \quad \Rightarrow \quad E(Z) = 0,\ V(Z) = 1
```

## Chapitre 3.4 — Covariance et corrélation

Au programme du CE : les exercices 3.8 à 3.12 portent dessus.

**E(XY) avec le transfert** (somme sur toutes les cases du tableau conjoint)

```latex
E(XY) = \sum_{x}\sum_{y} x\,y\,P(X = x, Y = y)
```

**Covariance**

```latex
\operatorname{Cov}(X, Y) = E\big((X - E(X))(Y - E(Y))\big) = E(XY) - E(X)\,E(Y)
```

```latex
\operatorname{Cov}(X, X) = V(X) \qquad \operatorname{Cov}(aX + b,\ cY + d) = ac\,\operatorname{Cov}(X, Y)
```

**Variance d'une somme** (toujours vraie)

```latex
V(X + Y) = V(X) + V(Y) + 2\,\operatorname{Cov}(X, Y)
```

**Indépendance**

```latex
X, Y \text{ indépendantes} \Rightarrow E(XY) = E(X)\,E(Y) \Rightarrow \operatorname{Cov}(X, Y) = 0
```

Réciproque fausse : Cov(X, Y) = 0 ne prouve pas l'indépendance.

**Coefficient de corrélation**

```latex
\rho(X, Y) = \frac{\operatorname{Cov}(X, Y)}{\sigma(X)\,\sigma(Y)} \in [-1, 1]
```

|ρ| = 1 ⇔ relation affine Y = aX + b ; ρ proche de 0 = pas de lien linéaire.

## Chapitre 3.5 — Lois usuelles

Au programme du CE via les exercices 3.13 à 3.15 (binomiale et Poisson). Savoir reconnaître la loi à partir de l'énoncé est la moitié du travail.

| Loi | Ce que compte X | X(Ω) | P(X = k) | E(X) | V(X) |
| --- | --- | --- | --- | --- | --- |
| Uniforme U(\[\[1,n\]\]) | une valeur équiprobable parmi n | \[\[1,n\]\] | 1/n | (n+1)/2 | (n²−1)/12 |
| Bernoulli B(p) | succès (1) ou échec (0) d'un essai | {0,1} | P(1) = p, P(0) = 1−p | p | p(1−p) |
| Binomiale B(n,p) | nombre de succès sur n essais indépendants | \[\[0,n\]\] | C(n,k) pᵏ (1−p)ⁿ⁻ᵏ | np | np(1−p) |
| Binomiale négative BN(r,p) | nombre d'essais pour obtenir r succès | \[\[r,+∞\[\[ | C(k−1,r−1) pʳ (1−p)ᵏ⁻ʳ | r/p | r(1−p)/p² |
| Poisson P(λ) | événements rares sur une période | ℕ | e⁻λ λᵏ / k! | λ | λ |

Pour Poisson, la formule est :

```latex
P(X = k) = e^{-\lambda}\,\frac{\lambda^k}{k!}, \qquad E(X) = V(X) = \lambda
```

BN(1, p) s'appelle la loi géométrique : P(X = k) = (1−p)ᵏ⁻¹ p, E(X) = 1/p.

**Poisson comme approximation de la binomiale** (n grand, p petit, np = λ)

```latex
\binom{n}{k}\,p^k (1-p)^{n-k} \approx e^{-\lambda}\,\frac{\lambda^k}{k!} \quad \text{avec } \lambda = np
```

Somme de deux Poisson indépendantes : X ∼ P(λ) et Y ∼ P(θ) ⇒ X + Y ∼ P(λ + θ).

**Quelle loi choisir ?**

1. Nombre de succès sur un nombre **fixé** d'essais indépendants → binomiale.
2. Nombre d'essais **jusqu'au** r-ième succès → binomiale négative.
3. Nombre d'événements rares dans une période ou une population, avec une moyenne connue → Poisson.

**Réflexes pour les « plus de / moins de »**

| Énoncé | Traduction | Calcul |
| --- | --- | --- |
| au plus 2 | X ≤ 2 | P(0) + P(1) + P(2) |
| moins de 2 | X ≤ 1 | P(0) + P(1) |
| plus de 2 | X ≥ 3 | 1 − P(X ≤ 2) |
| au moins 1 | X ≥ 1 | 1 − P(X = 0) |

## Pièges classiques et méthode pour le CE

**Réflexes de méthode**

1. Nommer les événements (« A : la pièce est défectueuse ») avant tout calcul.
2. Traduire chaque donnée de l'énoncé : « parmi les A, 30 % sont B » = P(B | A) = 0,3, pas P(A ∩ B).
3. Arbre ou tableau dès qu'il y a deux étapes ou deux critères.
4. On cherche P(cause | effet) → Bayes. On cherche P(effet) avec plusieurs causes → probabilités totales.
5. Pour une VA : donner X(Ω), puis la loi, puis vérifier que la somme fait 1.
6. Pour V(X) : calculer E(X), puis E(X²) par transfert, puis E(X²) − E(X)².

**Pièges fréquents**

| Piège | Bonne version |
| --- | --- |
| Confondre effectif et probabilité | probabilité = effectif / le bon total |
| P(A \| B) = P(B \| A) | faux en général → utiliser Bayes |
| P(A \| B̄) = 1 − P(A \| B) | faux → c'est P(Ā \| B) = 1 − P(A \| B) |
| Incompatibles ⇒ indépendants | faux (sauf probabilité nulle) |
| P(A ∪ B) = P(A) + P(B) | seulement si A ∩ B = ∅ |
| V(aX + b) = aV(X) + b | V(aX + b) = a²V(X) |
| V(X − Y) = V(X) − V(Y) | si indépendantes : V(X − Y) = V(X) + V(Y) |
| E(X²) = E(X)² | faux → théorème du transfert |
| Indépendance vérifiée sur une seule case | il faut toutes les cases |
| Cov(X, Y) = 0 ⇒ indépendantes | faux, seulement le sens direct |
