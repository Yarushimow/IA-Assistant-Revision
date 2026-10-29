# Fiche SP301 – Force et champ électrostatiques

Oct 4, 2026 · @Yoan

Interro de 25 min (15 % de la note) : force et champ électrostatiques, du début du chapitre 1 jusqu'au condensateur plan. Le potentiel n'est pas au programme.

## Constantes et ordres de grandeur

| Grandeur | Valeur |
| --- | --- |
| Charge élémentaire e | 1,602 × 10⁻¹⁹ C |
| Constante de Coulomb kₑ = 1/(4πε₀) | ≈ 9 × 10⁹ SI (N·m²/C²) |
| Charge de l'électron | −e |
| Charge du proton | +e |
| 1 eV | 1,6 × 10⁻¹⁹ J |

Atome d'hydrogène (r = 53 pm) : force électrique ≈ 8,2 × 10⁻⁸ N, force gravitationnelle ≈ 3,6 × 10⁻⁴⁷ N. La gravité est donc négligeable à l'échelle des particules.

## Loi de Coulomb

Deux charges s'attirent ou se repoussent avec une force proportionnelle au produit des charges et inversement proportionnelle au carré de la distance. Cette force est portée par la droite qui joint les deux charges.

```latex
\vec F_{12} = k_e \frac{q_1 q_2}{r^2}\,\vec u_{12} = -\vec F_{21} \qquad \vec u_{12} = \frac{\overrightarrow{M_1M_2}}{M_1M_2}
```

- F₁₂ est la force exercée **par q₁ sur q₂**. Elle s'applique en M₂.
- u₁₂ est unitaire et va **de la source (q₁) vers la charge qui subit (q₂)**.
- q₁q₂ > 0 : force répulsive. q₁q₂ < 0 : force attractive.
- Norme : F = kₑ |q₁q₂| / r², en newtons.
- 3ᵉ loi de Newton : F₂₁ = −F₁₂, donc même norme et sens opposé.
- Si r est multiplié par 2, la force est divisée par 4.

&#91;embedded content: Loi de Coulomb · les cas selon le signe des charges\]

Les deux forces ont toujours la même norme et des sens opposés, quelles que soient les charges.

### Les 4 cas de signes

