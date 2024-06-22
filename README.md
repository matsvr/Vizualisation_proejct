# Visualisation des Prénoms en France

Ce projet utilise Dash pour créer des visualisations interactives des prénoms les plus populaires en France de 1900 à 2020. Le projet est divisé en trois visualisations distinctes, chacune répondant à différentes questions sur les données des prénoms.

## Description du Projet

Nous travaillons avec un ensemble de données sur les prénoms en France, contenant la liste de tous les prénoms enregistrés en France, année par année, de 1900 à 2020. Il y a deux ensembles de données : l'un agrégé au niveau national et l'autre avec des données par département. Notre objectif est de créer 3 visualisations différentes autour de ces données, chacune se concentrant sur différents types de questions concernant les données :

### Visualisation 1: 
Comment les prénoms évoluent-ils au fil du temps ? Y a-t-il des prénoms qui sont restés constamment populaires ou impopulaires ? Y en a-t-il qui ont été soudainement ou brièvement populaires ou impopulaires ? Y a-t-il des tendances temporelles ?

### Visualisation 2:
Y a-t-il un effet régional dans les données ? Certains prénoms sont-ils plus populaires dans certaines régions ? Les prénoms populaires sont-ils généralement populaires dans tout le pays ?

### Visualisation 3:
Y a-t-il des effets de genre dans les données ? La popularité des prénoms donnés aux deux sexes évolue-t-elle de manière cohérente ? (Note : cet ensemble de données traite le sexe de manière binaire ; il s'agit d'une simplification qui est utilisée dans ce projet, mais qui n'est généralement pas valable.)

## Participants au Projet

- Louis Lemoine
- Victor Rivière
- Matthieu Sauveur
- Salimatou Traore
- Yuchen Xia

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- Python 3.7 ou une version ultérieure
- pip (Python package installer)

## Installation

1. Clonez le repository ou téléchargez les fichiers de projet.

```bash
git clone [https://github.com/votre-utilisateur/votre-repository.git](https://github.com/matsvr/Vizualisation_project.git)
cd Vizualisation_project
```

2. Installez les dépendances nécessaires :

```bash
pip install dash pandas plotly
```

## Utilisation

1. Placez votre fichier `dpt2020.csv` dans le même répertoire que le fichier `app.py`.

2. Exécutez le script `app.py` :

```bash
python app.py
```

3. Ouvrez votre navigateur web et accédez à l'adresse suivante :

```
http://127.0.0.1:8050/
```

## Structure du Projet

- `Initial Implementation/` : Contient les premières versions des visualisations.
- `Refined solution/` : Contient les versions finales et raffinées des visualisations.
  - `app.py` ou `Viz.py` : Les scripts principaux qui contiennent le code de l'application Dash pour la visualisation.
- `Sketch/` : Contient les esquisses et les conceptions initiales des visualisations.
- `dpt2020.csv` : Le fichier CSV contenant les données des prénoms.
- `departements-avec-outre-mer.geojson` et `departements-version-simplifiee.geojson` : Fichiers GeoJSON utilisés pour les visualisations régionales.
- `README.md` : Ce fichier, contenant des instructions sur l'installation et l'utilisation du projet.

## Fonctionnalités

- **Visualisation 1** : 
  - Filtrage par Sexe : Vous pouvez filtrer les prénoms par sexe (Tous, Garçons, Filles).
  - Filtrage par Département : Vous pouvez filtrer les prénoms par département.
  - Course de Barres : Visualisation dynamique des prénoms les plus populaires au fil du temps avec une animation de course de barres.
  
- **Visualisation 2** : 
  - (À compléter selon les fonctionnalités de la visualisation 2)
  
- **Visualisation 3** : 
  - (À compléter selon les fonctionnalités de la visualisation 3)
