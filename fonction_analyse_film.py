
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd



def resumer_notes_par_anciennete(ratings_movies):
    """Une ligne par film et ancienneté, avec somme, moyenne et nombre de notes."""
    # On copie seulement les colonnes utiles pour limiter la mémoire utilisée.
    notes = ratings_movies[["movieId", "rating"]].copy()
    # On mesure un écart entre années civiles, pas une durée au jour près.
    notes["tranche_anciennete"] = (
        pd.to_datetime(ratings_movies["date"], errors="coerce").dt.year
        - pd.to_numeric(ratings_movies["year"], errors="coerce")
    )
    # On écarte les dates manquantes et les notes antérieures à l'année de sortie.
    notes = notes.dropna(subset=["tranche_anciennete"])
    notes = notes.loc[notes["tranche_anciennete"] >= 0].copy()
    notes["tranche_anciennete"] = notes["tranche_anciennete"].astype(int)
    # Les sommes et effectifs permettront de regrouper plusieurs années correctement.
    return (
        notes.groupby(["movieId", "tranche_anciennete"])["rating"]
        .agg(moyenne_film="mean", somme_notes="sum", nombre_notes="count")
        .reset_index()
    )


def tracer_notes_par_anciennete(par_film, seuil_notes=1000):
    """Comparer les deux pondérations, avec les volumes de notes et de films."""
    # On réutilise la table agrégée, sans revenir aux millions de notes individuelles.
    resume = par_film.groupby("tranche_anciennete").agg(
        moyenne_par_film=("moyenne_film", "mean"),
        somme_notes=("somme_notes", "sum"),
        nombre_notes=("nombre_notes", "sum"),
        nombre_films=("movieId", "count"),
    ).sort_index()
    # La somme divisée par le nombre de notes donne le même poids à chaque note.
    resume["moyenne_par_note"] = resume["somme_notes"] / resume["nombre_notes"]
    # Le seuil masque les moyennes peu documentées ; les volumes restent affichés.
    assez_de_notes = resume["nombre_notes"] >= seuil_notes
    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True, constrained_layout=True)

    # Le premier panneau compare les deux façons de pondérer les films.
    for colonne, label, couleur in [
        ("moyenne_par_film", "Chaque film pèse autant", "#2878B5"),
        ("moyenne_par_note", "Chaque note pèse autant", "#E07B39"),
    ]:
        resume[colonne].where(assez_de_notes).plot(
            ax=axes[0], marker="o", markersize=3, label=label, color=couleur
        )
    axes[0].set_title(f"Notes moyennes par ancienneté (au moins {seuil_notes:,} notes)")
    axes[0].set_ylabel("Note moyenne (axe zoomé)")
    axes[0].legend()

    # Les deux autres panneaux montrent les nombres de notes et de films distincts.
    for ax, colonne, titre, couleur in [
        (axes[1], "nombre_notes", "Nombre de notes", "#7BAFD4"),
        (axes[2], "nombre_films", "Nombre de films distincts", "#F2B880"),
    ]:
        ax.bar(resume.index, resume[colonne], color=couleur)
        ax.set_ylabel(titre)
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda valeur, _: f"{valeur:,.0f}".replace(",", " "))
        )
    # On précise l'abscisse sur chaque panneau malgré le partage du même axe.
    for ax in axes:
        ax.grid(axis="y", alpha=0.3)
        ax.set_axisbelow(True)
        ax.set_xlabel("Ancienneté du film au moment de la note (années)")
        ax.xaxis.label.set_visible(True)
        ax.tick_params(axis="x", labelbottom=True)
    # Une graduation tous les dix ans évite de surcharger le graphique.
    axes[2].set_xticks(range(0, int(resume.index.max()) + 1, 10))
    plt.show()


def construire_table_periodes(par_film, movies_with_date, periodes, annee_min, annee_max):
    """Une ligne par film, avec sa moyenne et son effectif dans chaque fenêtre."""
    # On sélectionne la cohorte de sortie en gardant une seule ligne par film.
    table = movies_with_date.loc[
        movies_with_date["year"].between(annee_min, annee_max),
        ["movieId", "title", "year", "genres"],
    ].copy()
    # On ne conserve les notes agrégées que pour les films de cette cohorte.
    notes = par_film.merge(table[["movieId"]], on="movieId", validate="many_to_one")
    # Chaque fenêtre donne une moyenne et un nombre de notes pour chaque film.
    for nom, debut, fin in periodes:
        resume = (
            notes.loc[notes["tranche_anciennete"].between(debut, fin)]
            .groupby("movieId")
            .agg(somme_notes=("somme_notes", "sum"), nombre_notes=("nombre_notes", "sum"))
            .reset_index()
        )
        # On additionne d'abord les sommes et les effectifs de toutes les années.
        # Leur quotient évite de donner autant de poids à une année peu notée.
        resume[f"note_{nom}"] = resume["somme_notes"] / resume["nombre_notes"]
        resume = resume.rename(columns={"nombre_notes": f"nb_notes_{nom}"})
        # La jointure à gauche garde les films sans notes dans une fenêtre.
        # Le notebook applique ensuite le minimum de notes dans chaque période.
        table = table.merge(
            resume[["movieId", f"note_{nom}", f"nb_notes_{nom}"]],
            on="movieId", how="left", validate="one_to_one",
        )
    return table


def tracer_trajectoire(comparaison_films, periodes):
    """Tracer les moyennes de fenêtres pour le même ensemble de films."""
    # Chaque point repose sur les mêmes films, avec un poids égal pour chacun.
    resume = []
    for nom, debut, fin in periodes:
        resume.append({
            "periode": f"{debut}–{fin} ans",
            "centre": (debut + fin) / 2,
            "note_moyenne": comparaison_films[f"note_{nom}"].mean(),
            "nombre_films": len(comparaison_films),
            "nombre_notes": int(comparaison_films[f"nb_notes_{nom}"].sum()),
        })
    resume = pd.DataFrame(resume)
    # Les points sont placés au centre des fenêtres pour respecter leur espacement.
    # Les segments relient des moyennes de périodes, pas des observations annuelles.
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(resume["centre"], resume["note_moyenne"], marker="o", color="#2878B5")
    ax.set_xticks(resume["centre"], resume["periode"])
    ax.set_title("Trajectoire moyenne du même ensemble de films")
    ax.set_xlabel("Ancienneté au moment de la notation")
    ax.set_ylabel("Note moyenne (axe zoomé)")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()
    # On renvoie aussi le résumé des moyennes et des effectifs affiché dans le notebook.
    return resume.drop(columns="centre")