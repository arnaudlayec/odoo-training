# Formation Odoo Développeur — Essentiel

Prérequis techniques à préparer avant la formation

*31 août – 2 septembre 2026 · Ambient IT, Pantin · Formateur : Arnaud Layec*

> **À faire avant le J-7 (impératif)**
>
> - Lire ce document en entier et effectuer TOUTES les installations ci-dessous. Au vu des
>   différents TÉLÉCHARGEMENTS (et donc besoin en bande passante) et LOGICIELS/PACKAGES à
>   installer, la 1ère journée de formation serait fortement perturbée si des prérequis
>   n'étaient pas réalisés.
> - En cas de blocage (proxy d'entreprise, pas de droits admin, ou tout autre), répondre au
>   plus vite au mail "Organisation & Prérequis d'installation" envoyé par Ambient IT, ou
>   écrire à [job@ambient-it.net](mailto:job@ambient-it.net) et
>   [arnaud.layec@akretion.com](mailto:arnaud.layec@akretion.com).
> - Prévoir une machine avec des droits ADMINISTRATEUR LOCAL — indispensable pour installer
>   Docker/WSL et pendant la formation pour installer des outils complémentaires/débogage si
>   besoin.

Note : Docker est utilisé pour la formation. Toutefois, aucune compétence avancée n'est
requise au-delà de savoir l'installer et jouer les quelques commandes indiquées dans ce
tutoriel (build et run).

## 1. Compétences requises

### 1.1 Niveau Python minimal

Odoo est développé en Python. Cette formation n'enseigne pas Python : elle l'utilise comme
langage d'implémentation dès le premier TP (J1 après-midi). Vous n'avez pas besoin d'avoir
un niveau avancé en Python mais devez être à l'aise avec :

- Syntaxe de base : variables, types (`str`, `int`, `float`, `bool`, `list`, `dict`),
  opérateurs, indentation
- Structures de contrôle : `if`/`elif`/`else`, boucles `for`/`while`
- Fonctions : `def`, paramètres, valeurs de retour, arguments nommés/par défaut
- Manipulation de listes et dictionnaires (les compréhensions sont un plus, pas indispensable)
- Notions de base en programmation orientée objet : classe, `self`, héritage, méthode — nous
  creuserons spécifiquement leur usage dans l'ORM Odoo pendant la formation, mais les syntaxes
  `class Foo(Bar):` et `return super().my_method()` ne doivent pas être découverte le jour J
- Notion de module et d'import (`import`, `from ... import ...`)
- Utilisation de décorateur (nous n'en créerons pas) suivant la syntaxe:
  ```python
  @mon_decorator
  def (...):
  ```

En cas de doute, un rafraîchissement via le
[tutoriel officiel Python](https://docs.python.org/fr/3/tutorial/) avant la formation est
vivement recommandé.

### 1.2 Client PostgreSQL

Il est fréquent pour du débogguage ou du test d'accéder à la base de données en direct. Pour la
formation, il est recommandé de savoir lancer un client PostgreSQL en ligne de commande, écrire
une requête SQL et lire sa réponse. Exemple :
```bash
psql -d db
SELECT id, login FROM res_users LIMIT 10;
UPDATE res_users SET password='admin' WHERE id=1;
```

## 2. Machine — configuration minimale

- **Système** : si les composants nécessaires sont largement standards, il est recommandé :
  - d'utiliser un système Linux de préférence, par exemple Ubuntu 24.04 LTS (Noble). Les
    distributions 22.04 et 26.04, Debian 12 et 13 ont aussi été testées. Les autres
    distributions classiques sont à priori compatibles mais non testées : prévenir le formateur
    en amont si vous êtes sur Arch/Fedora/NixOS/etc.
  - pour les utilisateurs Windows : Windows 11 dans une
    [version supportée](https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information)
    (en août 2026 : 23H3). C'est important pour un WSL à jour. Raccourci pour le savoir :
    WIN+R et "winver". Windows 10 n'est PAS SUPPORTÉ pendant cette formation car des
    prérequis matériels peuvent manquer pour WSL.
  - pour les utilisateurs Mac : tous les composants de la formation sont compatibles Mac,
    toutefois un émulateur (comme Rosetta) sera nécessaire pour l'image Docker qui est buildée
    en amd64. Essayez sans plus tarder ces prérequis et informer le formateur si vous utilisez un Mac.
- **Droits administrateur** LOCAL/sudo sur la machine (installation de logiciels, WSL pour
  Windows, Docker).
- **RAM : 16 Go minimum** (8 Go fonctionnera au minimum mais avec des ralentissements
  sensibles — Odoo + PostgreSQL + Docker + éditeur de code + navigateur en simultané).
- **Espace disque libre : 20 Go minimum**, SSD obligatoire (images Docker de l'environnement
  Odoo, code source Odoo, dépendances Python).
- **CPU : x86_64 recommandé (4 cœurs mini)**
  - Utilisateurs de Mac Apple Silicon (M1/M2/M3/M4), votre attention est requise ! C'est
    possible mais l'image Docker est buildée pour amd64. Un émulateur (Rosetta) sera
    nécessaire. Essayez sans plus tarder ces prérequis et contactez le formateur en cas de
    problème.
- **Proxy et pare-feu** (poste d'entreprise : votre attention est OBLIGATOIRE ici) : JOUEZ
  ABSOLUMENT AVANT la formation tous les téléchargements indiqués dans ce tutoriel pour vous
  assurer des politiques proxy, pare-feu ainsi qu'antivirus et restriction d'installation
  (Docker, WSL, Git, …). À défaut : désactiver temporairement le proxy ou obtenir une machine
  personnelle pour ces 3 jours.

## 3. Comptes à créer avant la formation

- Un compte GitHub (gratuit) : [github.com/join](https://github.com/join) — nécessaire pour
  cloner les dépôts d'exercices et le template Akretion.
- Un compte Docker Hub (gratuit, optionnel et recommandé) :
  [hub.docker.com](https://hub.docker.com) — évite les limites de téléchargement anonyme
  ("pull rate limit").

## 4. Éditeur de code

Votre éditeur préféré, dans lequel vous vous sentez à l'aise, sera le meilleur. Une
coloration syntaxique Python/XML avec autocomplétion et snippets est plus que recommandée.

- J'utilise personnellement VS Code en sa version Open Source :
  [code.visualstudio.com](https://code.visualstudio.com). Extensions recommandées :
  - `Python` (Microsoft)
  - `WSL` si Windows (Microsoft)
  - `Rainbow CSV`
  - `XML Tools`
  - `Easy Snippet Maker`, en particulier si vous continuez dans le développement Odoo
    (peu utile pour la formation en tant que telle)
  - `Docker` est complètement optionnel
- Alternative : PyCharm Community, vim, ...

## 5. Git

- Git installé et fonctionnel en ligne de commande (`git --version`).
- Configuré avec votre nom et email :

```bash
git config --global user.name "Prénom Nom"
git config --global user.email "vous@exemple.com"
```

## 6. Environnement Windows

*Sous Windows, on développe TOUJOURS Odoo à l'intérieur de Linux (via WSL2) — jamais
directement sous Windows. Ainsi, une fois WSL2 et Docker Desktop installés (sur Windows), le
reste des prérequis se fera en ligne de commande dans WSL.*
*Comptez 45-60 minutes pour cette section si tout se passe bien.*

### 6.1 Installer WSL2

- Ouvrir un terminal PowerShell en administrateur et lancer :

```powershell
wsl --install -d Ubuntu-24.04
```

  Note : en cas d'échec,
  [vérifiez l'activation des fonctions de Virtualisation dans votre BIOS](https://blog.stephane-robert.info/docs/admin-serveurs/linux/references-complementaires/wsl2/#activer-la-virtualisation-biosuefi)
  (dépendance matérielle).

- Redémarrer la machine si demandé. Vous allez initialiser le compte utilisateur Linux (nom
  + mot de passe) lors du premier lancement d'Ubuntu. **Attention** : ne choisir que des
  caractères en minuscules et des lettres pour le nom d'utilisateur (a-z).
- Vérifier la version de WSL utilisée (**IMPORTANT** : doit être 2, pas 1) :

```powershell
wsl -l -v
```

- Installer Windows Terminal (Microsoft Store) pour un confort d'utilisation optimal.

### 6.2 Installer Docker Desktop

- Télécharger et installer Docker Desktop :
  [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop)
- Dans les réglages Docker Desktop → Settings → Resources → WSL Integration : activer
  l'intégration avec la distribution Ubuntu-24.04 installée. Ce paramétrage est
  **obligatoire** pour la formation.
- Dans Settings → Resources : allouer au moins 4 Go de RAM et 2 CPU à Docker (plus si la
  machine le permet).
- Vérifier depuis un terminal Ubuntu (WSL) :

```bash
docker --version
docker run hello-world
```

### 6.3 Travailler dans le système de fichiers Linux

- Très important pour les performances : le code du projet doit être stocké DANS le système
  de fichiers Linux de WSL (ex. `/home/votre_nom/projets/…`) et non sur `/mnt/c/…` — sans
  quoi Odoo sera très lent.
- Pour naviguer dans votre environnement WSL, ouvrir une console (Terminal) sur le chemin
  `\\wsl$` ou bien cliquer sur l'icône Linux depuis l'Explorateur de fichiers.
- Ouvrir VS Code directement depuis le terminal WSL avec la commande `code .` (l'extension
  `WSL` connecte alors VS Code à l'environnement Linux).

## 7. Environnement Linux (natif)

- Suivre la procédure officielle :

```bash
sudo apt-get install -y curl
curl -fsSL https://get.docker.com -o install-docker.sh
sudo sh install-docker.sh
```

- Ajouter votre utilisateur au groupe docker (pour ne pas avoir à utiliser sudo à chaque
  commande), puis se déconnecter/reconnecter :

```bash
sudo usermod -aG docker $USER
```

- Vérifier :

```bash
docker --version
docker run hello-world
```

## 8. Outillage communautaire pour builder Odoo (depuis WSL ou Linux)

C'est un outillage professionnel qui sera utilisé en formation pour lancer un environnement
Odoo "prêt à l'emploi" (image Docker pré-construite avec Odoo + PostgreSQL + les modules
nécessaires).
L'installation manuelle "from source" (`git clone git@github.com/odoo/odoo` ...) sera
uniquement montrée à l'écran en théorie, car particulièrement chronophage à réaliser et
source de nombreuses erreurs (sans grande valeur ajoutée).

Nous suivons ci-dessous le `README.md` du repo suivant (et des sous-repos pointés) :
<https://github.com/akretion/docky-odoo-template-shared>.

### 8.1 Installer pipx (si pas déjà fait)

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```

### 8.2 Installer docky, copier et ak

```bash
pipx install docky
pipx install copier
pipx install git+https://github.com/akretion/ak --force --include-deps
```

- Vérifier les installations :

```bash
docky --version
ak --version
copier --version
```

### 8.3 Cloner le repository du gabarit de projet

- Créer un dossier de travail vide pour la formation. Vous pouvez remplacer "training" par
  ce que vous souhaitez, par exemple "odoo". Le cas échéant, pensez à remplacer "training"
  par votre choix dans les étapes suivantes.

```bash
mkdir ~/training && cd ~/training
```

- Générer le squelette du projet Docky à partir du template (très léger).
  Note : après ces 2 étapes, Odoo ne sera pas (encore) installé. Mais tous les outils et
  fichiers de configuration permettant d'installer les prérequis et Odoo seront prêts. Ce
  sont presque les "seules" 2 étapes utilisées pour démarrer professionnellement un nouveau
  projet client.

```bash
copier copy https://github.com/akretion/docky-odoo-template-shared .
```

> Réponses :
> Project Name : **training**
> Odoo Version : **19.0**

- Puis générer le fichier d'environnement personnel :

```bash
copier copy https://github.com/akretion/docky-odoo-template-personal .
```

> Réponses : tout laisser par défaut
> env : **dev**
> Project Name : **training**
> Subdomain : **training**
> Current branch : **19.0**

- Rajouter `UID=1000` dans le fichier d'environnement :
```bash
echo "UID=1000" >> .env
cat .env # affiche le contenu du fichier : vous devez trouver 'UID=1000' en dernière ligne
```

### 8.4 Installer et lancer `traefik`

Traefik est un reverse-proxy, au même titre que Nginx par exemple.
Son avantage est qu'il s'intégère bien avec Docker.
Il est utilisé et nécessaire en environnement de développement.

Pour l'installer, il faut télécharger un `docker-compose.yml` préconfiguré pour
Odoo et lancer le container en mode persistant.

```bash
cd ~/training
git clone https://github.com/akretion/traefik-template.git traefik
cd traefik
docker compose up -d
```

### 8.5 Télécharger le code Odoo et lancer l'environnement

**Cette étape est IMPÉRATIVEMENT à faire AVANT le 1er jour de formation et pas en salle, car
fortement dépendante de la connexion Internet.**
**Prévoir 5 min (bonne connexion) à 30 min voire plus (connexion Internet moins
performante).**

```bash
# Répertoire courant : doit être "~/.../training/odoo"
cd odoo

# Cette étape lance l'outil "ak" et créera 2 dossiers "external-src" et "links".
# AK va télécharger les sources Odoo et certains modules OCA depuis
# github.com/odoo/odoo et github.com/OCA/xxx.
ak build

# Builder Odoo ! (dépend de votre connexion : peut prendre 5 à 30 min)
cd ..
docky build
```

- Au premier lancement, docky télécharge l'image Odoo Docker de référence de la communauté
  Odoo : **odoo-template-shared**. Une majorité de projets Odoo communautaires sont basés
  sur cette image.
- "docky" est un outil Akretion qui fait "proxy" aux commandes docker, légèrement plus
  longues. C'est généralement un raccourci de "docker compose …".

Envie de lancer Odoo une 1ère fois ? Testez ces 2 dernières commandes (facultatif mais très
rapide) :

```bash
# Répertoire courant : doit être "~/.../training"
docky run  # Fait entrer dans le container

# Une fois dans le container
odoo -i base --stop-after-init --load-language=fr_FR
odoo  # C'est tout !
```

Si vous avez une erreur au `odoo -i base ...`, essayer ceci en première action de déboggage :
1. Sortir du container, et vous positionner dans le répertoire `training`
2. Supprimer le dossier `.db` avec : `rm -rf .db`
3. Reprendre le tutoriel à l'étape `docky run` (juste avant)

Puis ouvrir dans un navigateur : [http://training_19-0.localhost](http://training.localhost/).
Login : `admin` ; Password : `admin`.
Bravo d'être arrivé jusque là !

## 9. Récapitulatif — checklist finale avant le J-1

> **Windows**
> - WSL2 + Ubuntu 24.04 installés et fonctionnels
> - Docker Desktop installé, intégration WSL activée, `docker run hello-world` OK
> - VS Code + extensions Python / Docker / WSL
> - Git configuré, dans WSL
> - pipx, docky, ak, copier installés DANS WSL
> - Container "traefik" lancé en parallèle
> - Projet généré via copier + `docky run` et build testé au moins une fois avec succès
>   (important !)

> **Linux**
> - Docker Engine + Compose installés, utilisateur dans le groupe docker
> - VS Code (ou votre éditeur préféré) + extensions recommandées facultatives (Python,
>   Rainbow CSV, XML Tools)
> - Git configuré
> - pipx, docky, ak, copier installés
> - Container "traefik" lancé en parallèle
> - Projet généré via copier + `docky run` testé au moins une fois avec succès
>   (important !)

## 10. Références

Image Odoo : basée sur <https://github.com/acsone/odoo-bedrock>. D'autres outils conçus par
la société Acsone sont inclus dans l'image, notamment **click-odoo** et
**click-odoo-update**.

Image Odoo et outils utilisés pendant la formation :
<https://github.com/akretion/odoo-docker>.

La création de ce tutoriel a été assistée par l'intelligence artificielle, modèle Sonnet 5.
