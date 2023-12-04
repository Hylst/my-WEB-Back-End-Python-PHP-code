from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from .models import Task, Tag

# 04/12/2023 - Geoffroy
# TP2 V2 - Dashboard avec statistiques et kanban-style

def dashboard(request):
    """Vue principale style kanban."""
    tasks_by_status = {
        'todo': Task.objects.filter(status='todo', parent__isnull=True),
        'in_progress': Task.objects.filter(status='in_progress', parent__isnull=True),
        'done': Task.objects.filter(status='done', parent__isnull=True),
    }
    
    # Statistiques
    stats = {
        'total': Task.objects.filter(parent__isnull=True).count(),
        'overdue': sum(1 for t in Task.objects.filter(parent__isnull=True) if t.is_overdue),
        'completed_today': Task.objects.filter(
            completed_at__date=timezone.now().date()
        ).count() if 'timezone' in dir() else 0,
    }
    
    tags = Tag.objects.annotate(task_count=Count('tasks'))
    
    return render(request, 'todo/dashboard.html', {
        'tasks_by_status': tasks_by_status,
        'stats': stats,
        'tags': tags,
        'priorities': Task.PRIORITY_CHOICES,
    })

def index(request):
    """Liste classique avec filtres avancés."""
    tasks = Task.objects.filter(parent__isnull=True)
    
    # Filtres
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    tag = request.GET.get('tag')
    search = request.GET.get('q')
    
    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=int(priority))
    if tag:
        tasks = tasks.filter(tags__name=tag)
    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    # Création rapide
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            priority = request.POST.get('priority', 3)
            due_date = request.POST.get('due_date') or None
            Task.objects.create(title=title, priority=priority, due_date=due_date)
            messages.success(request, f"✅ '{title}' ajouté")
        return redirect('index')
    
    return render(request, 'todo/index.html', {
        'tasks': tasks,
        'tags': Tag.objects.all(),
        'priorities': Task.PRIORITY_CHOICES,
        'statuses': Task.STATUS_CHOICES,
    })

def update_status(request, task_id, new_status):
    """Change le statut d'une tâche (pour drag & drop)."""
    task = get_object_or_404(Task, pk=task_id)
    if new_status == 'done':
        task.complete()
    else:
        task.status = new_status
        task.save()
    messages.info(request, f"Tâche mise à jour")
    return redirect('index')

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    title = task.title
    task.delete()
    messages.success(request, f"'{title}' supprimé")
    return redirect('index')

def add_subtask(request, parent_id):
    """Ajoute une sous-tâche."""
    parent = get_object_or_404(Task, pk=parent_id)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Task.objects.create(title=title, parent=parent, priority=parent.priority)
            messages.success(request, "Sous-tâche ajoutée")
    return redirect('index')

# Import manquant
from django.utils import timezone
