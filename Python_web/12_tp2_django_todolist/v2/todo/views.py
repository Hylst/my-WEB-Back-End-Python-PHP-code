from django.shortcuts import render, redirect
from .models import Task

# 04/12/2023 - Geoffroy
# V2 : On filtre et on trie.
# J'ai ajouté des filtres pour afficher "Tout", "A faire", "Terminé".
# C'est un peu plus UX friendly. On se sent moins submergé par la liste .

def index(request):
    filter_type = request.GET.get('filter', 'all')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        date_str = request.POST.get('due_date')
        if title:
            # On gère le cas où la date est vide
            due_date = date_str if date_str else None
            Task.objects.create(title=title, due_date=due_date)
        return redirect('index')

    if filter_type == 'completed':
        tasks = Task.objects.filter(completed=True).order_by('-created_at')
    elif filter_type == 'todo':
        tasks = Task.objects.filter(completed=False).order_by('due_date')
    else:
        tasks = Task.objects.all().order_by('completed', 'due_date') # Non terminées en premier

    return render(request, 'todo/index.html', {'tasks': tasks, 'filter': filter_type})

def toggle_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect('index')
