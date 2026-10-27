# TI301 – Structures de données et programmation

Fiche CE TI301

TI301 · Contrôle Écrit · 1 h · CM1–CM3 / TD1–TD3

# Fiche CE : listes, piles, files

Les éléments de cours à connaître, puis les exercices de TD de la liste du prof, avec la méthode d’abord et la correction repliée. Essaie chaque exercice sur papier avant d’ouvrir la correction, avec un schéma.

**Attention à l’énoncé :** le message du prof inverse les sigles. Une **pile** est **LIFO** (Last In First Out, on retire le dernier posé). Une **file** est **FIFO** (First In First Out, le premier arrivé sort en premier). C’est ce que dit le CM3 (slides 3 et 4).

## 1. Les types à connaître

```
// Cellule et liste simple (CM1)
typedef struct s_cell {
    int value;
    struct s_cell *next;
} t_cell;

typedef struct s_list {
    t_cell *head;          // t_list encapsule le pointeur de tête
} t_list;

// Liste "head and tail" (CM2)
typedef struct s_ht_list {
    t_cell *head;          // première cellule
    t_cell *tail;          // dernière cellule
} t_ht_list;

typedef t_ht_list t_circ_list;   // circulaire : tail->next == head

// Pile (CM3)
typedef t_list t_stacklist;      // pile avec liste : on empile/dépile en tête

#define NBMAX 50
typedef struct s_stacktab {
    int values[NBMAX];
    int nbElts;                  // taille logique = nb d'éléments
} t_stacktab;

// File (CM3)
typedef t_ht_list t_queue;       // file avec liste ht : on enfile en fin, défile en tête

typedef struct s_queuetab {
    int values[NBMAX];
    int first, last;             // first : où défiler, last : où enfiler
} t_queuetab;
```

Les fonctions de base du CM1 que tu réutilises partout :

```
t_cell *createCell(int val) {
    t_cell *nouv = (t_cell *)malloc(sizeof(t_cell));
    nouv->value = val;
    nouv->next = NULL;
    return nouv;
}

void addCell(t_list *ptr_list, int val) {   // ajout en tête
    t_cell *nouv = createCell(val);
    nouv->next = ptr_list->head;
    ptr_list->head = nouv;
}
```

| Structure | Vide si… | Fin de parcours | Une seule cellule si… |
| --- | --- | --- | --- |
| Liste simple | `l.head == NULL` | `curr == NULL` | `l.head->next == NULL` |
| Liste ht | `head == NULL` (et `tail == NULL`) | `curr == NULL` | `head == tail` |
| Circulaire | `head == NULL` | `curr == tail` ou `curr->next == head` | `head == tail` |

## 2. Méthode pour trouver un prototype

Le CM fait toujours le même tableau en quatre colonnes. Chaque colonne donne une partie du prototype.

| Colonne | Ce qu’elle donne |
| --- | --- |
| Nom | le nom de la fonction, le plus explicite possible |
| A besoin de | les paramètres |
| Modifie l’état ? | **oui → paramètre pointeur**, non → paramètre par valeur |
| Valeur attendue | le type de retour (`void` si rien, `int` 1/0 pour vrai/faux) |

**« Modifier » a un sens précis.** On modifie la *variable*, pas les valeurs des cellules :

* **Liste simple** : modifiée ⇔ `head` change. Ajouter en fin ou changer une `value` ne modifie pas la liste.
* **Liste ht / circulaire** : modifiée ⇔ `head` ou `tail` change.
* **Pile tableau** : `nbElts` change. **File tableau** : `first` ou `last` change.

| Fonction | Modifie ? | Prototype |
| --- | --- | --- |
| Rechercher | non | `int searchList(t_list list, int val);` |
| Ajout en tête | oui (head) | `void addCell(t_list *ptr_list, int val);` |
| Supprimer une valeur | peut-être (si en tête) | `void deleteVal(t_list *ptr_list, int val);` |
| Pile vide ? | non | `int isEmptyStack(t_stacktab s);` |
| Dépiler | oui | `int pop(t_stacktab *p_stack);` |
| Consulter le sommet | non | `int top(t_stacktab s);` |
| Enfiler | oui | `void enqueue(t_queue *p_q, int val);` |

Si la fonction *peut* modifier dans un seul cas (suppression en tête par exemple), il faut quand même un pointeur.

