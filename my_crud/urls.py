from django.urls import path
from .views import UsuarioVista, UsuarioPdfVista

urlpatterns = [
    path('usuarios/', UsuarioVista.as_view(), name='usuario-list'),
    path('usuarios/pdf/', UsuarioPdfVista.as_view(), name='usuario-pdf'),
]
