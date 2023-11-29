from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# 29/11/2023 - Geoffroy
# Modèles V2 - Relations et méthodes personnalisées
# J'ai ajouté un modèle Auteur pour montrer les ForeignKey.
# Plus des propriétés calculées et des validateurs. C'est plus "vrai" comme ça.

class Auteur(models.Model):
    """Représente un auteur de livres."""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    biographie = models.TextField(blank=True)
    
    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class Livre(models.Model):
    """Représente un livre de la bibliothèque."""
    
    GENRES = [
        ('FANTASY', 'Fantasy'),
        ('SCIFI', 'Science-Fiction'),
        ('THRILLER', 'Thriller'),
        ('ROMAN', 'Roman'),
        ('ESSAI', 'Essai'),
        ('AUTRE', 'Autre'),
    ]
    
    titre = models.CharField(max_length=200)
    auteur = models.ForeignKey(
        Auteur, 
        on_delete=models.CASCADE,
        related_name='livres'
    )
    genre = models.CharField(max_length=20, choices=GENRES, default='AUTRE')
    resume = models.TextField(blank=True)
    date_publication = models.DateField()
    note = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    disponible = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
    
    def __str__(self):
        return f"{self.titre} ({self.auteur})"
    
    @property
    def est_recent(self):
        """Retourne True si le livre a moins de 2 ans."""
        deux_ans = timezone.now().date() - timezone.timedelta(days=730)
        return self.date_publication > deux_ans
    
    @property
    def etoiles(self):
        """Retourne la note sous forme d'étoiles."""
        return "⭐" * self.note + "☆" * (5 - self.note)
    
    def emprunter(self):
        """Marque le livre comme emprunté."""
        if not self.disponible:
            raise ValueError("Ce livre est déjà emprunté!")
        self.disponible = False
        self.save()
    
    def retourner(self):
        """Marque le livre comme disponible."""
        self.disponible = True
        self.save()