## 3. Piles et files : où insérer, où retirer

|  | Pile (LIFO) | File (FIFO) |
| --- | --- | --- |
| Principe | on ajoute et retire **au même bout** | on ajoute à un bout, on retire **à l’autre** |
| Opérations | `push`, `pop`, `top`, `isEmptyStack`, `createStack` | `enqueue`, `dequeue`, `top`, `isEmptyQueue`, `createQueue` |
| Avec liste | push = ajout en tête, pop = retrait en tête. O(1) | liste **ht** : enqueue en fin (tail), dequeue en tête (head). O(1) |
| Avec tableau | push dans `values[nbElts]` puis `nbElts++` ; pop : `nbElts--` puis lire `values[nbElts]` | buffer circulaire : enfiler en `last % NBMAX`, défiler en `first % NBMAX` |
| Vide | `nbElts == 0` / `head == NULL` | `first == last` / `head == NULL` |
| Pleine (tableau) | `nbElts == NBMAX` | `last - first == NBMAX` |

**Pourquoi enfiler en fin et défiler en tête** avec une liste ht ? Retirer en fin demanderait l’avant-dernière cellule, donc un parcours complet en O(N). Retirer en tête et ajouter après `tail` sont tous les deux en O(1).

**Précondition** : on n’appelle `pop`/`dequeue` que si la structure n’est pas vide. Le CM conseille de tester `isEmpty…` avant l’appel (et `assert` dans la fonction), ou la variante `int pop(t_stacktab *p, int *p_val)` qui renvoie 0 si rien n’a pu être dépilé.

## TD1 ex.2 · Recherche de valeur

**Méthode.** Un pointeur `curr` part de `head`. Deux cas d’arrêt : trouvé (`curr->value == valeur`) ou fin de liste (`curr == NULL`). On teste **d’abord** `curr != NULL` : grâce au `&&` paresseux, on ne lit jamais `NULL->value`.

Voir la correction

```
// a) renvoie 1 si trouvée, 0 sinon
int searchList(t_list list, int valeur) {
    t_cell *curr = list.head;
    while (curr != NULL && curr->value != valeur)
        curr = curr->next;
    return (curr != NULL);
}

// b) renvoie l'adresse de la cellule, NULL si non trouvée
t_cell *searchListPtr(t_list list, int valeur) {
    t_cell *curr = list.head;
    while (curr != NULL && curr->value != valeur)
        curr = curr->next;
    return curr;
}
```

* **Pourquoi `t_list` et pas `t_list *` ?** La recherche ne change pas `head`. La fonction reçoit une copie ; même si on déplaçait `list.head`, l’original resterait intact.
* **« Non trouvé » pour un pointeur** : `NULL`.
* **Complexité** : O(N) au pire (valeur absente ou en fin), O(1) au mieux (en tête).
* **Pourquoi la version b) est préférée** : elle donne la même info (NULL = absent) *plus* l’adresse de la cellule, ce qui permet ensuite de la lire ou de la modifier sans reparcourir la liste.

## TD1 ex.5 · Suppression de valeur

Liste : `112 → 107 → 134 → 107 → 105 → NULL`

**Méthode.** Deux pointeurs : `curr` sur la cellule testée, `prev` sur la précédente. Dans une liste simplement chaînée on ne peut pas revenir en arrière, or supprimer `curr` c’est faire pointer sa précédente sur sa suivante.

Voir le tableau des cas

| Cas | Ce qu’il faut faire | Liste modifiée ? |
| --- | --- | --- |
| En tête (112) | `head = curr->next` puis `free(curr)` | **oui**, head change |
| Au milieu (134) | `prev->next = curr->next` puis `free` | non |
| En fin (105) | pareil, `prev->next` devient `NULL` | non |
| Absent (117) | rien, `curr` arrive à NULL | non |
| Doublon (107) | seule la 1re occurrence (2e cellule) est supprimée | non |

Comme un des cas modifie la liste, le paramètre est un **pointeur**.

Voir la correction

```
void deleteVal(t_list *ptr_list, int id) {
    t_cell *curr = ptr_list->head;
    t_cell *prev = NULL;

    // Étape 1 : parcourir jusqu'à trouver l'ID ou atteindre la fin
    while (curr != NULL && curr->value != id) {
        prev = curr;
        curr = curr->next;
    }
    // Étape 2 : ID absent (couvre aussi la liste vide)
    if (curr == NULL)
        return;
    // Étape 3 : suppression en tête
    if (prev == NULL)
        ptr_list->head = curr->next;
    // Étape 4 : suppression en milieu ou fin
    else
        prev->next = curr->next;
    // Étape 5 : libération (après avoir raccroché la liste)
    free(curr);
}
```

