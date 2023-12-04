from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# 04/12/2023 - Geoffroy
# TP2 V2 - Modèle avancé avec sous-tâches et tags

class Tag(models.Model):
    """Tags pour catégoriser les tâches."""
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#3498db")  # Hex color
    
    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, '🔴 Critique'),
        (2, '🟠 Haute'),
        (3, '🟡 Moyenne'),
        (4, '🟢 Basse'),
    ]
    
    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Pour les sous-tâches
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subtasks')
    
    class Meta:
        ordering = ['status', 'priority', 'due_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        if self.due_date and self.status not in ['done', 'cancelled']:
            return self.due_date < timezone.now().date()
        return False
    
    @property
    def completion_percentage(self):
        """Pourcentage de sous-tâches terminées."""
        subtasks = self.subtasks.all()
        if not subtasks:
            return 100 if self.status == 'done' else 0
        done = subtasks.filter(status='done').count()
        return int((done / subtasks.count()) * 100)
    
    def complete(self):
        self.status = 'done'
        self.completed_at = timezone.now()
        self.save()
    
    def reopen(self):
        self.status = 'todo'
        self.completed_at = None
        self.save()
