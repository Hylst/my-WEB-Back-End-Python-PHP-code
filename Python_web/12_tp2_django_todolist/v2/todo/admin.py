from django.contrib import admin
from .models import Task, Tag

# 04/12/2023 - Geoffroy
# Admin avancé pour le gestionnaire de tâches V2

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'task_count']
    search_fields = ['name']
    
    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = "Nombre de tâches"


class SubtaskInline(admin.TabularInline):
    """Affiche les sous-tâches dans le formulaire de la tâche parente."""
    model = Task
    fk_name = 'parent'
    extra = 1
    fields = ['title', 'status', 'priority', 'due_date']
    verbose_name = "Sous-tâche"
    verbose_name_plural = "Sous-tâches"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'due_date', 'is_overdue', 'completion_percentage', 'created_at']
    list_filter = ['status', 'priority', 'tags', 'due_date']
    search_fields = ['title', 'description']
    list_editable = ['status', 'priority']
    date_hierarchy = 'created_at'
    filter_horizontal = ['tags']
    inlines = [SubtaskInline]
    ordering = ['status', 'priority', '-created_at']
    
    fieldsets = [
        ('Informations', {
            'fields': ['title', 'description']
        }),
        ('État', {
            'fields': ['status', 'priority', 'due_date', 'completed_at']
        }),
        ('Organisation', {
            'fields': ['tags', 'parent'],
            'classes': ['collapse']
        }),
    ]
    
    readonly_fields = ['completed_at']
    
    def is_overdue(self, obj):
        return "⚠️" if obj.is_overdue else "✓"
    is_overdue.short_description = "Retard"
    
    def completion_percentage(self, obj):
        return f"{obj.completion_percentage}%"
    completion_percentage.short_description = "Progression"