`prev == NULL` veut dire que la boucle n’a jamais avancé, donc la cellule trouvée est la première.

## TD2 ex.2 · Suppression dans une liste ht

**Méthode.** Même idée que `deleteVal`, avec une contrainte en plus : **`tail` doit rester juste**. Le début donné initialise `prev = curr = head`, donc on reconnaît la première cellule par `curr == p_list->head` (pas par `prev == NULL`).

Voir les réponses aux questions

* **Q1** Absent : après la boucle, `curr == NULL`.
* **Q2.a** Premier : `curr == p_list->head`. On fait `p_list->head = curr->next`.
* **Q2.b** Aussi le dernier (une seule cellule) : `curr == p_list->tail`. Alors `tail = NULL` (head est déjà passé à NULL).
* **Q3.a** La boucle fait toujours `prev = curr` avant `curr = curr->next`, donc à l’arrêt `prev` est bien juste avant `curr`. Fais le schéma avec `3 → 8 → 5` et val = 5.
* **Q3.b** `prev->next = curr->next`.
* **Q3.c** Si `curr == p_list->tail`, la nouvelle dernière est `prev` : `p_list->tail = prev`.

Voir la correction

```
void removeFromHt(t_ht_list *p_list, int val) {
    t_cell *curr, *prev;
    if (p_list->head != NULL) {          // liste non vide
        curr = p_list->head;
        prev = curr;
        while ((curr != NULL) && (curr->value != val)) {
            prev = curr;
            curr = curr->next;
        }
        if (curr == NULL)                  // Q1 : absent
            return;

        if (curr == p_list->head) {        // Q2.a : c'est la première
            p_list->head = curr->next;
            if (curr == p_list->tail)      // Q2.b : et aussi la dernière
                p_list->tail = NULL;
        } else {
            prev->next = curr->next;       // Q3.b
            if (curr == p_list->tail)      // Q3.c : c'était la dernière
                p_list->tail = prev;
        }
        free(curr);
    }
}
```

## TD2 ex.5 · Afficher une liste circulaire

**Q1** Liste circulaire vide : `clist.head == NULL`.

Voir la correction

```
void displayCircList(t_circ_list clist) {
    t_cell *temp;
    temp = clist.head;
    if (clist.head != NULL) {
        while (temp != clist.tail) {      // ou temp->next != clist.head
            printf("%d ", temp->value);
            temp = temp->next;
        }
        printf("%d\n", temp->value);       // la dernière, traitée après
    }
}
```

**Q3, pourquoi la dernière à part ?**

* **3.1** Si on voulait tout traiter dans la boucle, on s’arrêterait en revenant à la première : `while (temp != clist.head)`.
* **3.2** Avant le premier test, `temp` vaut déjà `clist.head`.
* **3.3** La condition est fausse dès le départ, on n’afficherait rien. Dans une liste circulaire, le point de départ est aussi le point d’arrivée : on s’arrête donc sur la dernière et on la traite après la boucle. (Une boucle `do … while (temp != clist.head)` marche aussi, à condition d’avoir testé la liste vide avant.)

## TD2 ex.6 · Supprimer dans une liste circulaire

* **Q1** On passe l’adresse car la suppression peut changer `head` et/ou `tail` : la variable de l’appelant doit être modifiée.
* **Q2** Une seule cellule : `p_list->head == p_list->tail` (et différent de NULL).

**Méthode (squelette du TD).** La boucle s’arrête *sur* la dernière cellule sans la tester (sinon on tournerait en rond). Après la boucle, deux situations : on s’est arrêté avant la fin, donc on a trouvé ; ou on est sur la dernière, et on regarde si c’est elle qui stocke la valeur. Ces deux cas sont **exclusifs** (if / else), sinon on risquerait de supprimer une deuxième occurrence.

Voir la correction

