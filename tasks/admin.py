from django.contrib import admin
from .models import Task # Importamos el modelo 

# clase para una interfaz personalizada para el modelo Task
class TaskAdmin(admin.ModelAdmin): 
    readonly_fields = ('created',) # El campo created se muestra como de solo lectura en la interfaz de administración

# Register your models here.
admin.site.register(Task, TaskAdmin)
