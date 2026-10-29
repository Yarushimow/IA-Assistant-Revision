# TI307 – Introduction au système Linux

Révision CE Linux — TI307

TI307 · Introduction au système Linux · EFREI

# Fiche de révision CE\_

Tout le cours condensé pour le DE : TP1 (bases du shell), TP2 (permissions), TP3 (variables, quoting, gcc, descripteurs) et TP4 (redirections, processus, signaux). Commandes, pièges, calculateurs et simulateurs interactifs, et QCM avec corrigés.

DE le **samedi 10 oct.**
Au programme : **TP1 → TP4**
10 exos corrigés

TP1

## Bases du shell

Anatomie d'une commande, navigation, gestion des fichiers, chemins et raccourcis.

### Anatomie d'une commande

Une commande se lit : `commande [options] [arguments]`. Les options courtes se combinent (`ls -la` ≡ `ls -l -a`), les options longues s'écrivent `--all`.

Quatre **types** de commandes, révélés par `type` : externe (binaire dans le `PATH`), interne (builtin du shell), alias, fonction.

### Chemins absolu vs relatif

* **Absolu** : part de la racine, commence par `/` — ex. `/home/yoan/tp1`.
* **Relatif** : part du répertoire courant — ex. `../projets/tp1`.
* `.` = répertoire courant · `..` = parent · `~` = home de l'utilisateur.
* Jokers (globbing) : voir la section dédiée juste en dessous.

### Jokers / globbing TP1 · exo 7 — tombe souvent

Les jokers sont interprétés **par le shell** (pas par la commande) **avant** d'exécuter. Point crucial : `*` et `?` ne matchent **pas** les fichiers cachés (qui commencent par `.`).

| Motif | Signification | Exemple |
| --- | --- | --- |
| `*` | N'importe quelle suite de caractères (même vide) | `*.txt` |
| `?` | **Exactement un** caractère | `fic?.c` |
| `[abc]` | Un caractère parmi a, b ou c | `[aA]*` |
| `[a-z]` | Un caractère dans une plage | `[0-9]*` |
| `[^abc]` / `[^0-9]` | Un caractère **sauf** ceux listés (inversion) | `[^0-9]*` |

!

**Le piège n°1 :** `[...]` matche **un seul** caractère. `[ch]` = un « c » ou un « h », pas « ch ». Donc `*.[ch]` attrape `.c` et `.h` mais **jamais** `.cpp`. Et `[^0-9].txt` exige un nom d'**un seul** caractère non-chiffre : pour « ne commence pas par un chiffre » il faut `[^0-9]*.txt`.

Sur le jeu de test du TP : `annee1 Annee2 annee4 annee45 annee41 annee510 annee_saucisse annee_banane bonbon`

| Commande | Résultat |
| --- | --- |
| `ls *5` | Se terminent par 5 → `annee45 annee41`… non : seulement `annee45` (finit par 5) |
| `ls annee4*` | `annee4 annee45 annee41` |
| `ls [aA]*` | Commencent par a ou A → tous les `annee…` + `Annee2` |
| `ls [^0-9]*` | Ne commencent pas par un chiffre → tout (aucun ne commence par un chiffre ici) |
| `ls annee[^0-9]*` | 6e caractère non-chiffre → `annee_saucisse annee_banane` |
| `ls *ana*` | Contiennent « ana » → `annee_banane` |
| `echo ??????` | Noms d'exactement 6 caractères → `annee1 Annee2 annee4 bonbon` |
| `echo *_*` | Contiennent un underscore → `annee_saucisse annee_banane` |

### Navigation & exploration

| Commande | Rôle | Options utiles |
| --- | --- | --- |
| `pwd` | Affiche le répertoire courant | — |
| `cd` | Change de répertoire | `cd` seul → home · `cd -` → précédent |
| `ls` | Liste le contenu | `-l` détail · `-a` cachés · `-R` récursif · `-d` le dossier lui-même |

$ pwd
/home/yoan
$ cd projets/tp2
$ pwd
/home/yoan/projets/tp2

### Gestion des fichiers & répertoires

| Commande | Rôle | Options utiles |
| --- | --- | --- |
| `mkdir` | Crée un répertoire | `-p` crée les parents manquants |
| `touch` | Crée un fichier vide / met à jour la date | — |
| `cp` | Copie | `-R` récursif (dossiers) |
| `mv` | Déplace *ou* renomme | — |
| `rm` | Supprime | `-r` récursif · `-f` force (sans confirmation) |
| `rmdir` | Supprime un répertoire **vide** | `-p` supprime la chaîne de parents vides |
| `ln` | Crée un lien | `-s` lien symbolique (sinon lien physique) |

$ mkdir -p site/css
$ touch site/index.html
$ cp -R site sauvegarde # copie le dossier entier
$ mv site/index.html site/accueil.html # renomme
$ ls site
accueil.html css
$ rm -r sauvegarde # supprime le dossier + son contenu

### Consultation & aide

| Commande | Rôle |
| --- | --- |
| `man` | Manuel des commandes **externes** |
| `help` | Aide des commandes **internes** (builtins) |
| `type` | Dit quel type est une commande (externe/interne/alias/fonction) |
| `cat` | Affiche le contenu d'un fichier |
| `wc` | Compte : `-l` lignes · `-w` mots · `-c` octets |
| `date` · `cal` · `who` · `uname` · `echo` | Date · calendrier · connectés · infos système · afficher du texte |

$ date
dim. 13 septembre 2026 15:42:07 CEST
$ echo "Bonjour $USER"
Bonjour yoan
$ cat notes.txt
révisions Linux
CE samedi 19
$ wc -l notes.txt # -l = nombre de lignes
2 notes.txt
$ uname -s
Linux
$ type cd
cd is a shell builtin
$ type ls
ls is /usr/bin/ls