| q₁ | q₂ | Signe de q₁q₂ | Type | Sens de F₁₂ (sur q₂) |
| --- | --- | --- | --- | --- |
| > 0 | > 0 | > 0 | répulsion | même sens que u₁₂ (q₂ s'éloigne de q₁) |
| < 0 | < 0 | > 0 | répulsion | même sens que u₁₂ |
| > 0 | < 0 | < 0 | attraction | sens opposé à u₁₂ (q₂ va vers q₁) |
| < 0 | > 0 | < 0 | attraction | sens opposé à u₁₂ |

Règle rapide : on garde le signe de q₁q₂ dans la formule. Si le coefficient devant u₁₂ est positif, la force va dans le sens de u₁₂. S'il est négatif, elle va dans l'autre sens.

## Principe de superposition

La force totale sur une charge q est la **somme vectorielle** des forces créées par chaque autre charge, prise séparément.

```latex
\vec F(M) = \sum_{k=1}^{N} k_e \frac{q_k\, q}{r_k^2}\,\vec u_k = \sum_{k=1}^{N} k_e \frac{q_k\, q}{r_k^3}\,\overrightarrow{P_kM}
```

Méthode type :

1. Faire un schéma, placer un repère et le point O (souvent le milieu ou le centre de symétrie).
2. Pour chaque charge source, écrire le vecteur unitaire de la source vers le point étudié.
3. Écrire chaque force avec son signe : kₑ qₖq / rₖ² · uₖ.
4. Additionner les vecteurs. Utiliser la symétrie : les composantes perpendiculaires à l'axe de symétrie s'annulent.
5. Donner le résultat dans la base, puis la norme, puis l'application numérique.

Astuce : avec u = PM / r, on peut écrire kₑ q / r³ · PM. Par exemple, si O est le milieu de AB, on a AC + BC = 2·OC.

Exemple du cours (triangle équilatéral de côté d, q₁ = q₂ = −e en A et B, q = 2e en C) :

```latex
\vec F_C = -2\sqrt{3}\,k_e \frac{e^2}{d^2}\,\vec e_z \qquad OC = d\cos 30^\circ = \frac{\sqrt3}{2}d
```

La force est attractive, dirigée de C vers O.

## Champ électrique

Une charge q placée en O crée en tout point M un champ dirigé selon la droite OM. Il s'exprime en **N/C ou V/m**.

```latex
\vec E_O(M) = k_e \frac{q}{r^2}\,\vec u \qquad \vec u = \frac{\overrightarrow{OM}}{r}
```

- q > 0 : champ centrifuge (il s'éloigne de la charge).
- q < 0 : champ centripète (il pointe vers la charge).
- Le champ ne dépend que de la charge source, pas de la charge qu'on place en M.
- Superposition : E(M) = E₁(M) + … + Eₙ(M), comme pour les forces.

Lien entre force et champ : une charge Q placée en M subit

```latex
\vec F(M) = Q\,\vec E(M)
```

| Signe de Q | Sens de F par rapport à E |
| --- | --- |
| Q > 0 (proton) | même sens |
| Q < 0 (électron) | sens opposé |

Dans les deux cas, F et E ont la même direction.

&#91;embedded content: Champ d'une charge ponctuelle et force F = QE · les cas de signes\]

En bleu le champ E, en orange la force F.

### Les 4 combinaisons source / charge placée en M

| Source q (en O) | Charge Q (en M) | Sens de E en M | Sens de F sur Q | Bilan |
| --- | --- | --- | --- | --- |
| q > 0 | Q > 0 | de O vers M | de O vers M | répulsion |
| q > 0 | Q < 0 | de O vers M | de M vers O | attraction |
| q < 0 | Q > 0 | de M vers O | de M vers O | attraction |
| q < 0 | Q < 0 | de M vers O | de O vers M | répulsion |

On retrouve exactement la loi de Coulomb : F = Q·E = kₑ qQ / r² · u.

Méthode en deux temps : (1) le signe de la **source** donne le sens de E, (2) le signe de la **charge qui subit** dit si F va dans le sens de E ou à l'opposé.

## Dipôle électrostatique

On place −q en A (x = −a) et +q en B (x = +a), avec q > 0, AB = 2a et O le milieu de AB. Le champ du dipôle est parallèle à AB et va du + vers le −.

Champ au milieu O : les deux contributions pointent vers A et s'ajoutent.

```latex
\vec E(O) = -2k_e \frac{q}{a^2}\,\vec e_x
```

Champ sur la médiatrice, avec α = angle OMB et d = AM = BM = a / sin α :

```latex
\vec E(M) = k_e\frac{q}{d^3}\,\overrightarrow{BA} = -2k_e \frac{q}{a^2}\sin^3\alpha\;\vec e_x
```

Pour un point M en y = 2a, sin α = 1/√5. La force sur une charge Q placée en M vaut alors F = Q·E(M).

Piège : les composantes selon e\_y s'annulent par symétrie. Il ne reste que la composante selon e\_x.

&#91;embedded content: Dipôle · champ en O et en un point M de la médiatrice\]

En gris les deux contributions, en bleu le champ total. Les composantes verticales se compensent, il ne reste que −eₓ.

### Cas à savoir traiter

| Situation | Résultat |
| --- | --- |
| M confondu avec O (α = 90°, sin α = 1) | on retrouve E(O) = −2kₑq/a² · eₓ |
| M très loin sur la médiatrice (α → 0) | sin³α → 0, donc E → 0 |
| Charges inversées (+q en A, −q en B) | tous les champs changent de sens : E(O) = +2kₑq/a² · eₓ |
| Deux charges identiques +q en A et B | en O les contributions s'annulent : E(O) = 0 ; sur la médiatrice, E est porté par e\_y |
| Charge Q > 0 placée en M | F = Q·E(M), même sens que E (vers −eₓ) |
| Charge Q < 0 placée en M | F = Q·E(M), sens opposé (vers +eₓ) |

## Lignes de champ

Une ligne de champ est une courbe orientée, tangente au champ E en chaque point et de même sens que lui.

| Distribution | Allure des lignes |
| --- | --- |
| Charge seule q > 0 | droites radiales, orientées vers l'extérieur |
| Charge seule q < 0 | droites radiales, orientées vers la charge |
| Dipôle | boucles qui partent du + et arrivent sur le − |
| Condensateur plan | droites parallèles, perpendiculaires aux armatures, du + vers le − |

Deux lignes de champ ne se croisent jamais. Plus elles sont serrées, plus le champ est intense.

## Condensateur plan

Il est formé de deux armatures de surface S, séparées d'une distance d petite devant leurs dimensions. Sous une tension U, elles portent +Q et −Q. Le champ entre elles est **uniforme** : perpendiculaire aux armatures, dirigé du + vers le −, de norme U/d.

```latex
\|\vec E\| = \frac{U}{d} \qquad \vec F = q\,\vec E \ \text{(constante entre les armatures)}
```

Orienter eₓ avec soin. Si l'armature + est à droite, E = −U/d · eₓ.

&#91;embedded content: Condensateur plan · champ uniforme et force selon le signe\]

En bleu le champ, en orange la force. La force a la même norme partout entre les armatures.

Théorème de l'énergie cinétique : la force est constante, donc son travail est un simple produit scalaire.

```latex
E_{c,f} - E_{c,i} = W(\vec F) = \vec F\cdot\overrightarrow{AB}
```

Exemple du cours : un électron est lâché sans vitesse au centre (d = 2a). Il va vers l'armature + et parcourt a.

```latex
E_{c,f} = \frac{eU}{2a}\,\vec e_x\cdot a\,\vec e_x = \frac{eU}{2}
```

Sous 2 V, il gagne donc 1 eV = 1,6 × 10⁻¹⁹ J. Une particule qui traverse tout le condensateur gagne eU.

### Tous les cas du condensateur

| Particule | Charge | Force F = qE | Lâchée sans vitesse | Eₖ gagnée sur toute la traversée |
| --- | --- | --- | --- | --- |
| Proton, ion positif | q = +e > 0 | sens de E (vers −) | part vers l'armature − | eU |
| Électron | q = −e < 0 | opposée à E (vers +) | part vers l'armature + | eU |
| Ion de charge q quelconque | q | q·E | vers − si q > 0, vers + si q < 0 | \|q\|·U |
| Particule neutre (neutron) | 0 | nulle | ne bouge pas | 0 |

Selon le point de départ et le trajet :

| Situation | Travail W = F·déplacement | Effet |
| --- | --- | --- |
| Toute la traversée (distance d), dans le sens de F | +\|q\|U | accélération, Eₖ = \|q\|U |
| Départ au milieu, jusqu'à une armature (distance d/2) | +\|q\|U/2 | Eₖ = \|q\|U/2 (exemple du cours : eU/2) |
| Particule lancée contre la force | négatif | elle ralentit ; elle s'arrête si Eₖ initiale < \|q\|U |
| Déplacement parallèle aux armatures (perpendiculaire à F) | 0 | Eₖ ne change pas |

W est positif si F et le déplacement sont dans le même sens, négatif s'ils sont opposés.

Vitesse finale (partie de l'arrêt) : v = √(2E\_c / m).

Poids : il est négligeable devant la force électrique. Pour un proton dans 10⁴ V/m, le rapport vaut environ 10¹¹. Il faut le justifier en une phrase.

## Pièges et checklist le jour J

Les erreurs qui coûtent le plus de points :

- Oublier le **signe de la charge** dans la formule vectorielle (un électron vaut −e).
- Inverser le sens du vecteur unitaire. Il va toujours de la source vers le point étudié.
- Mélanger r² (avec le vecteur unitaire u) et r³ (avec le vecteur PM non normalisé).
- Additionner des normes au lieu de vecteurs.
- Oublier les conversions : 1 pm = 10⁻¹² m, 1 nm = 10⁻⁹ m, 1 µm = 10⁻⁶ m, 1 mm = 10⁻³ m.
- Valeurs utiles : cos 30° = √3/2, sin 30° = 1/2, cos 45° = √2/2.

Avant de rendre :

- [ ] Schéma fait, avec le repère et les vecteurs dessinés
- [ ] Résultat vectoriel donné dans la base (eₓ, e\_y, e\_z)
- [ ] Norme et application numérique avec l'unité
- [ ] Poids négligé et justifié si nécessaire
- [ ] Ordre de grandeur cohérent (forces sur des particules : très petites)
