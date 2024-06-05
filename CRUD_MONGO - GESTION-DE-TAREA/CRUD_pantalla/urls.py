from django.urls import path
from . import views

urlpatterns = [
    path('Registro/', views.registro_view, name='registro'),
    path('Login/', views.Login_usuario, name='Login'),
    path('logout/', views.logout, name='logout'),
    path('Inicio/', views.Inicio, name='Inicio'),
    path('Agregar_tarea/', views.Agregar_tarea, name='Agregar_tarea'),
    path('Eliminar_tarea/', views.Eliminar_tarea, name='Eliminar_tarea'),
    path('Editar_tarea/', views.Editar_tarea, name='Editar_tarea'),
    path('Guardar_modificacion/', views.Guardar_modificacion, name='Guardar_modificacion'),

]