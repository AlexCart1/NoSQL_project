
# Projet NoSQL 2025

Projet NoSQL 2025 - ESIEA 4 année
Objectifs: Maitrîser MongoDB, Noe4j, une interface **Streamlit** pour visualiser les résultats des différentes analyses. Le traitement de base de données depuis Python. Il faut mettre en place un projet disponible sur github, contenant des codes pythons tels que des queries.py, un main, des import de data et bien d'autre fichiers encore...



## Installation

0. **Environnement de travail** :
   - Téléchargez **[Visual Studio Code (VSCode)](https://code.visualstudio.com/)**
   - Installez les extensions suivantes dans VSCode :
     - **Python**
     - **MongoDB for VSCode**
     - **Neo4j** (pour interagir avec Neo4j directement depuis VSCode)

1. **Télécharger le projet** :
   - Créez un dossier, ouvrez le terminal dans ce dossier.
   - Clonez le projet avec la commande suivante :
     ```bash
     git clone https://github.com/AlexCart1/NoSQL_project.git
   - Ou téléchargez le projet en fichier .zip depuis GitHub et décompressez-le dans un dossier.

2. **Créer son environnement de travail** :
   - Ouvrez un terminal dans VSCode et naviguez jusqu'au dossier de votre projet. Ensuite, créez un environnement virtuel Python en exécutant la commande suivante :
     ```bash
     python -m venv .venv
     ```

3. **Activer l'environnement virtuel** :
   - **Sous Windows** : activer la venv
     ```bash
     .venv\Scripts\activate
     ```
   - **Sous macOS/Linux** : activer la venv
     ```bash
     source .venv/bin/activate
     ```

4. **Installer les dépendances** :
   - Avec l'environnement virtuel activé, installez toutes les dépendances nécessaires avec la commande suivante :
     ```bash
     pip install -r requirements.txt
     ```

## Exécution du projet

### 1. Lancer le programme principal (`main.py`)

Une fois l'environnement virtuel activé et les dépendances installées, lancer le programme principal avec la commande suivante dans le terminal vscode :
```bash
python main.py
```

### 2. Lancer le streamlit qui va ouvrir un nouveau browser
```bash
python launch_dashboard.py
```

