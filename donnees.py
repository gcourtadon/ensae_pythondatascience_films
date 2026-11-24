##faire installer toutes les dependances : sur quel env va t on executer ? 
import os
import zipfile
import pandas as pd

URL = "https://files.grouplens.org/datasets/movielens/ml-32m.zip"
NOM_ZIP = "ml-32m.zip"
DOSSIER = "data"

def telecharger(url, nom_fichier):
    """Télécharge le fichier à l'adresse url (par morceaux, car il est lourd)."""
    if os.path.exists(nom_fichier):
        print("Le ZIP existe déjà, pas de nouveau téléchargement.")
        return
    reponse = requests.get(url, stream=True)
    reponse.raise_for_status()
    with open(nom_fichier, "wb") as f:
        for morceau in reponse.iter_content(chunk_size=1024 * 1024):
            f.write(morceau)
    print("Téléchargement terminé.")


def extraire(nom_zip, dossier):
    """Dézippe l'archive dans le dossier indiqué."""
    with zipfile.ZipFile(nom_zip) as archive:
        print("Contenu du ZIP :", archive.namelist())
        archive.extractall(dossier)


# TELECHARGEMENT LOCAL EN CAS DE BUG (solution de secours)

#DOSSIER_CSV = "ml-32m"

# Si les CSV sont dans un sous-dossier, on le prend

#import os
#import pandas as pd
#movies = pd.read_csv(os.path.join(DOSSIER_CSV, "movies.csv"))
#tags = pd.read_csv(os.path.join(DOSSIER_CSV, "tags.csv"))
#links = pd.read_csv(os.path.join(DOSSIER_CSV, "links.csv"))
#ratings = pd.read_csv(os.path.join(DOSSIER_CSV, "ratings.csv"))

#display(movies.head())
#display(ratings.shape)
