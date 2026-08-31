#!/usr/bin/env bash
# ==============================================================================
# Odoo 19 — installation from source sur Ubuntu 24.04 LTS (Noble)
# Reference: https://www.odoo.com/documentation/19.0/administration/on_premise/source.html
# ------------------------------------------------------------------------------
# Usage : ./build_odoo_from_source_o19.sh [STEP]
#   STEP (optionnel, 1 par défaut) : numéro de l'étape à partir de laquelle
#   reprendre l'exécution. Les étapes précédentes sont ignorées (utile pour
#   relancer le script après une erreur sans tout refaire depuis le début).
#   Exemple : ./build_odoo_from_source_o19.sh 5
#
# Objectifs :
# - construire un environnement de développement manuellement
# - montrer ce qu'une image Docker Odoo fait "sous le capot"
#
# Ce que ce script fait :
# - installer les sources Odoo pour un environnement de développement
# - installer les prérequis d'infrastructure : postgresql et wkhtml2pdf
# - installer les prérequis applicatifs : binaires et librairies python
#
# Ce que ce script ne fait pas :
# - durcissement du serveur
# - reverse-proxy
# - systemd
#
# Dernier test le 20/08/2026 sur Ubuntu 24.04
# ==============================================================================

# ------------------------------------------------------------------------------
# 0. Setup
# ------------------------------------------------------------------------------
set -euo pipefail
# -e : stop whole script at 1st error
# -u : undeclared vars throws error instead of silently returning void
# -o pipefail : in a pipe (cmd1 | cmd2), throws an error even if cmd1 fails,
#               while by default bash only fails if cmd2 fails

STEP="${1:-1}"  # étape de départ (1 à 7), pour reprendre le script en cours de route

ODOO_VERSION="19.0"
ODOO_DIR="$HOME/dev/odoo/19.0/__src__/src"  # (i) personal choice / organization on your device
ODOO_DB_NAME=training
ODOO_USER_DB="odoo"
ODOO_USER_DB_PASSWORD="odoo"  # (i) only for DEV purpose
ODOO_REPO=https://github.com/odoo/odoo.git
# ODOO_REPO=https://github.com/oca/ocb.git  # Alternative OCB: avec les patchs communautaires en plus
WKHTMLTOPDF_VERSION="0.12.6.1-3"      # version patched-Qt recommandée par Odoo (toujours d'actualité en v19)

# ------------------------------------------------------------------------------
# 1. Dépendances système (Python, PostgreSQL, libs de compilation, Node.js)
# ------------------------------------------------------------------------------
step1() {
    sudo apt update && sudo apt upgrade -y

    # Python + outils de build + libs nécessaires aux paquets Python compilés
    # (psycopg2, python-ldap, lxml, gevent, Pillow, cryptography, ...)
    sudo apt install -y \
        python3-dev python3-pip python3-venv build-essential \
        libpq-dev libxml2-dev libxslt1-dev \
        libldap2-dev libsasl2-dev libssl-dev libffi-dev \
        libjpeg-dev zlib1g-dev libblas-dev libatlas-base-dev \
        git wget

    # PostgreSQL (serveur + client)
    sudo apt install -y postgresql
    sudo apt install -y postgresql-server-dev-16 # pour pgvector

    # Note : installer PostgreSQL de cette manière convient pour un environnement de
    # DEV mais pas en PROD. Le package PostgreSQL vient avec des configurations minimales
    # par défaut, alors que l'image Docker fourni un environnement PROD-ready.
    # Exemple de configurations plus adaptées :
    # https://github.com/PacktPublishing/Odoo-19-Development-Cookbook-6E/tree/main/Chapter01#11-postgresql-performance-tuning
}

# ------------------------------------------------------------------------------
# 2. wkhtmltopdf (obligatoire pour les rapports PDF QWeb)
# ------------------------------------------------------------------------------
step2() {
    # /!\ NE PAS installer via "apt install wkhtmltopdf" : le paquet des dépôts
    # Ubuntu n'est plus tenu à jour et Odoo S.A. a repris le projet
    # Attention à la version de wkhtml2pdf: elle peut varier selon la version de Odoo
    WKHTML_DEB="/tmp/wkhtmltox_${WKHTMLTOPDF_VERSION}.jammy_amd64.deb"
    wget -q "https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTMLTOPDF_VERSION}/wkhtmltox_${WKHTMLTOPDF_VERSION}.jammy_amd64.deb" -O "$WKHTML_DEB"
    sudo apt install -y "$WKHTML_DEB" # La syntaxe "apt install ./file.deb" permet de résoudre les dépendances (ici: xfonts)
    rm -f "$WKHTML_DEB"
    wkhtmltopdf --version
}

# ------------------------------------------------------------------------------
# 3. Rôle et base PostgreSQL pour Odoo
# ------------------------------------------------------------------------------
step3() {
    # You will be prompted here. Type the password defined in $ODOO_USER_DB_PASSWORD
    sudo -u postgres createuser --createdb --login --pwprompt "$ODOO_USER_DB"
}

