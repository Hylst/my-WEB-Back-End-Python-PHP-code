from django.shortcuts import render, redirect
from .models import Task

# 03/12/2023 - Geoffroy
# Vues pour la To-Do.
# Liste, Ajout, Toggle (fait/pas fait), Suppression.
# C'est le CRUD de base du développeur web. Le "katas" quotidien.

def index(request):
    tasks = Task.objects.all().order_by('-created_at')
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('index')
    return render(request, 'todo/index.html', {'tasks': tasks})

def toggle_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect('index')
