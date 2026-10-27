# SM302 – Fonctions de plusieurs variables

Fiche FDPV

SM302 · Fonctions de plusieurs variables · Chapitres 1 à 3

# Fiche FDPV

Domaines et courbes de niveau, limites et continuité, dérivées partielles et différentiabilité. Avec un visualiseur de domaines, le simulateur de limites et un entraînement.

Chapitre 1

## Domaines et courbes de niveau

### Trouver le domaine de définition

$D\_f$ = tous les points $(x,y)$ où on peut calculer $f$. On liste les conditions, on les traduit en équations connues, puis on dessine.

| Dans f il y a… | Condition | Frontière |
| --- | --- | --- |
| une fraction $\dfrac{A}{B}$ | $B\ne0$ | exclue (pointillés) |
| une racine $\sqrt{A}$ | $A\ge0$ | incluse (trait plein) |
| un logarithme $\ln A$ | $A>0$ | exclue (pointillés) |
| $\dfrac{1}{\sqrt{A}}$ | $A>0$ | exclue |

**Exemple** : $f(x,y)=\dfrac{\sqrt{x+y+1}}{x-1}$. Conditions $x+y+1\ge0$ et $x\ne1$, donc $D\_f=\{(x,y)\ /\ y\ge -x-1,\ x\ne1\}$ : au-dessus de la droite $y=-x-1$ (incluse), sans la droite verticale $x=1$.

**Astuce** : pour savoir de quel côté d'une courbe est le domaine, teste un point simple comme $(0,0)$. S'il vérifie la condition, son côté est le bon.

### Visualiseur de domaines

Exemples du cours et du TD 1. La zone colorée est le domaine, les traits en pointillés sont exclus.

Fonction

### Équations à reconnaître

$(x-x\_0)^2+(y-y\_0)^2=R^2$cercle de centre $(x\_0,y\_0)$, rayon $R$

$y=a(x-x\_0)^2+y\_0$parabole verticale, sommet $(x\_0,y\_0)$, vers le haut si $a>0$

$x=a(y-y\_0)^2+x\_0$parabole couchée, ouverte à droite si $a>0$

$\dfrac{(x-x\_0)^2}{a^2}+\dfrac{(y-y\_0)^2}{b^2}=1$ellipse, demi-axes $a$ (en x) et $b$ (en y)

$\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$hyperbole (ex : $xy=k$ aussi)

$ax+by=c$droite

**Mettre sous forme d'ellipse** : $9-x^2-9y^2>0 \iff \dfrac{x^2}{9}+y^2<1$, l'intérieur d'une ellipse de demi-axes 3 et 1.

### Courbes de niveau

Courbe de niveau $k$ = ensemble des points où $f(x,y)=k$. C'est une coupe horizontale de la surface à la hauteur $z=k$, vue de dessus (comme une carte IGN).

**Méthode** : on écrit $f(x,y)=k$, on isole pour reconnaître une équation connue, et on discute selon $k$.

**Exemple** : $9-x^2-y^2=k \iff x^2+y^2=9-k$.

$k<9$ : cercle de rayon $\sqrt{9-k}$
$k=9$ : le point $(0,0)$
$k>9$ : vide

| Surface | Équation | Courbes de niveau |
| --- | --- | --- |
| Plan | $z=8-2x-4y$ | droites parallèles |
| Paraboloïde | $z=x^2+y^2$ | cercles |
| Paraboloïde elliptique | $z=ax^2+by^2$ | ellipses |
| Paraboloïde hyperbolique (selle) | $z=x^2-y^2$ | hyperboles |
| Cylindre parabolique | $z=x^2$ | droites verticales |
| Sphère | $x^2+y^2+z^2=R^2$ | cercles |

Chapitre 2

## Limites et continuité

### L'idée

En une variable, on arrive en $a$ par la gauche ou par la droite. En deux variables, le point est dans un plan : on peut y arriver par **une infinité de chemins** (axes, droites, paraboles, spirales…).

La limite existe et vaut $\ell$ si **tous** les chemins mènent à $\ell$. Donc :

2 chemins, 2 valeurs → n'existe pas
existe → il faut une preuve qui couvre tous les chemins

