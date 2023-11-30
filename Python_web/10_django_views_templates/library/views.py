from django.shortcuts import render
from .models import Livre

# 30/11/2023 - Geoffroy
# Les Vues.
# C'est l'équivalent des routes Flask, mais souvent encapsulé.
# Ici on fait le lien entre la base de données (Models) et l'utilisateur (Templates).
# C'est le chef d'orchestre.

def index(request):
    # On récupère tous les livres. Imaginons une grande bibliothèque.
    livres = Livre.objects.all()
    context = {'livres': livres}
    # On rend le template en lui passant les données (le context).
    return render(request, 'library/index.html', context)
