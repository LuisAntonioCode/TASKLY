from django.db import models
from django.contrib.auth.models import User # Importamos el modelo de usuario

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100) # Titulo de la tarea
    description = models.TextField(blank=True) # Descripcion de la tarea
    created = models.DateTimeField(auto_now_add=True) # Fecha de creacion de la tarea
    datecomplete = models.DateTimeField(null=True, blank=True) # Fecha de la tarea completa
    important = models.BooleanField(default=False) # Si la tarea es importante o no
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Usuario que crea la tarea

    def __str__(self):
        return self.title + ' - Creada por ' + self.user.username