### La méthode

1

**Remplacer directement**

On remplace $(x,y)$ par le point. Ex : $\dfrac{x^2+3y}{1+xy}$ en $(1,2)$ donne $\dfrac{7}{3}$.

un nombre → fini$\frac00$ → étape 2

2

**Tester des chemins**

On remplace une relation entre $x$ et $y$ dans $f$ pour obtenir une fonction d'une seule variable. Dans l'ordre :

$(x,mx)\ \to\ (0,y)\ \to\ (x,x^2)\ \text{ou}\ (y^2,y)$

$(x,mx)$ contient déjà $(x,0)$ ($m=0$) et $(x,x)$ ($m=1$) : pas besoin de les faire à part. S'il reste du $m$, prends $m=0$ et $m=1$ comme tes deux valeurs, c'est fini.

Encore $\frac00$ sur un chemin ? On ne change pas de chemin : on **simplifie** (on factorise le $x^2$ en haut et en bas). Ex : $\dfrac{mx^2}{x^2(1+m^2)}=\dfrac{m}{1+m^2}$.

2 valeurs différentes → n'existe pastoujours $\ell$ → étape 3

3

**Prouver que la limite vaut $\ell$**

**Majoration :** trouver $g$ avec $|f(x,y)-\ell| \le g(x,y) \to 0$.

**Polaires :** on reprend la **fonction d'origine** (pas celle avec $y=mx$), $x=r\cos\theta,\ y=r\sin\theta$, on simplifie les $r$ ($x^2+y^2=r^2$), puis $r\to0$.

Rédaction : majore la partie en $\theta$ ($|\cos|\le1$, $|\sin|\le1$). Ex : $|3r\cos^2\theta\sin\theta|\le3r\to0$. Écrire seulement « ça tend vers 0 » peut coûter des points.

ne dépend pas de $\theta$ → existedépend de $\theta$ → n'existe pas

### Raccourci : comparer les degrés

Degré d'un terme = somme des puissances de $x$ et $y$ ($x^2y$ est de degré 3). On note $p$ le degré du haut, $q$ celui du bas. Ça dit **quoi chercher**, puis on rédige :

>

**$p > q$ : la limite vaut 0, on le prouve en polaires**

Ex : $\dfrac{x^3+y^3}{x^2+y^2}=\dfrac{r^3(\cos^3\theta+\sin^3\theta)}{r^2}=r\,(\cos^3\theta+\sin^3\theta)$

On majore la partie en $\theta$ avec $|\cos|\le1,\ |\sin|\le1$ : $|f|\le 2r\to0$. Rédaction : « ne dépend pas de $\theta$, la limite existe et vaut 0 ».

=

**$p = q$ : la limite n'existe pas, on le prouve avec $y=mx$**

Ex : $\dfrac{xy}{x^2+y^2}$ avec $y=mx$ : $\dfrac{mx^2}{x^2(1+m^2)}=\dfrac{m}{1+m^2}$

Les $x$ s'annulent toujours (même degré), il reste une expression en $m$. On donne deux valeurs : $m=0\to0$, $m=1\to\tfrac12$. Si elle ne dépend pas de $m$, la limite existe (rare).

<

**$p < q$ : n'existe pas (pas finie)**

Ex : $\dfrac{x}{x^2+y^2}$ avec $y=0$ : $\dfrac{1}{x}$, qui tend vers $+\infty$ ou $-\infty$ selon le côté.

?

**Un étage mélange des degrés différents : la règle ne marche pas**

Ex : $x^4+y^2$. On choisit le chemin qui rend les deux termes du bas égaux : ici $y=x^2$ (alors $y^2=x^4$). Pour $x^2+y^4$, c'est $x=y^2$. Ce chemin donne souvent une valeur non nulle.

### En polaires, il ne reste que du θ ?

Ça arrive quand haut et bas ont le même degré. Ex : $\dfrac{2xy^2}{(x^2+y^2)^{3/2}}=\dfrac{2r^3\cos\theta\sin^2\theta}{r^3}=2\cos\theta\sin^2\theta$.

