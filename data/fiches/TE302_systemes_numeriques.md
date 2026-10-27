# TE302 – Systèmes numériques

Fiche CE TE302

TE302 · Systèmes numériques · EFREI P2

# Fiche de révision du CE du samedi 10 octobre

Tout le CTD et les TP jusqu'aux compteurs asynchrones inclus : bascules, registres, compteurs asynchrones. Les compteurs synchrones (synthèse avec Karnaugh) ne sont pas au programme de ce CE.

**QCM sur le cours**Une seule bonne réponse en général. Définitions, tables, temps.

**Exercice de compréhension**Les fondamentaux vus en CTD et en TP.

**Exercice d'application**Lire un schéma et une datasheet, tracer des chronogrammes. Prends une règle.

Documents interdits · calculatrice utile mais pas indispensable

## Les bascules

CTD 1 · TP1

**Combinatoire** : les sorties ne dépendent que des entrées. **Séquentiel** : les sorties dépendent aussi de l'état précédent (bouclage, mémoire). La bascule est la brique de base du séquentiel : elle mémorise 1 bit.

### Les familles

* **Asynchrone** (RS) : réagit dès que les entrées changent.
* **Synchrone sur niveau** (latch, RST, D latch) : réagit tant que l'horloge est au niveau actif.
* **Synchrone sur front** (flip-flop D, JK) : réagit uniquement au front actif.

Lire le symbole

* Triangle sur CLK : déclenchement sur **front montant** (↑).
* Rond + triangle : déclenchement sur **front descendant** (↓).
* Rond devant une entrée (~CLR, ~PR) : entrée **active au niveau bas**.

### Bascule RS asynchrone

**Avec des NOR** : entrées actives à 1.

| S | R | Q | Fonction |
| --- | --- | --- | --- |
| 0 | 0 | Q | Mémoire |
| 1 | 0 | 1 | Set |
| 0 | 1 | 0 | Reset |
| 1 | 1 | 0 (Q̄=0) | Non utilisé |

**Avec des NAND** (TP1) : entrées actives à 0.

| S | R | Q | Fonction |
| --- | --- | --- | --- |
| 1 | 1 | Q | Mémoire |
| 0 | 1 | 1 | Set |
| 1 | 0 | 0 | Reset |
| 0 | 0 | 1 (Q̄=1) | Non utilisé |

Piège

L'état « non utilisé » donne Q = Q̄, ce qui contredit la définition. En NOR c'est S = R = 1, en NAND c'est S = R = 0. Le cours écrit la table NAND dans l'ordre R, S : regarde toujours sur le schéma quelle porte sort Q.

### Bascule D

* **D latch (sur niveau)** : clk = 1 → Q recopie D en continu ; clk = 0 → mémoire.
* **D flip-flop (sur front)** : au front actif, Q prend la valeur de D *juste avant* le front. Le reste du temps, mémoire.

Q(t + tp) = D(t) au front actif ; sinon Q garde sa valeur

| CLK | D | Q(t+Δt) | Fonction (TP1) |
| --- | --- | --- | --- |
| pas de front actif | X | Q(t) | M (maintien) |
| front actif | 0 | 0 | C (copie) |
| front actif | 1 | 1 | C (copie) |

### Bascule JK

**Table de vérité** (au front actif)

| J | K | Q(t+Δt) | Fonction |
| --- | --- | --- | --- |
| 0 | 0 | Q(t) | M (mémoire) |
| 0 | 1 | 0 | R (reset) |
| 1 | 0 | 1 | S (set) |
| 1 | 1 | Q̄(t) | T (toggle) |

**Table de transitions** (X = 0 ou 1)

| Q(t) | Q(t+1) | J | K |
| --- | --- | --- | --- |
| 0 | 0 | 0 | X |
| 0 | 1 | 1 | X |
| 1 | 0 | X | 1 |
| 1 | 1 | X | 0 |

Moyen mnémotechnique : **J** comme « jump » (met à 1), **K** comme « kill » (met à 0). Les deux à 1 : la sortie s'inverse.

### Entrées asynchrones PRE et CLR

