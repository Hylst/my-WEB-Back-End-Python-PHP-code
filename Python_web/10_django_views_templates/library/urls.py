from django.urls import path
from . import views

# 30/11/2023 - Geoffroy
# Les URLs de l'app 'library'.
# On map l'URL racine de l'app vers la vue index.

urlpatterns = [
    path('', views.index, name='index'),
]