# ------------------------------------------------------------------------------
# 4. Code source Odoo (branche 19.0, clone superficiel pour aller vite)
# ------------------------------------------------------------------------------
step4() {
    git clone $ODOO_REPO "$ODOO_DIR" -b "$ODOO_VERSION" --single-branch --depth=1
}

# ------------------------------------------------------------------------------
# 5. Environnement virtuel Python + dépendances
# ------------------------------------------------------------------------------
step5() {
    python3 -m venv "$ODOO_DIR/venv"
    source "$ODOO_DIR/venv/bin/activate"

    # Update pip
    pip install -U pip

    # Installe les dépendances Python (librairies via pip)
    pip install -r "$ODOO_DIR/requirements.txt"

    # Dépendances des modules hors du natif Odoo CE
    # Optionnel pour la formation, nous n'en aurons pas besoin
    # Il s'agit uniquement d'exemples pour indiquer la complexité de maintenance
    pip install sentry-sdk pyjwt "factur-x>=6.7" mock numpy openpyxl \
        pycountry pyfrdas2 "pyfrctc>=0.15" python-slugify==4.0.0 \
        requests_oauthlib unidecode phonenumbers pypdf python-barcode \
        xlsxwriter xlrd "python-stdnum>=1.16" markdown pysaml2 \
        pygments pre-commit oca-decorators openupgradelib odoo_test_helper \
        flake8 cachetools

    # Outils de maintenance
    pip install click-odoo-contrib

    # Outils de dev (facultatif, pas pour une PROD)
    pip install ipdb watchdog

    # Installation de 'pg-vector' (PostgreSQL >= 15) pour utiliser les features AI de Odoo
    # Optionnel pour la formation
    # Référence : https://github.com/pgvector/pgvector#installation-notes---linux-and-mac
    cd /tmp
    git clone https://github.com/pgvector/pgvector.git
    cd pgvector
    make
    sudo make install

    # Installe la commande "odoo-bin" / "odoo" dans le venv
    pip install -e "$ODOO_DIR"
    odoo --version
}

# ------------------------------------------------------------------------------
# 6. Fichier de configuration minimal
# ------------------------------------------------------------------------------
step6() {
    # Générer un modèle de fichier de config
    cd "$ODOO_DIR"
    odoo -c odoo.conf -s --stop-after-init

    # Editer le fichier de configuration
    nano odoo.conf  # 'nano' ou votre éditeur préféré (vim, micro, ...)

    # Modifier les variables à l'intérieur du fichier comme suit :
    # addons_path = ./odoo/addons,./addons
    # db_host = localhost
    # db_name = ${ODOO_DB_NAME}  # Odoo n'interprétera pas les variables : les remplacer en dur
    # db_user = ${ODOO_USER_DB}
    # db_password = ${ODOO_USER_DB_PASSWORD}
    # logfile = False  # This will outputs logs to the shell, pratical in DEV
    # workers = 0 # needed in DEV, else it requires a reverse-proxy like Nginx
}

# ------------------------------------------------------------------------------
# 7. Initialisation d'une première base et lancement
# ------------------------------------------------------------------------------
step7() {
    # Regardons d'abord rapidement la documentation de la commande 'odoo'
    # Les arguments passés à la commande permettent des options similaires mais pas
    # exhaustivement équivalent aux variables du fichier de configuration 'odoo.conf'
    odoo --help

    # Le paramètre 'addons_path' est interprété depuis le dossier courant (relatif)
    cd "$ODOO_DIR" # Pour s'assurer que le répertoire courant est le bon

    # Initialiser une database 'training', avec le module 'base' uniquement
    odoo -c odoo.conf -d ${ODOO_DB_NAME} -i base --without-demo=all --stop-after-init --load-language=fr_FR

    echo "Bravo ! L'installation terminée"
    echo "Ouvrir http://localhost:8069"
    echo "Login : admin/admin"
}

# ------------------------------------------------------------------------------
# Exécution : démarrer à l'étape $STEP
# ------------------------------------------------------------------------------
if ! [[ "$STEP" =~ ^[1-7]$ ]]; then
    echo "STEP invalide : '$STEP' (attendu un nombre entre 1 et 7)" >&2
    exit 1
fi

# En cas de reprise à partir de l'étape 6 ou 7, le venv de l'étape 5 existe déjà
# sur le disque mais n'a pas été (re)activé dans ce shell : on le réactive ici.
if (( STEP > 5 )) && [[ -f "$ODOO_DIR/venv/bin/activate" ]]; then
    source "$ODOO_DIR/venv/bin/activate"
    cd $ODOO_DIR
fi

for n in 1 2 3 4 5 6 7; do
    if (( n >= STEP )); then
        echo "######### ETAPE $n ############"
        "step${n}"
    fi
done