* **Prioritaires** sur l'horloge et sur les entrées D, J, K.
* **Indépendantes** de l'horloge : elles agissent tout de suite, sans attendre de front.
* **Actives au niveau bas** : ~PR = 0 force Q = 1 (mise à un, MAU), ~CLR = 0 force Q = 0 (remise à zéro, RAZ).
* Pour les rendre inactives, on les relie à **1 (VCC)**. Les deux à 0 en même temps : interdit.

### Les trois temps d'une bascule

| Nom | Symbole | Définition |
| --- | --- | --- |
| Pré-positionnement (setup) | tpp | Durée minimale pendant laquelle D doit être stable **avant** le front actif. |
| Maintien (hold) | tm | Durée minimale pendant laquelle D doit rester stable **après** le front actif. |
| Propagation | tp ou Δt | Retard entre le front actif et le moment où Q est valide. |

En TP1, on a mesuré ΔtLH (sortie qui monte) et ΔtHL (sortie qui descend), de l'ordre de la dizaine de nanosecondes. La fréquence d'horloge maximale est de l'ordre de fmax ≈ 1 / tpmax, avec le tp le plus défavorable.

### Montage diviseur de fréquence (toggle)

Bascule D avec D = Q̄, ou JK avec J = K = 1 : la sortie s'inverse à chaque front actif. Sa fréquence vaut **fH / 2**.

D flip-flop sur front montant, D = Q̄, CI Q = 0. Q change un tp après chaque front ↑ : période doublée.

## Les registres

CTD 2 · TP2

Un registre de longueur N = **N bascules D sur la même horloge**. Il mémorise un mot de N bits.

