# Visualisation des Prénoms en France

Ce projet utilise Dash pour créer des visualisations interactives des prénoms les plus populaires en France de 1900 à 2020. Le projet est divisé en trois visualisations distinctes, chacune répondant à différentes questions sur les données des prénoms.

## Description du Projet

Nous travaillons avec un ensemble de données sur les prénoms en France, contenant la liste de tous les prénoms enregistrés en France, année par année, de 1900 à 2020. Il y a deux ensembles de données : l'un agrégé au niveau national et l'autre avec des données par département. Notre objectif est de créer 3 visualisations différentes autour de ces données, chacune se concentrant sur différents types de questions concernant les données :

### Visualisation 1: 
Comment les prénoms évoluent-ils au fil du temps ? Y a-t-il des prénoms qui sont restés constamment populaires ou impopulaires ? Y en a-t-il qui ont été soudainement ou brièvement populaires ou impopulaires ? Y a-t-il des tendances temporelles ?

### Visualisation 2:
Y a-t-il un effet régional dans les données ? Certains prénoms sont-ils plus populaires dans certaines régions ? Les prénoms populaires sont-ils généralement populaires dans tout le pays ?

### Visualisation 3:
Y a-t-il des effets de genre dans les données ? La popularité des prénoms donnés aux deux sexes évolue-t-elle de manière cohérente ?

## Composition du groupe R

- Louis Lemoine
- Victor Rivière
- Mathieu Sauveur
- Salimatou Traore
- Yuchen Xia

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- Python 3.7 ou une version ultérieure
- pip (Python package installer)

## Installation

1. Clonez le repository ou téléchargez les fichiers de projet.

```bash
git clone https://github.com/matsvr/Vizualisation_project.git
cd Vizualisation_project
```

2. Installez les dépendances nécessaires :

```bash
pip install dash pandas plotly holoviews hvplot bokeh wordcloud matplotlib
```

## Utilisation

1. Déplacez-vous dans le répertoire `Initial Implementation` :

2. a) Visualization 1

- Accédez au dossier Initial Implementation/ puis lancez la commande python ci-dessous :
  
```bash
cd Initial\ Implementation
python Visualisation1.py
```

- Ouvrez votre navigateur web et accédez à l'adresse suivante :

```
http://127.0.0.1:8050/
```

2. b) Visualization 2

- Accédez au dossier Initial Implementation/ puis lancez la commande python ci-dessous :
  
```bash
cd Initial\ Implementation
python Visualisation1.py
```

- Ouvrez votre navigateur web et accédez à l'adresse suivante :

```
http://127.0.0.1:8055/
```
- Pour la Visualisation avec les DOM-TOM
```
http://127.0.0.1:8056/
```




2. c) Visualization 3a

- Accédez au dossier Initial Implementation/ :
  
```bash
cd Initial\ Implementation
```
- Lancez un serveur Bokeh avec la commande ci-après qui vous permettra d'accéder à la visualisation :

```
bokeh serve --show Visualization3a.py
```

- Il est aussi possible de lancer la visualisation dans un Notebook Jupyter en lançant le fichier Visualization3a.ipynb

- Dans ce Notebook vous pouvez soit générer une visualisation intéractive (Partie 1) ou encore créer une animation GIF de la visualisation en question sur un certain nombre d'années prédéfini (Partie 2) 

2. d) Visualization 3b

- Accédez au dossier Initial Implementation/ :
  
```bash
cd Initial\ Implementation
```

- Exécutez les cellules du Notebook Jupyter Visualization3b.ipynb

## Structure du Projet

- `Initial Implementation/` : Contient les premières versions des visualisations.
- `Refined solution/` : Contient les versions finales et raffinées des visualisations.
- `Sketch/` : Contient les esquisses et les conceptions initiales des visualisations.
- `dpt2020.csv` : Le fichier CSV contenant les données des prénoms.
- `departements-avec-outre-mer.geojson` et `departements-version-simplifiee.geojson` : Fichiers GeoJSON utilisés pour les visualisations régionales.

## Fonctionnalités

- **Visualisation 1** : 
  - Filtrage par Sexe : Vous pouvez filtrer les prénoms par sexe (Tous, Garçons, Filles).
  - Filtrage par Département : Vous pouvez filtrer les prénoms par département.
  - Filtrage par Popularité : Vous pouvez filtrer les prénoms par popularité (Les plus populaires, Les moins populaires).
  - Course de Barres : Visualisation dynamique des prénoms les plus populaires au fil du temps avec une animation de course de barres.
  
- **Visualisation 2** : 
  - Cette visualisation nous permet de pouvoir afficher les prénoms les plus populaires pour chacuns des départements. 
  - Un filtrage par année avec une liste déroulante, la carte se met à jour pour afficher les départements colorés en fonction du nombre d'occurrences du prénom le plus fréquent.
  - Un modal apparait lors du passage de la souris sur le département, listant (nom du département, code du département, prénom le plus représenté et son nombre)
  - Un tableau listant les 50 prénoms les plus représenter pour l'année séléectionnée.
  
- **Visualisation 3a** :
  - Cette visualisation permet de pouvoir afficher les prénoms les plus communs pour chaque sexe en fonction de l'année et du département
  - La visualisation s'oriente autour de deux nuages de mots (un pour les prénoms masculins et un autre pour les prénoms féminins) dans lesquels plus un nom est commun plus celui-ci aura une police de grande taille
  - On doit donc d'abord sélectionner l'année voulue
  - Puis sélectionner le département voulu (si cela est nécessaire), celui-ci étant initialisé sur l'option "Tous les départements"

- **Visualisation 3b** :
  - Cette visualisation permet d'afficher les prénoms les plus communs pour chaque sexe en fonction de l'année
  - La visualisation est un 'BarPolar' scindé en 2, identifié par des couleurs bleu et orange pour différencier les sexes. Plus la barre est longue plus le prénom associé a été attribué lors de l'année représentée.
  - Il suffit de cliquer sur play afin de visualiser une années après l'autre à la manière d'un diaporama. On voit donc l'évolution des attributions des noms au fil des années.
  - On peut aussi sélectionner une année précise à l'aide du 'slider' en dessous du graph.

