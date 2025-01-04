# Creamos el formulario en base al modelo Task

from django import forms # Importamos el módulo forms para crear el formulario de tareas
from .models import Task # Importamos el modelo 

# Creamos el formulario
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important'] # Definimos los campos que se mostraran en el formulario
        widgets = {
            # Definimos los atributos de los campos del formulario con clases de Bootstrap 
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la tarea'}), 
            'description': forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'Descripción de la tarea', 'rows': 6}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }