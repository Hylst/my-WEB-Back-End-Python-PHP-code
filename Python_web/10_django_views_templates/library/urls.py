from django.urls import path
from . import views

# 30/11/2023 - Geoffroy
# URLs mises à jour pour les CBV

urlpatterns = [
    path('', views.LivreListView.as_view(), name='index'),
    path('livre/<int:pk>/', views.LivreDetailView.as_view(), name='detail'),
    path('stats/', views.stats_view, name='stats'),
]