```
void removeCirc(t_circ_list *p_list, int val) {
    t_cell *curr, *prev;
    if (p_list->head != NULL) {                         // liste non vide
        if (p_list->head == p_list->tail && p_list->head->value == val) {
            free(p_list->head);                         // une seule cellule, qui stocke val
            p_list->head = NULL;                        // on réinitialise la liste
            p_list->tail = NULL;
        } else {
            curr = p_list->head;                        // on cherche la cellule
            prev = curr;
            while (curr != p_list->tail && curr->value != val) {
                prev = curr;
                curr = curr->next;
            }
            if (curr != p_list->tail) {                 // trouvée avant la fin
                if (curr == p_list->head) {             // c'est la première
                    p_list->head = curr->next;
                    p_list->tail->next = p_list->head;  // la dernière pointe sur la nouvelle première
                } else {
                    prev->next = curr->next;
                }
                free(curr);
            } else if (curr->value == val) {            // c'est la dernière qui stocke val
                prev->next = curr->next;                // = head
                p_list->tail = prev;                    // nouvelle dernière
                free(curr);
            }
        }
    }
}
```

Vérifie les cas limites sur schéma : une seule cellule qui ne contient pas `val` (on passe dans le `else`, la boucle ne tourne pas, `curr == tail` et la valeur diffère : rien ne se passe), suppression de la première, de la dernière, d’une du milieu.

## TD3 ex.2 · Labyrinthe avec une pile

La pile `path` contient des `t_position`. Le sommet est la position actuelle. On n’utilise **que** `push`, `pop`, `top`, `isEmptyStack`, `createStack` : l’implémentation (liste ou tableau) ne doit pas compter.

Q1 · La note de SDDCode

`pop(&path);` sans stocker la valeur est du C valide : la valeur renvoyée est simplement ignorée, et la pile perd bien son sommet, donc on recule d’une case. L’idée est juste. Ce qui manque : `pop` exige une pile **non vide**. Il faut tester `isEmptyStack(path)` avant. Une note autour de 7/10 se défend ; ce qui compte au CE, c’est la justification (bonne idée + précondition oubliée).

Q2 · Retour en arrière

```
// renvoie 1 si on a trouvé une position d'où repartir, 0 si la pile est vide
int backtrack(t_stack *p_path) {
    while (!isEmptyStack(*p_path)) {
        if (hasUnvisitedNeighbour(top(*p_path)))
            return 1;            // le sommet a un voisin non visité
        pop(p_path);             // impasse : on recule d'une case
    }
    return 0;
}
```

Paramètre pointeur car la pile est modifiée par `pop`.

Q3 · Afficher le chemin

**La pile doit-elle être modifiée ?** Non : à la fin elle doit être dans le même état. Mais avec un type abstrait, le seul moyen de voir les éléments est de dépiler. On dépile, on affiche, puis on remet tout en place.

```
// Version itérative avec une pile temporaire
void displayPath(t_stack *p_path) {
    t_stack tmp = createStack();
    t_position pos;
    while (!isEmptyStack(*p_path)) {        // de la position actuelle vers l'entrée
        pos = pop(p_path);
        printf("(%d,%d) ", pos.x, pos.y);
        push(&tmp, pos);
    }
    while (!isEmptyStack(tmp))              // on remet tout dans le bon ordre
        push(p_path, pop(&tmp));
}

// Version récursive : la pile d'appels sert de pile temporaire
void displayPathRec(t_stack *p_path) {
    t_position pos;
    if (!isEmptyStack(*p_path)) {
        pos = pop(p_path);
        printf("(%d,%d) ", pos.x, pos.y);
        displayPathRec(p_path);
        push(p_path, pos);                  // on rempile en remontant
    }
}
```

**Pourquoi un pointeur malgré tout ?** Parce qu’on appelle `pop` et `push`, qui exigent un pointeur. Et une copie serait dangereuse : avec une pile en liste, la copie partage les mêmes cellules, et `pop` fait `free` sur la cellule de tête. L’original pointerait alors sur de la mémoire libérée. Avec un tableau, la copie recopierait tout le tableau pour rien.

### Rappel TD3 ex.1 · push / pop

Voir la correction