$ cal
 septembre 2026
lu ma me je ve sa di
1 2 3 4 5 6
7 8 9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30

!

**Piège classique du CC1 :** ne pas confondre `man` (commandes **externes**) et `help` (commandes **internes** du shell). Le CE aime bien tester ça.

### Commandes internes vs externes TP1 · exo 5

`type` révèle 4 catégories : **builtin** (interne au shell), **external** (binaire sur le disque, dans le `PATH`), **function**, **alias**. Les internes n'ont pas de fichier ; les externes vivent dans `/bin` ou `/usr/bin`.

| Type | Exemples vus en TP |
| --- | --- |
| **Internes** (builtins) | `cd`, `echo`, `type`, `help`, `umask`, `hash` |
| **Externes** (binaires) | `ls`, `pwd`, `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `cat`, `wc`, `uname`, `date`, `cal`, `who`, `find`, `chmod` |

$ type type
type is a shell builtin
$ type -a echo # -a montre TOUTES les correspondances, dans l'ordre
echo is a shell builtin
echo is /usr/bin/echo

### Raccourcis clavier

* Tab complétion automatique · ↑↓ ou Ctrl-P/Ctrl-N historique
* Ctrl-L efface l'écran · Ctrl-U efface la ligne · Ctrl-A/Ctrl-E début/fin de ligne
* Ctrl-C interrompt · Ctrl-D fin d'entrée / quitte le terminal

### Recherche avec `find` TP1 · exo 8

Syntaxe : `find <chemin> <critères> [action]`. Contrairement aux jokers du shell, `find` **descend récursivement** dans toute l'arborescence et interprète lui-même le motif (d'où les guillemets sur `-name`).

| Critère | Sélectionne |
| --- | --- |
| `-type f` / `-type d` | Fichiers réguliers / répertoires |
| `-name "*.conf"` | Par nom (guillemets obligatoires pour que le shell ne développe pas le motif) |
| `-mtime -1` | Modifiés il y a moins de 24 h |
| `-size +100c` | Plus de 100 octets |

$ find /etc -type f -name "\*.conf"
/etc/ssh/ssh\_config
/etc/resolv.conf
$ find /var/log -type f -mtime -1 # logs modifiés dans les dernières 24h

→

`ls /etc/*.conf` = expansion par le shell, **pas de récursion** (seulement le niveau courant). `find /etc -name "*.conf"` = parcours **récursif**. C'est la différence clé jokers vs `find`.

### Liens physiques & symboliques TP1 · exo 9

|  | Lien physique — `ln f lien` | Lien symbolique — `ln -s f lien` |
| --- | --- | --- |
| **Inode** | Le **même** que l'original | Un inode **différent** (fichier spécial qui contient un chemin) |
| **Si on supprime l'original** | Le lien marche toujours (données gardées tant qu'un nom existe) | Le lien est **cassé** (pointe dans le vide) |
| **Sur un répertoire** | **Interdit** (risque de cycles) | Autorisé |
| **Autre système de fichiers** | Impossible | Possible |

$ ln -s notes.txt raccourci
$ ls -li
1734562 -rw-r--r-- 2 yoan etu 512 sept. 24 notes.txt
1734562 -rw-r--r-- 2 yoan etu 512 sept. 24 dur.txt # même inode + compteur à 2
1734999 lrwxrwxrwx 1 yoan etu 9 sept. 24 raccourci -> notes.txt

`ls -i` affiche le numéro d'inode : deux liens physiques ont le **même** numéro. Le `l` et la flèche `->` repèrent un lien symbolique.

### Premier script shell TP1 · exo 10

Un script commence par un **shebang** qui désigne l'interpréteur, puis il faut le rendre exécutable avant de le lancer avec `./`.
```
#!/bin/bash
# affiche des infos système
echo "=== Infos ==="
echo "Date : $(date)" # $(...) = substitution de commande
echo "User : $(whoami)"
if [ -z "$1" ]; then # $1 = 1er argument ; -z = chaîne vide ?
echo "Donne un nom de projet"
exit 1 # quitte avec un code d'erreur
fi
mkdir "$1"

$ chmod +x mon\_script.sh # le rendre exécutable
$ ./mon\_script.sh projet1 # ./ car le répertoire courant n'est pas dans le PATH
```
TP2

## Système de fichiers & permissions

La hiérarchie FHS, la lecture des droits, chmod, umask et les permissions spéciales.

### Hiérarchie du système (FHS)

| Répertoire | Contient |
| --- | --- |
| `/` | La racine, sommet de l'arborescence |
| `/bin` · `/sbin` | Binaires essentiels (utilisateur / système) |
| `/etc` | Fichiers de configuration (dont `/etc/passwd`) |
| `/home` | Répertoires personnels des utilisateurs |
| `/root` | Home de l'administrateur `root` |
| `/usr` | Programmes & bibliothèques installés |
| `/var` | Données variables (logs, files d'attente) |
| `/tmp` | Fichiers temporaires (souvent avec sticky bit) |
| `/dev` · `/proc` | Périphériques · infos des processus (virtuel) |

### Inode & `/etc/passwd`

Le **nom** d'un fichier et le fichier lui-même sont séparés : le nom (dans le répertoire) pointe vers un **inode**, qui contient les métadonnées (droits, propriétaire, taille, dates) et l'emplacement des données. C'est ce qui rend possibles les liens physiques.

Une ligne de `/etc/passwd` a 7 champs séparés par `:` :

login:x:UID:GID:commentaire:/home/login:/bin/bash

`id` affiche ton UID, ton GID et tes groupes. `groups` liste juste les groupes.

$ id
uid=1001(yoan) gid=1001(etu) groups=1001(etu),27(sudo)
$ groups
etu sudo

### Lire les droits avec `ls -l`

Le premier bloc de `ls -l` = 1 caractère de type + 9 bits de permissions (3 × `rwx`) pour **u**tilisateur / **g**roupe / **o**thers.

-rwxr-xr-- 1 yoan etu 2048 sept. 9 tp2.sh

type

-

user (u)

rwx

7

group (g)

r-x

5

others (o)

r--

4

`-rwxr-xr--` → octal **754**  ·  type : `-` fichier, `d` répertoire, `l` lien

→

Poids des bits : **r = 4**, **w = 2**, **x = 1**. On additionne par groupe. `rwx` = 4+2+1 = 7, `r-x` = 4+1 = 5, `r--` = 4.

### Droits sur un fichier **vs** un répertoire à connaître par cœur

| Bit | Sur un fichier | Sur un répertoire |
| --- | --- | --- |
| `r` | Lire le contenu | Lister les noms (`ls`) |
| `w` | Modifier le contenu | Créer / supprimer / renommer des entrées |
| `x` | Exécuter | Traverser / entrer (`cd`), accéder aux fichiers |

!

Sur un répertoire, `x` sans `r` : on peut y entrer et accéder à un fichier si on connaît son nom, mais pas lister. `r` sans `x` : on voit les noms mais on ne peut rien ouvrir. Il faut **presque toujours** `x` sur un dossier pour s'en servir.

### Quels droits pour quelle opération TP2 · exos 4 & 7 — le gros piège

Le point qui trompe tout le monde : **supprimer ou créer un fichier ne dépend pas des droits du fichier, mais de ceux du dossier qui le contient.**

| Opération | Droit requis | Sur quoi |
| --- | --- | --- |
| `cat f` (lire) | `r` | le fichier |
| `echo ... >> f` (écrire) | `w` | le fichier |
| `./f` (exécuter) | `x` | le fichier |
| `cd d` (entrer) | `x` | le dossier |
| `ls d` (lister) | `r` | le dossier |
| `rm f` (supprimer) | `w` + `x` | **le dossier parent** (pas le fichier !) |
| `touch f` (créer) | `w` + `x` | **le dossier parent** |
| `cp f g` | `r` sur `f` + `w`,`x` sur le dossier de destination | les deux |

!

`rm g` peut réussir même si `g` est en lecture seule (voire 000) : seul compte le fait que tu aies `w`+`x` sur le **dossier**. C'est exactement le genre de question du CE.

### Combinaisons de droits sur un dossier

| Droits | `ls` (lister) | `cd` (entrer) | Accès à un fichier connu | Créer / supprimer |
| --- | --- | --- | --- | --- |
| `---` (000) | ✗ | ✗ | ✗ | ✗ |
| `r--` (400) | ✓ (noms seuls) | ✗ | ✗ | ✗ |
| `--x` (100) | ✗ | ✓ | ✓ (si on connaît le nom) | ✗ |
| `-wx` (300) | ✗ | ✓ | ✓ | ✓ |
| `r-x` (500) | ✓ | ✓ | ✓ | ✗ |
| `rwx` (700) | ✓ | ✓ | ✓ | ✓ |

### `chmod` — notation symbolique & octale

* **Symbolique** : cible `u`/`g`/`o`/`a` (all) + opérateur `+`/`-`/`=` + droits. Ex. `chmod u+x fic`, `chmod go-w fic`, `chmod a=r fic`.
* **Octale** : trois chiffres, un par groupe. Ex. `chmod 755 fic` → `rwxr-xr-x`, `chmod 644 fic` → `rw-r--r--`.

$ ls -l script.sh
-rw-r--r-- 1 yoan etu 128 sept. 13 script.sh
$ chmod u+x script.sh # ajoute x au propriétaire
$ ls -l script.sh
-rwxr--r-- 1 yoan etu 128 sept. 13 script.sh
$ chmod 640 script.sh # réécrit tout en octal
$ ls -l script.sh
-rw-r----- 1 yoan etu 128 sept. 13 script.sh

La forme symbolique complète est `[ugoa][+-=][rwx]`. Le choix de l'opérateur change tout :

| Opérateur | Effet |
| --- | --- |
| `+` | **Ajoute** les droits cités, sans toucher aux autres |
| `-` | **Retire** les droits cités, sans toucher aux autres |
| `=` | **Fixe exactement** ces droits : tout ce qui n'est pas cité est **retiré** |

| Commande | Ce qu'elle fait |
| --- | --- |
| `chmod a=` | **Enlève TOUS les droits à tout le monde** → `---------` (000). Le `=` fixe « exactement rien ». |
| `chmod a=r f` | Fixe exactement r pour tous → `r--r--r--` (444). |
| `chmod o+rw f` | Ajoute lecture + écriture aux **others**. |
| `chmod o-wx f` | Retire écriture + exécution aux others. |
| `chmod u=o f` | Le propriétaire reçoit **les droits actuels des others** (on copie une classe sur une autre). |
| `chmod g+u f` | Le groupe **gagne les droits actuels du propriétaire**. |
| `chmod a+x,g-w f` | La **virgule chaîne** plusieurs changements en une commande. |

!

**C'est LA question qui t'a bloqué au CE :** `chmod a=` (rien après le `=`) → tout le monde perd tout, résultat `----------`. À retenir : le `=` **remplace** (il efface ce qui n'est pas cité), alors que `+`/`-` ne touchent qu'aux bits mentionnés. `root` et le propriétaire peuvent toujours refaire un `chmod` ensuite (changer les droits dépend de la propriété, pas du bit `w`).

### `umask` — le masque de création

Le `umask` **retire** des droits aux valeurs par défaut (**666** pour un fichier, **777** pour un répertoire). On **soustrait** le masque.
```
# umask 022 (valeur par défaut courante)
fichier : 666 − 022 = 644 (rw-r--r--)
dossier : 777 − 022 = 755 (rwxr-xr-x)

$ umask
0022
$ touch nouveau.txt
$ mkdir nouveau\_dir
$ ls -l
-rw-r--r-- 1 yoan etu 0 sept. 13 nouveau.txt # 644
drwxr-xr-x 2 yoan etu 4096 sept. 13 nouveau\_dir # 755
```
!

Un fichier ne reçoit **jamais** `x` à la création, même si le calcul le permettrait : le défaut est 666, pas 777. Le `x` se pose ensuite avec `chmod`.

→

**La règle exacte (au cas où le TP te piège) :** ce n'est pas une vraie soustraction, c'est un **ET bit à bit avec l'inverse du masque** : `droits = base ET (NON umask)`. La soustraction donne le bon résultat **sauf** quand un chiffre du masque contient un bit absent de la base. Ex. base **666**, umask **121** : la soustraction donnerait 545 (faux), le vrai résultat est **646** (le bit `x` du masque ne retire rien puisque la base n'a pas de `x`). Dans tous les cas courants (022, 027, 077, 002) la soustraction marche.

| umask | Fichier (base 666) | Dossier (base 777) |
| --- | --- | --- |
| `022` | 644 `rw-r--r--` | 755 `rwxr-xr-x` |
| `027` | 640 `rw-r-----` | 750 `rwxr-x---` |
| `077` | 600 `rw-------` | 700 `rwx------` |
| `002` | 664 `rw-rw-r--` | 775 `rwxrwxr-x` |

### PATH & résolution des commandes TP2 · exo 6

* `PATH` est la liste des dossiers (séparés par `:`) où le shell cherche les binaires, **dans l'ordre** — la première correspondance gagne.
* Un chemin **absolu** (`/bin/ls`) ou explicite (`./mon_prog`) contourne toujours le `PATH`.
* Bash met en cache l'emplacement des commandes : `hash -r` vide ce cache quand un binaire change de place ou de droits.

$ echo $PATH
/home/yoan/bin:/usr/local/bin:/usr/bin:/bin
$ type -a rm # montre TOUTES les correspondances, dans l'ordre du PATH
rm is /usr/bin/rm
rm is /bin/rm

!

**Shadowing** : si tu mets un dossier **en tête** du `PATH` avec un fichier `rm` à toi, c'est **lui** qui s'exécute à la place du vrai `rm` (piège vu au CC1). Et si tu retires le `x` d'une commande (`chmod -x`), Bash **ne bascule pas** vers le binaire système : tu obtiens une erreur de permission.

### Permissions spéciales

| Bit | Octal | Effet | Vu dans `ls -l` |
| --- | --- | --- | --- |
| SUID | `4000` | Exécute avec les droits du **propriétaire** | `s` à la place du `x` de u |
| SGID | `2000` | Droits du **groupe** / héritage du groupe sur un dossier | `s` à la place du `x` de g |
| Sticky | `1000` | Seul le propriétaire peut supprimer ses fichiers (ex. `/tmp`) | `t` à la place du `x` de o |

On les pose en octal sur **4 chiffres** (le 1er = bits spéciaux) : `chmod 4755 prog` (SUID + 755), `chmod 2775 equipe` (SGID + 775), `chmod 1777 partage` (sticky + 777).

→

**SGID sur un dossier** = les nouveaux fichiers créés dedans héritent automatiquement du **groupe du dossier** (pratique pour un dossier d'équipe partagé). **SGID sur un fichier** = il s'exécute avec les droits du groupe. Attention : si le `x` de base est absent, le bit spécial s'affiche en **majuscule** (`S` ou `T`) — ça veut dire « bit posé mais pas d'exécution ».

`find` permet de les chercher — teste les critères :

$ find / -perm -4000 -type f 2>/dev/null # tous les binaires SUID (2>/dev/null masque les erreurs)
$ find / -perm -2000 -type f # les SGID
$ find /home -perm -o=w -type f # fichiers écrivables par tout le monde (risque)
$ find /home -nouser -o -nogroup # fichiers sans proprio / sans groupe valide

TP3

## Environnement de travail & compilation C

Variables, caractères spéciaux et leur inhibition, expansion d'accolades, substitution de commande, puis compilation C avec gcc et descripteurs de fichiers.

### Variables shell TP3 · exo 1

* Affectation : `nom=valeur` — **aucun espace** autour du `=` (sinon erreur).
* Développement : le `$` déclenche le remplacement → `echo $nom`. Les accolades `${nom}` délimitent le nom (utile pour coller du texte : `${nom}pp`).
* Une variable **non définie** se développe en chaîne **vide** (pas d'erreur).
* Variable **shell** (locale) vs variable d'**environnement** (transmise aux processus enfants après `export`). `set` montre tout, `env`/`printenv` seulement l'environnement.

$ nom\_fich=hello.c
$ echo nom\_fich
nom\_fich # sans $ : texte littéral
$ echo $nom\_fich
hello.c
$ echo ${nom\_fich}pp
hello.cpp # les accolades séparent la variable du suffixe
$ echo $nom\_fichpp
 # variable inexistante → vide

### Caractères spéciaux & inhibition TP3 · exos 2-4 — le cœur

Les caractères **spéciaux** (`$`, `*`, `\`, `'`, `"`, espace, `;`…) ont un sens pour le shell. Les **inhiber** = les rendre littéraux. Trois mécanismes :

| Mécanisme | Effet | Développe `$var` ? | Développe `*` ? |
| --- | --- | --- | --- |
| `\c` (backslash) | Rend **le caractère suivant** littéral | — | — |
| `'…'` (apostrophes) | **Tout** est littéral, sans exception | **Non** | **Non** |
| `"…"` (guillemets) | Littéral **sauf** `$`, `` ` ` ``, `\` | **Oui** | Non |

$ echo 3\$canadiens
3$canadiens # \ inhibe le $
$ touch 'un horrible nom de fichier'
$ echo "il a dit \"salut\""
il a dit "salut"

!

La distinction clé : `'$x'` affiche **`$x`** (littéral), `"$x"` affiche **la valeur**. Les apostrophes coupent TOUT, les guillemets laissent passer les variables et `$(…)` mais protègent les jokers.

### Expansion d'accolades TP3 · exo 5

Les accolades **génèrent des chaînes**, indépendamment des fichiers existants (≠ jokers qui, eux, matchent des fichiers réels).
```
$ echo a{b,c,d}e
abe ace ade
$ echo {1..5}
1 2 3 4 5
$ mkdir -p projet/{src,tests,docs} # crée 3 sous-dossiers d'un coup
$ touch fichier\_{01..03}.txt
# crée fichier\_01.txt fichier\_02.txt fichier\_03.txt
```
→

**Accolades vs jokers :** `{a,b,c}` génère `a b c` même si rien n'existe ; `[abc]` ne matche que des fichiers **présents**. C'est une question de cours classique.

### Substitution de commande TP3 · exo 6

`$(commande)` insère la **sortie** d'une commande dans la ligne. Fonctionne hors quotes et entre guillemets, jamais entre apostrophes.

$ echo "Nous sommes le $(date)"
Nous sommes le lun. 24 sept. 2026 …
$ aujourdhui=$(date) # stocke la sortie dans une variable

Syntaxe moderne `$(…)` recommandée ; l'ancienne `` ` ` `` (backquotes) existe mais s'imbrique mal. À ne pas confondre : `$(…)` = substitution de **commande**, `${…}` = développement de **variable**.

### Compilation C avec gcc TP3 · exos 7-8

Quatre étapes derrière `gcc` : **préprocesseur** (cpp, `-E`) → **compilation** (`-S`, produit du `.s`) → **assemblage** (as, `-c`, produit du `.o`) → **édition de liens** (ld). Une **erreur** empêche la compilation ; un **warning** la laisse passer.

**Compilation séparée :** chaque source → un `.o` (avec `-c`), puis on lie tous les objets. Avantage : on ne recompile que ce qui a changé.

$ gcc -c main.c hello.c bye.c # produit main.o hello.o bye.o
$ gcc \*.o -o run # édition de liens → exécutable

!

Conventions C du TP : `void f(void)` (pas `void f()`), et garde d'en-tête `BYE_H` (pas `_BYE_H_`, réservé). Bonne pratique pro : `-Wall -Wextra -Werror`.

### Descripteurs de fichiers TP3 · exos 9-10

Tout processus démarre avec 3 descripteurs standards :

| N° | Nom | Rôle |
| --- | --- | --- |
| `0` | STDIN\_FILENO | entrée |
| `1` | STDOUT\_FILENO | sortie |
| `2` | STDERR\_FILENO | erreurs |

* `read(fd, buf, n)` / `write(fd, buf, n)` peuvent traiter **moins** d'octets que demandé → il faut **boucler**. `read` renvoie **0** = fin de fichier (EOF), **-1** = erreur.
* `dup2(fd, 1)` = fait pointer le descripteur **1** vers le même fichier que `fd` → c'est **ainsi que le shell implémente `>`** (ouvrir le fichier, `dup2` sur stdout, fermer le fd d'origine).
* `dup(fd)` = duplique vers le **plus petit** descripteur libre ; les deux partagent la **même position** (offset). Fermer l'un ne ferme pas le fichier tant que l'autre est ouvert.

TP4

## Canaux standards, processus & signaux

Redirections des 3 canaux, tubes, gestion des processus/tâches (premier & arrière-plan) et envoi de signaux.

### Les 3 canaux & les redirections TP4 · exos 1-3

Rappel : **0** = stdin (entrée), **1** = stdout (sortie), **2** = stderr (erreurs). On redirige chaque canal séparément.

!

`>` **écrase** sans prévenir, `>>` **ajoute**. `>` ≡ `1>` et `<` ≡ `0<` (le canal 1/0 est implicite). Pour séparer : `cmd 1> ok.txt 2> err.txt` envoie sortie et erreurs dans deux fichiers.

### Tubes (pipes) TP4 · exo 4

Le tube `|` branche le **stdout** d'une commande sur le **stdin** de la suivante.

$ ls /usr/include/\*.h | wc -l
312 # compte les .h, sans fichier intermédiaire

### Processus & tâches TP4 · exos 5-6

Un **processus** = une unité d'exécution du système (un PID unique). Une **tâche** (job) = ce que lance le shell (un ou plusieurs processus).

| Commande / touche | Effet |
| --- | --- |
| `ps` · `ps -e` | Liste tes processus · tous les processus |
| `top` | Vue interactive (quitter avec `q`) |
| `jobs` · `jobs -p` | Tâches du shell · seulement leurs PID |
| `Ctrl-Z` | Suspend la tâche au premier plan (signal SIGTSTP) |
| `Ctrl-C` | Interrompt la tâche au premier plan (signal SIGINT) |
| `fg %1` · `bg %1` | Reprend la tâche 1 au premier plan · en arrière-plan |
| `cmd &` | Lance `cmd` directement en **arrière-plan** |

$ ./compteur # tourne au premier plan
^Z # Ctrl-Z → suspendu
$ jobs
[1]+ Stopped ./compteur
$ bg %1 # repart en arrière-plan
$ fg %1 # revient au premier plan

### Signaux TP4 · exo 7 — tombe au DE

Un signal se envoie avec `kill`. Trois syntaxes équivalentes : `kill -SIGTERM`, `kill -s SIGTERM`, `kill -15`. On cible un **PID** ou une tâche `%n`.

!

**SIGTERM (15)** = arrêt **propre** (le programme peut nettoyer) → à privilégier. **SIGKILL (9)** = tue de force, **ni interceptable ni ignorable** → dernier recours pour un processus figé. **SIGINT** ≈ Ctrl-C (interrompre), **SIGTSTP** ≈ Ctrl-Z (suspendre, pas tuer).

→

Choix du bon signal : interrompre un programme → SIGINT ; arrêter un service proprement → SIGTERM ; processus figé qui ne répond plus → SIGKILL ; suspendre un calcul pour le reprendre → SIGTSTP puis SIGCONT.

TP4+

## Filtres de texte, grep, sed & awk

Les exercices complémentaires : filtrer et transformer du texte, chaîner les outils avec des tubes, extraire des données de fichiers structurés comme `/etc/passwd`.

### Filtres de base tout passe par stdin → stdout

| Commande | Rôle | Options clés |
| --- | --- | --- |
| `head` / `tail` | Premières / dernières lignes | `-n 5` (nombre de lignes) · `-c` (octets) |
| `sort` | Trie les lignes | `-n` tri numérique · `-r` inverse |
| `uniq` | Supprime les doublons **consécutifs** | `-c` compte les occurrences |
| `cut` | Extrait des colonnes | `-d: -f1` (champ 1, délim. `:`) · `-c1-3` (caractères) |
| `tr` | Remplace / supprime des caractères | `tr 'a' 'b'` · `tr -d ' '` (supprime) |
| `rev` | Inverse les caractères de chaque ligne | — |
| `tee` | Écrit dans un fichier **ET** à l'écran | `… | tee f.txt` |

!

**Piège `uniq` :** il ne supprime que les doublons **côte à côte**. Pour dédoublonner un fichier non trié, il faut **trier d'abord** → `sort fichier | uniq`.

### grep en détail TP4-exo · exo 3

Les 4 tâches de l'exercice, résolues :
```
# 1. valeur de la constante RAND\_MAX
$ grep -r "RAND\_MAX" /usr/include
# 2. chemins + lignes contenant 127.0.0.1 dans /etc
$ grep -r "127.0.0.1" /etc
# 3. SEULEMENT les noms de fichiers concernés
$ grep -rl "127.0.0.1" /etc
# 4. répertoire personnel de l'utilisateur games
$ grep "^games:" /etc/passwd | cut -d: -f6
/usr/games
```
### Pipelines classiques

La force du shell : enchaîner des petits outils avec `|`. Quelques combos qui reviennent :
```
# distribution des shells utilisés dans /etc/passwd
$ cut -d: -f7 /etc/passwd | sort | uniq -c | sort -rn
 28 /usr/sbin/nologin
3 /bin/bash
1 /bin/sync
# les 10 fichiers .h les plus légers de /usr/include
$ wc -c /usr/include/\*.h | sort -n | head -n 10
```
→

Le combo `sort | uniq -c | sort -rn` est un classique : **trier** → **compter** les doublons → **reclasser** du plus fréquent au moins fréquent.

### sed — éditeur de flux ⭐ exo 4

| Commande | Effet |
| --- | --- |
| `sed 's/x/y/' f` | Remplace la **1ʳᵉ** occurrence de `x` par `y` sur chaque ligne |
| `sed 's/x/y/g' f` | `g` = global → **toutes** les occurrences de la ligne |
| `sed '/motif/d' f` | `d` = **supprime** les lignes contenant `motif` |
| `sed -i 's/x/y/g' f` | `-i` = modifie le fichier **en place** (⚠ pas de retour arrière) |

$ sed 's/:/ /g' /etc/passwd # remplace tous les : par des espaces
$ sed '/nologin/d' /etc/passwd # enlève les comptes nologin

### awk — traitement par champs ⭐ exos 5-6

Idéal pour les fichiers en colonnes. `-F:` fixe le séparateur, `$1`…`$7` sont les champs, `$0` la ligne entière.

$ awk -F: '{ print $1, $7 }' /etc/passwd # login + shell
$ awk -F: '$7 == "/bin/bash"' /etc/passwd # filtrer par shell
$ awk -F: '$3 >= 1000' /etc/passwd # utilisateurs humains (UID ≥ 1000)
$ awk 'END { print NR }' /etc/passwd # NR = nombre de lignes à la fin

→

**cut vs awk :** `cut` suffit pour extraire une colonne simple ; `awk` sert dès qu'il faut **filtrer** (conditions sur les champs), **calculer** ou **reformater**. Pour `/etc/passwd`, délimiteur `:` dans les deux cas (`cut -d:` / `awk -F:`).

★

## Calculateur chmod

Clique les bits pour t'entraîner à convertir symbolique ↔ octal. À faire de tête le jour du CE.

#### rwx → octal

Active les droits pour chaque groupe et lis le résultat.

user

0

group

0

others

0

000  ·  ---------

▷

## Simulateur de `cd`

Navigue dans une vraie arborescence : tape une commande `cd` (chemin absolu ou relatif) ou clique un dossier. Le simulateur t'affiche où tu atterris et surligne ta position.

yoan@efrei:~$

Position de départ : **/home/yoan** (ton home, alias `~`).

