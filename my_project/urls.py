"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), # url de la página de inicio
    path('home_task/', views.home_task, name='home_task'), # url de la página de inicio del usuario autentificado
    path('signup/', views.signup, name='signup'), # url de la página de registro
    path('tasks/', views.tasks, name='tasks'), # url de la página para mostrar tareas pendientes
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'), # url de la página para mostrar tareas completadas
    path('tasks/create/', views.create_task, name='create_task'), # url para crear tareas 
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'), # url para obtener una tarea y actualizar una tarea
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'), # url para marcar una tarea como completada
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'), # url para eliminar una tarea
    path('logout/', views.signout, name='logout'), # url para cerrar sesión
    path('signin/', views.signin, name='signin'), # url para iniciar sesión
    path('delete_user/', views.delete_user, name='delete_user'),  # URL para eliminar usuario
]