**D'abord simplifier :** est-ce que ça se réduit à un nombre fixe ? Le cas à connaître : $\cos^2\theta+\sin^2\theta=1$.

il reste un nombre (ex : 3) → existe et vaut 3
il reste du θ → n'existe pas

**Pour le prouver,** donne deux angles qui donnent deux valeurs. Teste dans l'ordre $0,\ \tfrac\pi4,\ \tfrac\pi2,\ \pi$. Ici : $\theta=0\to0$ et $\theta=\tfrac\pi4\to\tfrac{\sqrt2}{2}$.

**Deux angles donnent la même valeur ?** Ça ne prouve rien, tu es peut-être tombé dessus par hasard ($\theta=0$ et $\theta=\tfrac\pi2$ donnent tous les deux 0 ici). Essaie un autre angle. Si tous donnent exactement pareil, c'est sûrement une constante cachée.

### Au contrôle : quel outil, quand ?

1

Remplacement direct. Un nombre ? Fini.

2

$\frac00$ ? Compare les degrés $p$ (haut) et $q$ (bas).

3

$p=q$ → $y=mx$, deux valeurs de $m$
$p>q$ → polaires + majoration
degrés mélangés en bas → parabole qui équilibre

4

Deux valeurs différentes → n'existe pas. Toujours la même $\ell$ → preuve en polaires ou majoration. Point $\ne(0,0)$ → recentre d'abord.

### Majorations à connaître

$\dfrac{x^2}{x^2+y^2}\le 1$idem avec $y^2$ au numérateur

$|x|\le\sqrt{x^2+y^2}$idem pour $|y|$

$2|xy|\le x^2+y^2$vient de $(|x|-|y|)^2\ge0$

$|\cos|\le1,\ |\sin|\le1$utile en polaires

$x^2+y^2=r^2$le dénominateur devient simple

$\dfrac{\sin t}{t}\xrightarrow[t\to0]{}1$avec $t=x^2+y^2$

### Pièges classiques

**Toutes les droites donnent 0, donc la limite vaut 0 ?** Non. Avec $\dfrac{x^2y}{x^4+y^2}$, toutes les droites donnent 0 mais la parabole $y=x^2$ donne $\tfrac12$. Teste toujours une parabole.

**Plein de chemins donnent la même valeur, donc c'est prouvé ?** Non. Les chemins servent à *soupçonner* $\ell$. La preuve passe par une majoration ou les polaires.

**Le point n'est pas (0,0) ?** On recentre. En $(1,0)$ : on pose $X=x-1$ et on étudie la limite quand $(X,y)\to(0,0)$.

### Continuité

$f$ est continue en $(a\_1,a\_2)$ si et seulement si $\displaystyle\lim\_{(x,y)\to(a\_1,a\_2)} f(x,y) = f(a\_1,a\_2)$.

Polynômes, fractions rationnelles, $\sin$, $\cos$, $\exp$, $\ln$ et leurs combinaisons sont continus sur leur domaine. Le seul point à étudier est le **point problématique** d'une fonction définie en deux morceaux :

$f(x,y)=\begin{cases}\dfrac{2xy}{x^2+y^2} & \text{si } (x,y)\ne(0,0)\\[4pt] 0 & \text{si } (x,y)=(0,0)\end{cases}$

1

Calcule la limite en $(0,0)$ avec la méthode des limites (morceau du haut).

2

Compare avec la valeur imposée (morceau du bas).

limite existe et = valeur → continuepas de limite ou ≠ valeur → pas continue

Ici $y=mx$ donne $\dfrac{2m}{1+m^2}$ : ça dépend de $m$, pas de limite, donc **f n'est pas continue en (0,0)**.

**Prolongement par continuité** : si $f$ n'est pas définie en un point mais que sa limite y existe et vaut $\ell$, on peut la prolonger en posant $\tilde f(a\_1,a\_2)=\ell$. Ex : $\dfrac{x-y}{x^2-y^2}=\dfrac{1}{x+y}\to\dfrac12$ en $(1,1)$.

## Le simulateur

