from django.urls import path
from .views import UsuarioList, UsuarioDetail, TareaList, TareaDetail

urlpatterns = [
    path('usuarios/', UsuarioList.as_view()),
    path('usuarios/<str:email>/', UsuarioDetail.as_view()),
    path('tareas/', TareaList.as_view()),
    path('tareas/<str:nombre>/', TareaDetail.as_view()),
]
