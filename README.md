# ensae_pythondatascience_films

# Projet Python pour la Data Science

*Auteurs : Alma El Karoui et Gabriel Courtadon — ENSAE Paris, 2026.*

## Sujet : Comment note-t-on un film ?

Une note moyenne semble résumer l’appréciation d’un film. Elle dépend pourtant aussi du public qui le choisit, de ses habitudes et du moment où il le note.

**Problématique :** que révèle une note MovieLens du film, de l’utilisateur et des conditions de notation, et notamment comment évolue-t-elle avec l’ancienneté du notant et du film ?

## Données

Nous utilisons [MovieLens 32M](https://grouplens.org/datasets/movielens/32m/), une base publique fournie par GroupLens : environ **32 millions de notes**, attribuées par **200 948 utilisateurs** à **87 585 films**, entre 1995 et 2023.

L’analyse repose principalement sur deux fichiers, joints par l’identifiant `movieId` :

- `movies.csv` : titres et genres des films ;
- `ratings.csv` : notes, utilisateurs et dates de notation.

Les fichiers `tags.csv` et `links.csv`, également présents dans l’archive, ne sont pas exploités dans les analyses.

## Démarche

Le notebook présente successivement :

1. Le nettoyage, la jointure et les statistiques descriptives des données.
2. L’évolution des notes et de leur dispersion avec l’ancienneté des utilisateurs (**IV.A**), en comparant aussi les mêmes personnes.
3. L’évolution des notes avec l’ancienneté des films (**IV.B**), puis les trajectoires d’une cohorte fixe.
4. Trois régressions descriptives sur la variation tardive des notes, intégrant progressivement les caractéristiques des films, leur réception initiale et l’évolution du volume de notations.

Les résultats sont interprétés comme des **associations**, sans établir de liens causaux.

## Reproduction du projet

**Installation.** Depuis un terminal, dans un environnement Python dédié :

```bash
git clone https://github.com/gcourtadon/ensae_pythondatascience_films.git
cd ensae_pythondatascience_films
python -m pip install pandas numpy matplotlib seaborn requests statsmodels jupyterlab ipykernel
```

**Lancement.** Depuis la racine du projet :

```bash
python -m jupyterlab main.ipynb
```

Sélectionner le noyau de l’environnement utilisé, puis **redémarrer le noyau et exécuter toutes les cellules dans l’ordre**.

Le notebook télécharge l’archive officielle, d’environ **240 Mo**, puis extrait les fichiers dans `data/ml-32m/`. Les données restent stockées localement et ne sont pas versionnées dans Git. Le traitement des 32 millions de notes peut nécessiter plusieurs Go de mémoire vive.

## Structure du dépôt

- **`main.ipynb`** : rapport principal, comprenant les traitements, les graphiques, les interprétations et la conclusion générale.
- **`donnees.py`** : fonctions de téléchargement et d’extraction des données.
- **`fonction_analyse_film.py`** : fonctions d’agrégation, de visualisation et de préparation des analyses de la partie IV.B.
- **`data/`** : dossier créé lors de l’exécution pour accueillir les données téléchargées.