Choisis une fonction et un chemin, puis rapproche-toi de (0,0). Enregistre plusieurs chemins : dès que deux valeurs diffèrent, la limite n'existe pas. Le curseur « Angle θ » de la droite, c'est le θ des polaires : si la limite change quand tu le bouges, elle dépend de θ.

Fonction

Chemin vers (0,0)

Angle θ

Distance au point

Valeurs de f sur [−1,1]². Orange : positif, bleu : négatif. Trait : ton chemin.

f le long du chemin, en fonction du paramètre t. Le rond creux marque la valeur vers laquelle f tend en t = 0.

Point (x, y)

–

f(x, y)

–

Limite sur ce chemin

–

Chemins testés

* Aucun chemin enregistré.

Chapitre 3

## Dérivées partielles et différentiabilité

### Dérivées partielles premières

Pour $\dfrac{\partial f}{\partial x}$ : **$y$ est une constante**, on dérive par rapport à $x$ comme d'habitude. Pour $\dfrac{\partial f}{\partial y}$ : $x$ est une constante.

Notations équivalentes : $\dfrac{\partial f}{\partial x} = f\_x = D\_1 f = D\_x f$.

**Exemple** : $f(x,y)=3x^2+3xy^2+5x-1$

$\dfrac{\partial f}{\partial x}=6x+3y^2+5 \qquad \dfrac{\partial f}{\partial y}=6xy$

En $(-5,4)$ : $f\_x=-30+48+5=23$ et $f\_y=6\times(-5)\times4=-120$.

**Sens** : $f\_x(a\_1,a\_2)$ est la pente de la surface quand on avance dans la direction des $x$, en restant à $y=a\_2$.

**Piège** : $\dfrac{\partial}{\partial x}(x\sin(xy))=\sin(xy)+xy\cos(xy)$. La règle du produit et la dérivée de $\sin(u)$ s'appliquent normalement, avec $y$ vu comme un nombre.

### Dérivées secondes et théorème de Schwarz

On redérive une dérivée première. Il y en a quatre : $f\_{xx}$, $f\_{yy}$ et les deux **mixtes** $\dfrac{\partial^2 f}{\partial x\partial y}=\dfrac{\partial}{\partial x}\Big(\dfrac{\partial f}{\partial y}\Big)$ et $\dfrac{\partial^2 f}{\partial y\partial x}$.

**Schwarz** : si $f$ et ses dérivées secondes sont continues, les deux mixtes sont **égales**. Tu n'en calcules qu'une, l'autre sert de vérification.

**Exemple** : $f=x^3+xy^4-3y^2$ donne $f\_x=3x^2+y^4$ et $f\_y=4xy^3-6y$.

$f\_{xx}=6x \qquad f\_{yy}=12xy^2-6 \qquad f\_{xy}=f\_{yx}=4y^3$

### Dérivée partielle au point problématique

Pour une fonction en deux morceaux, les règles de dérivation ne marchent qu'en dehors du point. **Au point**, on revient à la définition :

$\dfrac{\partial f}{\partial x}(a\_1,a\_2)=\lim\limits\_{h\to0}\dfrac{f(a\_1+h,a\_2)-f(a\_1,a\_2)}{h} \qquad \dfrac{\partial f}{\partial y}(a\_1,a\_2)=\lim\limits\_{h\to0}\dfrac{f(a\_1,a\_2+h)-f(a\_1,a\_2)}{h}$

**Exemple** : $f=\dfrac{xy^3}{x^2+y^2}$, $f(0,0)=0$.

$\dfrac{\partial f}{\partial x}(0,0)=\lim\limits\_{h\to0}\dfrac{f(h,0)-0}{h}=\lim\limits\_{h\to0}\dfrac{0}{h}=0$, et de même $\dfrac{\partial f}{\partial y}(0,0)=0$.

**Dérivées partielles qui existent ≠ fonction continue.** $\dfrac{2xy}{x^2+y^2}$ (prolongée par 0) a $f\_x(0,0)=f\_y(0,0)=0$, mais elle n'est pas continue en $(0,0)$ : sur l'axe $y=0$ elle vaut toujours 0, mais pas sur la diagonale.

### Différentiabilité

