from django.db import models
from django.utils import timezone

# 03/12/2023 - Geoffroy
# TP2 V1 - Modèle Task amélioré
# Ajout de priorité et de dates pour un vrai gestionnaire de tâches.

class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, '🔴 Urgent'),
        (2, '🟠 Important'),
        (3, '🟡 Normal'),
        (4, '🟢 Faible'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True, verbose_name="Échéance")
    
    class Meta:
        ordering = ['completed', 'priority', 'due_date']
    
    def __str__(self):
        status = "✅" if self.completed else "⬜"
        return f"{status} {self.title}"
    
    @property
    def is_overdue(self):
        if self.due_date and not self.completed:
            return self.due_date < timezone.now().date()
        return False
    
    @property
    def priority_label(self):
        return dict(self.PRIORITY_CHOICES).get(self.priority, "Normal")