Quatre fonctions : **transfert parallèle** (N bits disponibles en même temps), **mémorisation**, **transfert série** (bit par bit, par décalage), **rotation** (sortie série rebouclée sur l'entrée série).

### Décalages et rotations

| Fonction | Câblage | Entrée série | Sortie série |
| --- | --- | --- | --- |
| Décalage à droite | Di = Qi−1 | D0 = E | Q(N−1) |
| Décalage à gauche | Di = Qi+1 | D(N−1) = E | Q0 |
| Rotation à droite | Di = Qi−1 | D0 = Q(N−1) | Q(N−1) |
| Rotation à gauche | Di = Qi+1 | D(N−1) = Q0 | Q0 |

Décalage à droite sur 4 bits, contenu initial D0 D1 D2 D3, entrée E :

| Front | Q0 | Q1 | Q2 | Q3 | Sortie |
| --- | --- | --- | --- | --- | --- |
| Initial | D0 | D1 | D2 | D3 | D3 |
| 1 | E | D0 | D1 | D2 | D2 |
| 2 | E | E | D0 | D1 | D1 |
| 4 | E | E | E | E | E |

### Architectures

* **Entrée série / sorties parallèles** : le mot est disponible sur les sorties après **N fronts**.
* **Entrées parallèles / sorties parallèles** : les Di sont copiées sur les Qi **au même front**, après tp (si tpp et tm sont respectés).
* **Chargement série/parallèle** : un multiplexeur 2→1 devant chaque D choisit entre la donnée parallèle et la sortie de la voisine.

MUX 2→1 : s = ā·e0 + a·e1 (a = 0 → e0, a = 1 → e1)

Piège

La convention de la commande change selon le document. Dans le cours, S/P = 1 charge les Di (parallèle). Dans le TP2, L = 0 chargeait en parallèle et L = 1 décalait. Lis toujours le schéma ou la table fournie.

### Registre bidirectionnel

Commande de sens K (ou R en TP2) : décalage à droite pour K = 1, à gauche pour K = 0. Chaque entrée s'écrit avec un MUX d'adresse K :

Di = K·Q(i−1) + K̄·Q(i+1)
D0 = K·DS + K̄·Q1 D(N−1) = K·Q(N−2) + K̄·DS
QS = K·Q(N−1) + K̄·Q0

Il faut **N + 1 MUX** : N pour les entrées D, plus 1 pour la sortie série QS qui change aussi selon le sens. En TP2 sur 4 bits : 5 MUX. Pour l'exercice 2 du CTD sur 6 bits (74HC174) : 7 MUX.

### Circuits intégrés à connaître

| Circuit | Ce qu'il contient | À retenir |
| --- | --- | --- |
| 7474 | 2 bascules D, front ↑ | ~PR et ~CLR actives au niveau bas |
| 74HC107 | 2 bascules JK, front ↓ | ~CLR active au niveau bas |
| 74HC174 | 6 bascules D, CLK commune | ~CLR commune, active au niveau bas |
| 74HC164 | Registre 8 bits, décalage QA → QH | Donnée série DS = A·B (une entrée sert de validation) |
| 74HC194 | Registre universel 4 bits | ~MR actif bas, DSR et DSL, modes par S1 S0 |

Modes du 74HC194 : S1S0 = 00 maintien, 01 décalage à droite (entrée DSR, sortie Q3), 10 décalage à gauche (entrée DSL, sortie Q0), 11 chargement parallèle. Le jour J, vérifie sur la table fournie.

### Compteurs construits avec un registre

* **Compteur en anneau** : un seul 1 qui tourne. **N états** avec N bascules. Exemple de l'annale 2023 : D0 = NOR(Q0, Q1), CI Q0Q1Q2 = 100, séquence **1, 2, 4**, synchrone.
* **Compteur Johnson** : on réinjecte l'inverse de la dernière sortie, DS = Q̄(N−1). **2N états** avec N bascules, un seul bit change à chaque front.

| Front | Q0 Q1 Q2 Q3 |
| --- | --- |
| CI | 0 0 0 0 |
| 1 → 4 | 1 0 0 0 · 1 1 0 0 · 1 1 1 0 · 1 1 1 1 |
| 5 → 8 | 0 1 1 1 · 0 0 1 1 · 0 0 0 1 · 0 0 0 0 |

Johnson 4 bits : 8 états, chaque sortie est un créneau de période 8 fronts.

### Registres de l'ATmega328P

Recherche en autonomie du CTD 2 (exercices 5 à 7) : à connaître si ça a été corrigé en séance.

* 32 registres de travail de 8 bits (R0 à R31). Paires : X = R27:R26, Y = R29:R28, Z = R31:R30.
* SREG : registre d'état. Le bit **C** (Carry) reçoit la retenue, ou le bit qui sort lors d'un décalage.

| Instruction | Effet | R18 = 10110110 devient | C |
| --- | --- | --- | --- |
| LSL | Décalage à gauche, 0 entre à droite, bit 7 → C | 01101100 | 1 |
| LSR | Décalage à droite, 0 entre à gauche, bit 0 → C | 01011011 | 0 |
| ASR | Décalage à droite, le bit 7 (signe) est conservé | 11011011 | 0 |
| ROL | Rotation à gauche à travers C (C → bit 0, bit 7 → C) | 0110110C | 1 |
| ROR | Rotation à droite à travers C (C → bit 7, bit 0 → C) | C1011011 | 0 |

ROL et ROR tournent sur **9 bits** (8 bits + C) : ce n'est pas une rotation circulaire classique sur 8 bits. LSL multiplie par 2, LSR divise par 2 un nombre non signé, ASR divise par 2 un nombre signé.

## Les compteurs asynchrones

CTD 3 · TD2

* Un compteur à **N bascules** a au plus **2N états**, de 0 à 2N − 1.
* **Cycle complet** : les 2N états, compteur modulo 2N (noté #2N). **Cycle incomplet** : M états avec M < 2N, compteur modulo M.
* Nombre de bascules : le plus petit N tel que la plus grande valeur de la séquence s'écrive sur N bits. Séquence [3, 4, 5, 9] : 9 = 1001, donc **4 bascules**.

Asynchrone ou synchrone

**Asynchrone** (série, à propagation) : seule la bascule Q0 reçoit l'horloge H. Chaque bascule suivante est déclenchée par la sortie de la précédente, CLKi = Qi−1 ou Q̄i−1. Les retards s'additionnent.

**Synchrone** (parallèle) : toutes les bascules reçoivent la même horloge, sur le même front.

### Le montage de base

Chaque bascule est en mode toggle (D = Q̄ ou J = K = 1), donc chacune divise par 2 la fréquence de son horloge :

f(Qi) = fH / 2(i+1) ex. fH = 1 MHz → Q0 : 500 kHz, Q1 : 250 kHz, Q2 : 125 kHz

### Compteur ou décompteur ?

Pour compter, la bascule i doit basculer quand Q(i−1) passe de **1 à 0** (c'est la retenue : 011 → 100). Il faut donc qu'un front actif de CLKi tombe à ce moment.

| Front actif des bascules | CLKi = Qi−1 | CLKi = Q̄i−1 |
| --- | --- | --- |
| Front descendant ↓ (JK du cours, 74HC107) | Compteur | Décompteur |
| Front montant ↑ (D du cours, 7474) | Décompteur | Compteur |

Piège

Ne retiens pas « Q = compteur » tout seul : ça dépend du front. Vérifie toujours sur les deux premiers fronts du chronogramme : si on passe de 0 à 1, c'est un compteur ; si on passe de 0 à 7 (ou 15), c'est un décompteur.

Compteur asynchrone #8, bascules JK sur front ↓, J = K = 1, CLKi = Qi−1, CI 000. Chronogramme théorique (tp négligé). Q0 est le bit de poids faible.

Décompteur avec bascules D sur front ↑ et CLKi = Qi−1, CI 000 : séquence 0, 7, 6, 5, 4, 3, 2, 1, 0… Annale 2023 : décompteur **modulo 4** à 2 bascules, CI Q0 = Q1 = 1, séquence **3, 2, 1, 0**, non synchrone.

### Le temps de propagation et ses effets

Au front de H, Q0 change après tp. Si Q0 fait basculer Q1, Q1 change après 2tp, puis Q2 après 3tp, etc. Pire cas : **tous** les bits changent (7 → 0 sur 3 bits).

Retard max = N·tp Condition : N·tp < TH → fmax = 1 / (N·tp)

Exemple du TD avec tp = 8 ns : 3 bascules → 24 ns → fmax ≈ 41,7 MHz. Avec 4 bascules → 32 ns → fmax ≈ 31,2 MHz.

Zoom sur le passage de 3 à 4 en tenant compte de tp. Le compteur passe brièvement par 2 puis 0 avant d'atteindre 4 : ce sont des états transitoires (aléas, glitchs), en couleur.

Mêmes effets ailleurs : 7 → 6 → 4 → 0 ; 1 → 0 → 2. Plus il y a de bascules, plus les retards cumulés sont grands.

**Définition à savoir réciter** : le temps de propagation d'une bascule synchrone est le retard entre le front actif de son horloge et le moment où sa sortie Q est valide.

### Compteur modulo M par remise à zéro

1. Écrire M en binaire.
2. Prendre les bits à **1** de M et les envoyer dans une **NAND**.
3. Relier la sortie de la NAND aux ~CLR de toutes les bascules (actives au niveau bas).

| Modulo | M en binaire | Bascules | Détection |
| --- | --- | --- | --- |
| 5 | 101 | 3 | ~CLR = NAND(Q2, Q0) |
| 6 | 110 | 3 | ~CLR = NAND(Q2, Q1) |
| 10 | 1010 | 4 | ~CLR = NAND(Q3, Q1) |
| 12 | 1100 | 4 | ~CLR = NAND(Q3, Q2) |

Piège

On détecte **M** (5 pour un modulo 5), pas M − 1 : la remise à zéro est asynchrone, elle agit dès que l'état M apparaît, sans attendre le front suivant. On ne met dans la NAND que les bits à 1 : les états supérieurs à M ne sont jamais atteints.

Compteur modulo 5 : séquence 0, 1, 2, 3, 4, 0… L'état 5 n'existe que le temps que la NAND réagisse et que les bascules se remettent à zéro (fine bande colorée après le front 5).

**Durée de l'état 5** : théoriquement nulle. En pratique, environ tp de la NAND + temps de remise à zéro, soit quelques nanosecondes. C'est un état parasite (glitch) visible à l'analyseur logique. Risque : si une bascule se remet à zéro avant les autres, la NAND repasse à 1 trop tôt et la RAZ peut être incomplète.

## Méthode pour l'exercice d'application

Lecture de schéma · chronogrammes

1. **Identifier chaque bascule** : type (D, JK), front actif (triangle seul ou rond + triangle), état de PRE et CLR (reliés à 1 = inactifs).
2. **Écrire l'équation de chaque entrée** : Di, Ji, Ki, et surtout **qui pilote CLKi** (H pour tout le monde = synchrone ; Qi−1 ou Q̄i−1 = asynchrone).
3. **Noter les conditions initiales** (CI) à gauche du chronogramme.
4. **Tracer les traits verticaux à la règle** sur chaque front actif de H, et les numéroter.
5. **Calculer l'état suivant avec les valeurs juste avant le front**. Pour un asynchrone, une bascule ne change que sur un front actif de *sa propre* horloge (la sortie précédente).
6. **Annoter les fonctions** si demandé : M, C pour une D ; M, S, R, T pour une JK ; S, R, M, NU pour une RS.
7. **Si tp est demandé**, décaler chaque transition : Q0 à +tp, Q1 à +2tp… et repérer les états transitoires.
8. **Conclure** : lire la séquence en décimal avec **Q0 = poids faible**, donner la fonction (compteur, décompteur, registre à décalage), le modulo, synchrone ou non.

Vérifications rapides

* Chaque Qi d'un compteur à cycle complet est un créneau de période 2i+1 × TH.
* Un compteur ne doit jamais sauter de valeur entre deux fronts (hors états transitoires).
* Pour un registre à décalage, chaque sortie recopie la précédente avec un front de retard.

## Ce qu'on a vu en TP

Multisim · TP1 et TP2

TP1 · Bascules

* **RS en NAND** (74HC) en sous-circuit, testée avec le Word Generator sur la séquence {1, 3, 2, 3, 0} en mode BURST, puis annotée S, R, M, NU sur GRAPHER.
* **D avec le 7474** (PR et CLR actives au niveau bas), XWG à 1 kHz et analyseur à 10 kHz, annotations M et C.
* **Temps de propagation** : XWG à 10 MHz, analyseur à 100 MHz, mesure de ΔtLH et ΔtHL, d'où un ordre de grandeur de fmax.
* **Exemple d'application** en mode STEP, puis à 50 MHz : la période (20 ns) devient comparable aux temps de propagation et la séquence affichée n'est plus correcte.
* **JK avec le 74HC107** (front ↓, CLR active au niveau bas), annotations M, S, R, T.

TP2 · Registres

* **MUX 2→1 en 4 NAND** : une NAND en inverseur donne ā, puis s = ā·e0 + a·e1. Avec a = 0, s recopie e0 ; avec a = 1, s recopie e1.
* **Registre 3 bits S/P** (3 MUX + 3 bascules D du TP1, L commune aux 3 MUX). Séquence de test avec EPi = 1 : au front 1 (L = 0) chargement parallèle, Q0Q1Q2 = 111 ; ensuite L = 1, ES = 0 : 011, 001, 000 ; ES = 1 : 100, 110, 111 ; ES = 0 : 011.
* **Registre bidirectionnel 4 bits** : 74HC174 + sous-circuit « Combinatoire » de 5 MUX d'adresse R, ~CLR relié à VCC, horloge à 1 Hz. R = 1 : les sondes s'allument de Q0 vers Q3 ; R = 0 : de Q3 vers Q0.
* **74HC164 en compteur Johnson** : A et B reliés à une NAND dont les deux entrées sont sur QH, donc DS = Q̄H. Partant de 0 : 11111111 au 8e front, 00000000 au 16e. 16 états avec 8 bascules, l'horloge est divisée par 16.

### Les questions du prof, avec la réponse

| Question | Réponse |
| --- | --- |
| Pourquoi des MUX et pas des fils ? | Un fil fixe un seul sens de décalage. Le MUX choisit la source de chaque bascule selon R. |
| Pourquoi ~CLR à VCC ? | Elle est active au niveau bas : à 0, le registre resterait bloqué à 0000. |
| Pourquoi 5 MUX et pas 4 ? | La sortie série change aussi selon le sens (Q3 à droite, Q0 à gauche). |
| À quoi sert un Johnson ? | 2N états avec N bascules, un seul bit change à chaque front : séquencement, division de fréquence. |
| Série ou parallèle ? | Parallèle : tous les bits en un front. Série : un bit par front, N fronts pour N bits. |

Réglage Multisim à ne pas oublier : mode BURST (une seule salve) et pas CYCLE.

## QCM d'entraînement

Annale 2023 + questions type

Réponds dans ta tête, puis ouvre la question pour voir la correction.

Une bascule D active sur front montant, avec D = Q̄. Sa sortie Q… annale 2023

1. change d'état sur front descendant de H
2. change d'état selon l'entrée PRESET
3. inverse l'état précédent sur front montant de H
4. mémorise l'état précédent

**c.** D = Q̄ : à chaque front montant, Q prend l'inverse de sa valeur. C'est le diviseur par 2.

Les entrées PRESET et CLEAR d'une bascule… annale 2023

1. sont actives sur niveau haut
2. dépendent de l'horloge
3. dépendent de l'horloge et de l'entrée D
4. sont indépendantes de l'horloge et de l'entrée D

**d.** Elles sont asynchrones, prioritaires, et actives au niveau bas.

Sur le chronogramme d'une bascule D, tpp correspond au… annale 2023

1. temps minimum avant que Q soit valide
2. temps minimum pendant lequel D doit être maintenue avant le front actif
3. temps minimum pendant lequel D doit être maintenue après le front actif
4. temps de propagation avant que Q soit valide

**b.** tpp = setup. c. est tm (hold), a. et d. décrivent tp.

Un registre 4 bits dont chaque entrée ei arrive directement sur une D… annale 2023

1. copie ses entrées ei sur ses sorties Si au même front d'horloge
2. copie ses entrées après 4 fronts
3. est un registre entrée parallèle – sortie série
4. est un registre entrée série – sortie parallèle

**a.** Chargement parallèle : un seul front suffit. Il faudrait 4 fronts en série.

Un compteur ayant la séquence [3, 4, 5, 9] nécessite… annale 2023

1. 3 bascules
2. 4 bascules
3. 5 bascules
4. 9 bascules

**b.** 9 = 1001 s'écrit sur 4 bits. Ce n'est pas le nombre d'états (4) qui compte, mais la plus grande valeur.

Bascule JK avec J = K = 1, au front actif…

1. Q = 1
2. Q = 0
3. Q garde sa valeur
4. Q s'inverse

**d.** Mode toggle.

Compteur asynchrone à 4 bascules, tp = 10 ns par bascule. Fréquence d'horloge maximale ?

1. 100 MHz
2. 40 MHz
3. 25 MHz
4. 10 MHz

**c.** Retard max = 4 × 10 = 40 ns, donc fmax = 1 / 40 ns = 25 MHz.

Bascules D sur front montant, CLKi = Qi−1, CI 000. Le circuit est…

1. un compteur modulo 8
2. un décompteur modulo 8
3. un registre à décalage
4. un compteur synchrone

**b.** Au premier front, Q0 passe de 0 à 1 : ce front montant fait basculer Q1, qui fait basculer Q2. On passe de 0 à 7.

Compteur asynchrone modulo 10 par RAZ. Que met-on dans la NAND reliée aux ~CLR ?

1. Q3 et Q0
2. Q3 et Q1
3. Q3, Q2 et Q1
4. Q0 et Q1

**b.** 10 = 1010 : Q3 et Q1. (Q3 et Q0 détecte 9, ce qui ferait un modulo 9.)

Horloge à 1 MHz. Fréquence de Q2 dans un compteur asynchrone ?

1. 333 kHz
2. 250 kHz
3. 125 kHz
4. 500 kHz

**c.** fH / 23 = 125 kHz.

Compteur Johnson à 4 bascules : nombre d'états ?

1. 4
2. 8
3. 16
4. 5

**b.** 2N = 8. En anneau, ce serait N = 4. En binaire naturel, 2N = 16.

Registre à décalage 8 bits, entrée série. Combien de fronts pour charger un mot complet ?

1. 1
2. 4
3. 8
4. 16

**c.** Un bit par front.

Bascule RS en NOR avec S = R = 1 ?

1. Mémoire
2. Set
3. Reset
4. État non utilisé

**d.** Q = Q̄ = 0, ce qui contredit la définition.

Différence entre une D latch et une D flip-flop ?

1. La latch réagit sur front, la flip-flop sur niveau
2. La latch réagit sur niveau, la flip-flop sur front
3. La latch n'a pas d'horloge
4. Aucune

**b.** La latch recopie D tant que clk est au niveau actif ; la flip-flop ne recopie qu'au front.

Sources : CTD 1 à 3 de D. Achvar (2026-27), TP1 et TP2, TD Compteurs, DE 2023 corrigé, et nos séances de TP2. Bon courage pour samedi.