**Théorème** : si $f\_x$ et $f\_y$ existent et sont **continues** autour de $(a\_1,a\_2)$, alors $f$ est différentiable en ce point. On dit que $f$ est $C^1$.

1

Calcule $f\_x$ et $f\_y$ hors du point, avec les règles.

2

Calcule $f\_x$ et $f\_y$ au point, avec la définition (limite en $h$).

3

Vérifie que la limite de $f\_x(x,y)$ quand $(x,y)\to$ le point égale la valeur de l'étape 2. Pareil pour $f\_y$. C'est une limite du chapitre 2 : polaires ou majoration.

4

les deux continues → différentiable

Ce qu'il faut retenir :

$C^1$ ⇒ différentiable ⇒ continue
dérivées partielles existent ⇏ continue
continue ⇏ dérivées partielles existent

Polynômes, fractions rationnelles (là où le dénominateur ≠ 0), $\sin$, $\cos$, $\exp$ sont $C^1$. Sommes, produits, quotients et composées de fonctions différentiables sont différentiables.

### Règle de la chaîne

Si $x$ et $y$ dépendent de $t$ :

$\dfrac{df}{dt}=\dfrac{\partial f}{\partial x}\dfrac{dx}{dt}+\dfrac{\partial f}{\partial y}\dfrac{dy}{dt}$

Si $x$ et $y$ dépendent de $u$ et $v$ :

$\dfrac{\partial f}{\partial u}=\dfrac{\partial f}{\partial x}\dfrac{\partial x}{\partial u}+\dfrac{\partial f}{\partial y}\dfrac{\partial y}{\partial u} \qquad \dfrac{\partial f}{\partial v}=\dfrac{\partial f}{\partial x}\dfrac{\partial x}{\partial v}+\dfrac{\partial f}{\partial y}\dfrac{\partial y}{\partial v}$

Moyen mnémotechnique : on passe par **chaque** variable intermédiaire, et on additionne les chemins.

### Gradient et dérivée directionnelle

$\nabla f(a\_1,a\_2)=\Big(\dfrac{\partial f}{\partial x}(a\_1,a\_2),\ \dfrac{\partial f}{\partial y}(a\_1,a\_2)\Big)$

direction de la plus forte montée
$-\nabla f$ : plus forte descente
perpendiculaire aux courbes de niveau
$\|\nabla f\|$ = pente maximale

**Dérivée dans une direction $\vec u$** (si $f$ est différentiable) : on rend $\vec u$ unitaire, puis $D\_{\vec u}f=\nabla f\cdot\vec u$.

**Exemple** : $f=xe^y+\cos(xy)$ en $(2,0)$, direction $(3,-4)$. $f\_x=e^y-y\sin(xy)=1$, $f\_y=xe^y-x\sin(xy)=2$, donc $\nabla f=(1,2)$. $\|(3,-4)\|=5$, donc $\vec u=(\tfrac35,-\tfrac45)$ et $D\_{\vec u}f=\tfrac35-\tfrac85=-1$.

La fonction ne change pas dans les directions perpendiculaires au gradient.

### Équations aux dérivées partielles

**Primitiver** : la « constante » d'intégration devient une **fonction de l'autre variable**.

$\dfrac{\partial f}{\partial x}=2x+y \;\Rightarrow\; f(x,y)=x^2+xy+g(y)$

$\dfrac{\partial^2 f}{\partial x\partial y}=0 \;\Rightarrow\; f(x,y)=G(x)+h(y)$

**Avec un changement de variables** $u,v$ : on exprime $f\_x$ et $f\_y$ en fonction de $f\_u,f\_v$ (règle de la chaîne), on remplace, et l'équation devient simple.

Ex : $f\_x-3f\_y=0$ avec $u=2x+y$, $v=3x+y$. On a $f\_x=2f\_u+3f\_v$ et $f\_y=f\_u+f\_v$, donc $-f\_u=0$, donc $f=g(v)=g(3x+y)$.

## Entraînement limites

Quatre fonctions, comme au contrôle. Toutes en (0,0) sauf mention. Réponds, puis lis la correction.

Score : 0 / 0
