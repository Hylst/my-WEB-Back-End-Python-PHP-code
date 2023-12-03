from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task

# 03/12/2023 - Geoffroy
# TP2 V1 - Vues améliorées avec messages et filtres

def index(request):
    filter_type = request.GET.get('filter', 'all')
    priority = request.GET.get('priority')
    
    tasks = Task.objects.all()
    
    # Filtres
    if filter_type == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_type == 'todo':
        tasks = tasks.filter(completed=False)
    elif filter_type == 'overdue':
        from django.utils import timezone
        tasks = tasks.filter(completed=False, due_date__lt=timezone.now().date())
    
    if priority:
        tasks = tasks.filter(priority=int(priority))
    
    # Création
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        priority = request.POST.get('priority', 3)
        due_date = request.POST.get('due_date') or None
        
        if title:
            Task.objects.create(title=title, priority=priority, due_date=due_date)
            messages.success(request, f"Tâche '{title}' ajoutée !")
        else:
            messages.error(request, "Le titre est obligatoire")
        return redirect('index')
    
    context = {
        'tasks': tasks,
        'filter': filter_type,
        'priorities': Task.PRIORITY_CHOICES,
        'stats': {
            'total': Task.objects.count(),
            'completed': Task.objects.filter(completed=True).count(),
            'pending': Task.objects.filter(completed=False).count(),
        }
    }
    return render(request, 'todo/index.html', context)

def toggle_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = not task.completed
    task.save()
    status = "terminée" if task.completed else "réouverte"
    messages.info(request, f"Tâche {status}")
    return redirect('index')

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    messages.success(request, "Tâche supprimée")
    return redirect('index')