contenu du dossier courant (ls) :

Essaie `cd ..`, `cd ../..`, `cd -`, `cd ~`, `cd /`, ou un chemin complet. Les fichiers ne sont pas des dossiers → `cd` dessus renvoie une erreur, comme dans un vrai shell.

⚑

## Pièges & nuances spécial DE — le prof en met beaucoup

Les distinctions subtiles qui font perdre des points, regroupées par TP. Colonne de gauche : ce qui trompe. Colonne de droite : la nuance à retenir.

* **Linux *est* un système de type UNIX.** (Erreur repérée au CC1 — ne pas répondre l'inverse.)
* **`man` vs `help` :** `man` pour les commandes externes, `help` pour les builtins du shell.
* **Shadowing du PATH :** mettre un dossier *en tête* du `PATH` peut masquer un binaire système. Les chemins absolus, eux, ignorent le `PATH`.
* **Cache de Bash :** après avoir déplacé un binaire ou changé ses droits, `hash -r` pour vider le cache — sinon Bash cherche encore à l'ancien endroit.
* **`chmod -x` :** retirer `x` à une commande provoque une erreur de permission — Bash ne bascule **pas** automatiquement vers un binaire système du même nom.
* **umask :** on *soustrait*, et un fichier ne reçoit jamais `x` à la création (défaut 666).

→

Astuce de démo/TP : pour voir la sortie de `cat`, `echo "du texte" > fic` est plus pratique que `touch fic` (le fichier a un contenu).

### TP1 — shell, chemins, jokers

| Ce qui trompe | La nuance à retenir |
| --- | --- |
| `cd ..` vs `cd -` vs `cd ~` | `..` = parent (juste au-dessus) · `cd -` = **dernier** dossier visité · `cd ~` = home. Positions différentes ! |
| Un chemin qui contient `.src` | Seuls `.` (courant) et `..` (parent) sont spéciaux. `.src` est un simple nom **caché** (commence par un point), pas le répertoire courant. |
| `cd..` collé | Il faut **un espace** : `cd ..`. Collé → « command not found ». |
| `*.[ch]` sur un `.cpp` | `[ch]` = **un seul** caractère (c ou h). `.cpp` (3 lettres) n'est **pas** matché. |
| `[^0-9].txt` | = un nom d'**un seul** caractère non-chiffre + `.txt`. « Ne commence pas par un chiffre » = `[^0-9]*.txt`. |
| `*` et `?` et les fichiers cachés | Ils n'incluent **jamais** les fichiers commençant par `.` (il faut `ls -a` pour les voir). |
| `rmdir` sur un dossier plein | Échoue : `rmdir` = dossiers **vides** seulement. Sinon `rm -r`. |
| `ls > f.txt` qui se liste lui-même | Le shell crée `f.txt` **avant** de lancer `ls` → il fait déjà partie du dossier listé. |
| lien physique vs symbolique | Physique = **même inode**, survit à la suppression de l'original, interdit sur dossier. Symbolique = chemin, **cassé** si la cible disparaît, OK sur dossier. |

### TP2 — permissions

| Ce qui trompe | La nuance à retenir |
| --- | --- |
| `chmod a=` | Rien après le `=` → tout le monde perd tout → `----------` (000). |
| `=` vs `+`/`-` | `=` **remplace** (efface ce qui n'est pas cité) · `+`/`-` ne touchent qu'aux bits mentionnés. |
| `chmod u=o` | Le propriétaire reçoit les droits **actuels** des others (on copie une classe sur une autre). |
| umask « soustraction » | En vrai c'est un **ET binaire** avec l'inverse. Cas 121 sur base 666 → **646** (pas 545). Marche comme une soustraction seulement en cas courants. |
| Un fichier créé avec `x` ? | Jamais : base d'un fichier = **666** (777 pour un dossier). Le `x` se pose ensuite. |
| `rm f` / `touch f` | Dépendent des droits du **dossier parent** (`w`+`x`), **pas** du fichier. On peut supprimer un fichier en lecture seule. |
| Dossier `r` sans `x` (ou l'inverse) | `r` seul : on voit les noms mais on n'accède à rien. `x` seul : on entre et accède si on connaît le nom, mais pas de liste. |
| SUID/sticky dans `ls -l` | `s` à la place du `x` de **u** (SUID), `t` à la place du `x` de **o** (sticky). **Majuscule** `S`/`T` si le `x` dessous est absent. |
| `chmod -x` sur une commande | Provoque une **erreur de permission** ; Bash ne bascule pas vers le binaire système. Un chemin absolu ignore le PATH. |

### TP3 — variables, quoting, gcc, descripteurs

| Ce qui trompe | La nuance à retenir |
| --- | --- |
| `x = 5` (avec espaces) | **Erreur** : aucune espace autour du `=`. C'est `x=5`. |
| `echo $inexistante` | Se développe en **chaîne vide**, sans erreur. |
| `'$x'` vs `"$x"` | Apostrophes = **tout littéral** (affiche `$x`). Guillemets = variables et `$(…)` développés, mais **jokers protégés**. |
| `$(…)` vs `${…}` | `$(…)` = sortie d'une **commande** · `${…}` = valeur d'une **variable**. |
| `{a,b}` vs `[ab]` | Accolades **génèrent** du texte (même sans fichiers) · crochets **matchent** des fichiers existants. |
| `gcc hello.c` sans `-o` | Produit `a.out` (pas `hello`). `-c` s'arrête au `.o` (aucun exécutable). |
| `read`/`write` « lisent tout » | Peuvent traiter **moins** d'octets que demandé → il faut **boucler**. `read` renvoie **0** = EOF, **-1** = erreur. |
| `dup(fd)` vs deux `open()` | `dup` partage la **même position** (offset). Deux `open()` = descriptions **indépendantes** (offsets séparés). |
| Garde d'en-tête `_BYE_H_` | Convention : `BYE_H`. Les formes `_XXX_` sont réservées. |

### TP4 — canaux, processus, signaux

| Ce qui trompe | La nuance à retenir |
| --- | --- |
| `1>` vs `>` · `<` vs `0<` | **Identiques** : le canal 1 (stdout) et 0 (stdin) sont implicites. `1>>` = `>>` aussi. |
| `>` vs `>>` | `>` écrase (et **vide le fichier avant** d'exécuter, même si la commande plante) · `>>` ajoute. |
| `2>` | Redirige **stderr** (canal 2), séparé de stdout (canal 1). D'où `cmd 1> ok 2> err`. |
| `cat f` vs `cat < f` | `cat f` = **1 argument** · `cat < f` = **0 argument** (le fichier arrive par stdin). Même affichage, chemin différent. |
| `cat` seul affiche « en double » | Normal : 1× l'**écho du clavier** (le terminal) + 1× la **recopie** par `cat`. Avec `cat < f` pas d'écho clavier → une seule fois. |
| `ls | wc -l` vs `wc -l $(ls)` | Pipe → compte le **nombre de fichiers** (liste sur stdin). `$(…)` → les noms deviennent des **arguments**, `wc` compte les **lignes dans** les fichiers (total bien plus grand). |
| Ctrl-Z vs Ctrl-C | Ctrl-Z = SIGTSTP (**suspend**) · Ctrl-C = SIGINT (**interrompt**). Reprise = SIGCONT (`fg`/`bg`). |
| SIGTERM vs SIGKILL | SIGTERM (15) = arrêt **propre**, interceptable, **défaut** de `kill`. SIGKILL (9) = **force**, ni interceptable ni ignorable. |
| Processus vs tâche | Tâche (job) = unité du **shell** (un ou plusieurs processus) · processus = unité du **système** (un PID). |
| Syntaxes de `kill` | `kill -SIGTERM` = `kill -s SIGTERM` = `kill -15` → **même effet**. |

✎

## Exos type CE

Réponds d'abord, puis déplie le corrigé. Cache les réponses pour te tester en conditions.

01

Crée en une seule commande l'arborescence `projets/tp2/logs` à partir de ton home, même si `projets` n'existe pas.

Appliquer

▸ Voir le corrigé

$ mkdir -p ~/projets/tp2/logs

L'option `-p` crée tous les parents manquants et ne renvoie pas d'erreur s'ils existent déjà.

02

Traduis `-rw-r-----` en octal, puis donne la commande `chmod` (octale) équivalente sur `notes.txt`.

Appliquer

▸ Voir le corrigé

u = `rw-` = 4+2 = **6** · g = `r--` = **4** · o = `---` = **0** → **640**.

$ chmod 640 notes.txt

03

Un `umask` vaut `027`. Quels seront les droits d'un **fichier** et d'un **répertoire** nouvellement créés ? (octal + symbolique)

Analyser

▸ Voir le corrigé

Fichier : 666 − 027 = **640** → `rw-r-----`.

Répertoire : 777 − 027 = **750** → `rwxr-x---`.

Le groupe perd `w` (2), others perd tout (7).

04

Quelle est la différence entre `man` et `help` ? Donne un exemple de commande pour chacun.

Comprendre

▸ Voir le corrigé

`man` documente les commandes **externes** (binaires) : `man ls`. `help` documente les commandes **internes** du shell (builtins) : `help cd`. Pour savoir laquelle utiliser : `type cd` → « cd is a shell builtin ».

05

Un dossier `partage` a les droits `drwxr-x---`, propriétaire `yoan`, groupe `etu`. L'utilisateur `lea` (groupe `etu`) peut-elle : (a) lister son contenu ? (b) créer un fichier dedans ?

Analyser

▸ Voir le corrigé

`lea` est dans le groupe `etu` → droits du groupe = `r-x`.

**(a) Oui** : `r` permet de lister et `x` de traverser.

**(b) Non** : créer un fichier demande `w` sur le dossier, que le groupe n'a pas.

06

Décris les 7 champs d'une ligne de `/etc/passwd` : `yoan:x:1001:1001:Yoan:/home/yoan:/bin/bash`

Comprendre

▸ Voir le corrigé

login `yoan` · mot de passe `x` (déporté dans `/etc/shadow`) · UID `1001` · GID `1001` · commentaire/GECOS `Yoan` · home `/home/yoan` · shell de connexion `/bin/bash`.

07

Donne **en symbolique** la commande qui : ajoute `x` au propriétaire, retire `w` au groupe et à others, sur `script.sh` — sans toucher au reste.

Appliquer

▸ Voir le corrigé

$ chmod u+x,go-w script.sh

La notation symbolique n'affecte que les bits cités : les autres droits restent inchangés (contrairement à l'octal qui réécrit tout).

08

Tu déplaces ton binaire `mon_prog` dans un autre dossier du `PATH`, mais Bash affiche « No such file or directory ». Pourquoi, et comment corriger ?

Analyser

▸ Voir le corrigé

Bash a mis en **cache** l'ancien emplacement (table de hachage). Il faut le vider :

$ hash -r

Ensuite Bash refait la recherche dans le `PATH`.

09

À quoi sert le **sticky bit** sur `/tmp` (`drwxrwxrwt`) ? Et comment le poser en octal sur un dossier `echange` déjà en 777 ?

Évaluer

▸ Voir le corrigé

Malgré le `w` pour tous, le sticky bit fait que **seul le propriétaire d'un fichier** (ou de `/tmp`, ou root) peut le supprimer. Sans lui, n'importe qui pourrait effacer les fichiers des autres.

$ chmod 1777 echange # le 1 = sticky

Le `t` apparaît à la place du `x` de others : `drwxrwxrwt`.

10

Écris une commande `find` qui recherche, à partir de `/`, tous les fichiers ayant le bit **SUID** positionné.

Créer

▸ Voir le corrigé

$ find / -perm -4000

Le `-` devant `4000` signifie « au moins ces bits » (le SUID est présent, peu importe le reste). Sans le `-`, il faudrait une correspondance exacte du mode.

?

## QCM — 5 séries

Trois QCM complets sur TP1-2, une série « cas pièges » (dont le fameux `chmod a=`), et une série TP3-4 (variables, quoting, gcc, redirections, processus, signaux). Chaque série a son propre score. Une seule bonne réponse : clique, la correction et l'explication s'affichent tout de suite ; change de série avec les onglets.

Fiche de révision — TI307 Introduction au système Linux · EFREI
`man` ≠ `help` · r4 w2 x1 · umask se soustrait