```
// Pile avec liste : on travaille en tête
int pop(t_stacklist *p_stack) {          // pile supposée non vide
    t_cell *old = p_stack->head;
    int val = old->value;
    p_stack->head = old->next;
    free(old);
    return val;
}
// push = addCell (ajout en tête de liste), déjà écrit en CM1

// Pile avec tableau : on travaille à la fin
int pop(t_stacktab *p_stack) {           // pile supposée non vide
    p_stack->nbElts--;
    return p_stack->values[p_stack->nbElts];
}
void push(t_stacktab *p_stack, int val) {
    assert(p_stack->nbElts < NBMAX);      // pile non pleine
    p_stack->values[p_stack->nbElts] = val;
    p_stack->nbElts++;
}
```

## TD3 ex.4 · Files avec liste ht et avec tableau

### Partie I · File avec liste ht

**Q1** Avec une liste simple, ajouter en fin demande de parcourir toute la liste : O(N). Avec `tail`, on accède directement à la dernière : O(1).

Voir la correction

```
void enqueue(t_queue *p_q, int val) {     // ajout en fin
    t_cell *newcell = createCell(val);
    if (p_q->head == NULL) {               // file vide : la nouvelle est première ET dernière
        p_q->head = newcell;
        p_q->tail = newcell;
    } else {
        p_q->tail->next = newcell;
        p_q->tail = newcell;
    }
}

int dequeue(t_queue *p_q) {               // retrait en tête, file supposée non vide
    t_cell *old = p_q->head;
    int val = old->value;
    p_q->head = old->next;
    if (p_q->head == NULL)                 // on vient de retirer la seule cellule
        p_q->tail = NULL;
    free(old);
    return val;
}
```

Les deux cas oubliés le plus souvent : la file vide dans `enqueue`, et `tail` à remettre à NULL dans `dequeue`.

### Partie II · File avec tableau (first, last)

Opérations : enfiler 4, enfiler 8, enfiler 7, défiler, enfiler 9, défiler, enfiler 0. Départ : `first = last = 0`.

Voir la trace

| Opération | Effet | first | last |
| --- | --- | --- | --- |
| enfiler 4 | `values[0] = 4` | 0 | 1 |
| enfiler 8 | `values[1] = 8` | 0 | 2 |
| enfiler 7 | `values[2] = 7` | 0 | 3 |
| défiler | renvoie `values[0]` = 4 | 1 | 3 |
| enfiler 9 | `values[3] = 9` | 1 | 4 |
| défiler | renvoie `values[1]` = 8 | 2 | 4 |
| enfiler 0 | `values[4] = 0` | 2 | 5 |

État final (cases utilisées en couleur) : la file contient 7, 9, 0. Les valeurs 4 et 8 sont encore dans le tableau mais ne font plus partie de la file.

48790?…

012 ← first345 ← last

**Q2 · buffer circulaire** : vide si `first == last` ; pleine si `last - first == NBMAX`. On écrit en `last % NBMAX` et on lit en `first % NBMAX`. `first` et `last` augmentent sans jamais revenir à 0 : seuls les indices d’accès sont pris modulo.

Bonus · le code

```
int isEmptyQueue(t_queuetab q) { return q.first == q.last; }
int isFullQueue(t_queuetab q)  { return q.last - q.first == NBMAX; }

void enqueue(t_queuetab *p_q, int val) {
    assert(!isFullQueue(*p_q));
    p_q->values[p_q->last % NBMAX] = val;
    p_q->last++;
}
int dequeue(t_queuetab *p_q) {
    int val;
    assert(!isEmptyQueue(*p_q));
    val = p_q->values[p_q->first % NBMAX];
    p_q->first++;
    return val;
}
```

## Pièges classiques au CE

* **Ordre du `&&`** : toujours `curr != NULL && curr->value != val`, jamais l’inverse.
* **`free` en dernier** : on raccroche d’abord (`prev->next = curr->next`), on libère ensuite.
* **Oublier `tail`** dans une liste ht ou circulaire : à chaque ajout/suppression en fin, ou quand la liste devient vide.
* **Circulaire** : la fin n’est jamais `NULL`. Après une modification en tête, mettre à jour `tail->next`.
* **Liste vide** et **une seule cellule** : les deux cas limites à vérifier sur schéma pour chaque fonction.
* **Pointeur ou pas** : se demander si `head`/`tail`/`nbElts`/`first`/`last` peuvent changer.
* **`.` vs `->`** : `list.head` quand on a la liste, `ptr_list->head` quand on a un pointeur.
* **Pile / file** : on n’utilise que les fonctions de l’interface quand l’énoncé le demande, sans toucher à `values` ou `head`.
