from django.contrib import admin
from .models import Task

# 03/12/2023 - Geoffroy
# Configuration de l'admin Django pour gérer les tâches facilement

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'completed', 'due_date', 'created_at']
    list_filter = ['completed', 'priority', 'due_date']
    search_fields = ['title', 'description']
    list_editable = ['completed', 'priority']
    date_hierarchy = 'created_at'
    ordering = ['completed', 'priority', 'due_date']
    
    fieldsets = [
        ('Informations', {'fields': ['title', 'description']}),
        ('Statut', {'fields': ['completed', 'priority', 'due_date']}),
    ]
