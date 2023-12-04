from django.db import models
from django.utils import timezone

# 04/12/2023 - Geoffroy
# TP2 - Version 2.
# On ajoute une date d'échéance.
# C'est comme un compte à rebours avant l'explosion. Ça motive.

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def is_overdue(self):
        if self.due_date and not self.completed:
            return self.due_date < timezone.now().date()
        return False

    def __str__(self):
        return f"{self.title} ({'Terminé' if self.completed else 'En cours'})"
