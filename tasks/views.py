from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # formulario de registro y formulario autentificacion
from django.contrib.auth.models import User # Importamos el modelo de usuario
from django.contrib.auth import login, logout, authenticate  
from django.db import IntegrityError
from .forms import TaskForm # Importamos el formulario de tareas
from .models import Task 
from django.utils import timezone # Importamos el módulo timezone para trabajar con fechas y horas
from django.contrib.auth.decorators import login_required # Importamos el decorador login_required para proteger las rutas

# Vista para la página de inicio
def home(request):
    return render(request, 'home.html')

# Vista para el inicio de la página de tareas
@login_required
def home_task(request):
    return render(request, 'home_task.html')

# Vista para la página de registro
def signup(request):
    if request.method == 'GET': # si la peticion es GET se muestra el formulario
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else: # si la peticion es POST se procesa el formulario
        if request.POST['password1'] == request.POST['password2']: # si las contraseñas son iguales
            try:
                # Registrar usuario
                user = User.objects.create_user( 
                    username=request.POST['username'], 
                    password=request.POST['password1']
                )
                user.save()
                login(request, user) 
                return redirect('home_task') # redirigir a la página de inicio del usuario autenticado
            except IntegrityError: 
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        # si las contraseñas no son iguales
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })

# Vista para la página de tareas pendientes
@login_required
def tasks(request):                           
    task = Task.objects.filter(user=request.user, datecomplete__isnull=True) # Se muestran las tareas pendientes del usuario autenticado
    return render(request, 'tasks.html', {
        'tasks': task,
        'title': 'Tareas Pendientes'
    })

# Vista para la página de tareas completadas
@login_required
def tasks_completed(request):                           
    task = Task.objects.filter(user=request.user, datecomplete__isnull=False).order_by('-datecomplete') # Se muestran las tareas completadas del usuario autenticado 
    return render(request, 'tasks.html', {
        'tasks': task,
        'title': 'Tareas Completadas'
    })

# Vista para la página de creacion de tareas
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            # Guardar tarea
            form = TaskForm(request.POST) # Se crea un formulario con los datos enviados
            new_task = form.save(commit=False) # Se guarda el formulario sin guardar en la base de datos
            new_task.user = request.user # Se asigna la tarea al usuario autenticado
            new_task.save() # Se guarda la tarea
            return redirect('tasks') # Se redirige a la página de tareas pendientes
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor ingrese datos validos'
            })

# Vista para la página de detalles - Actualizar tareas y Obtener tareas
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user) # Se obtiene la tarea del usuario autenticado
        form = TaskForm(instance=task) # Se crea un formulario con los datos de la tarea
        return render(request, 'task_detail.html', {
            'task': task, 
            'form': form
        })
    else:
        # Actualizar tarea
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user) # Obtenemos la tarea del usuario autenticado
            form = TaskForm(request.POST, instance=task) # Se crea un formulario con los datos enviados
            form.save() # Se actualiza la tarea
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error al actualizar la tarea'
            })

# Vista para la página de detalles - Completar tareas
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user) # Obtenemos la tarea del usuario autenticado
    if request.method == 'POST':
        task.datecomplete = timezone.now() # Se marca la tarea como completada
        task.save() # Se guarda la tarea
        return redirect('tasks')

# Vista para la página de detalles - Eliminar tareas
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user) # Obtenemos la tarea del usuario autenticado
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')  

# Vista para cerrar sesión
@login_required
def signout(request):
    logout(request)
    return redirect('home')

# Vista para la página de inicio de sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # Autenticar usuario
        user = authenticate( # Si el usuario es valido
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None: # si el usuario no es valido o no existe
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o la contraseña son incorrectos'
            })
        else: # si el usuario existe
            login(request, user) # Guardar sesion del usuario autenticado
            return redirect('home_task') 

# vista para eliminar usuario 
@login_required
def delete_user(request):
    user = request.user  # Obtenemos el usuario autenticado
    if request.method == 'POST':
        user.delete()  # Eliminamos el usuario
        logout(request)  # Cerramos la sesión después de eliminar
        return redirect('home')  # Redirigimos a la página principal
    return render(request, 'delete_user.html')  # Confirmación antes de eliminar
