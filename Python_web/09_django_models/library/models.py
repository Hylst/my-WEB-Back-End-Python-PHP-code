from django.db import models

# 29/11/2023 - Geoffroy
# Les Modèles.
# C'est ici qu'on définit les règles de l'univers.
# Plus besoin d'écrire du SQL à la main (CREATE TABLE...), Django le fait pour nous.
# C'est comme avoir un intendant qui gère l'inventaire.

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    resume = models.TextField(blank=True)
    date_publication = models.DateField()
    
    # "Magic method" pour que l'affichage soit lisible.
    def __str__(self):
        return f"{self.titre} (par {self.auteur})"
