from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Livre

# 30/11/2023 - Geoffroy
# Vues V2 - Passage aux Class-Based Views (CBV)
# C'est plus Django-esque et plus maintenable à long terme.
# Ajout aussi d'une recherche basique.

class LivreListView(ListView):
    """Liste paginée des livres avec recherche."""
    model = Livre
    template_name = 'library/index.html'
    context_object_name = 'livres'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(titre__icontains=search) | 
                Q(auteur__nom__icontains=search) |
                Q(auteur__prenom__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['total_count'] = Livre.objects.count()
        return context


class LivreDetailView(DetailView):
    """Détail d'un livre avec ses infos complètes."""
    model = Livre
    template_name = 'library/detail.html'
    context_object_name = 'livre'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Livres du même auteur
        context['autres_livres'] = Livre.objects.filter(
            auteur=self.object.auteur
        ).exclude(pk=self.object.pk)[:5]
        return context


# Fonction-based view pour les stats (alternative aux CBV)
def stats_view(request):
    """Statistiques de la bibliothèque."""
    from django.db.models import Count, Avg
    
    stats = {
        'total_livres': Livre.objects.count(),
        'livres_disponibles': Livre.objects.filter(disponible=True).count(),
        'note_moyenne': Livre.objects.aggregate(Avg('note'))['note__avg'] or 0,
        'par_genre': Livre.objects.values('genre').annotate(count=Count('id')),
    }
    return render(request, 'library/stats.html', {'stats': stats})
