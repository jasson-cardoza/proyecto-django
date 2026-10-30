from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    # Sesión
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Perfil (la cuenta)
    path('registro/', views.PerfilCreateView.as_view(), name='perfil_registro'),
    path('perfiles/', views.PerfilListView.as_view(), name='perfil_list'),
    path('perfil/', views.PerfilDetailView.as_view(), name='perfil_mio'),
    path('perfiles/<int:pk>/', views.PerfilDetailView.as_view(), name='perfil_detail'),
    path('perfiles/<int:pk>/editar/', views.PerfilUpdateView.as_view(), name='perfil_update'),
    path('perfiles/<int:pk>/eliminar/', views.PerfilDeleteView.as_view(), name='perfil_delete'),

    # Direcciones
    path('direcciones/', views.DireccionListView.as_view(), name='direccion_list'),
    path('direcciones/nueva/', views.DireccionCreateView.as_view(), name='direccion_create'),
    path('direcciones/<int:pk>/', views.DireccionDetailView.as_view(), name='direccion_detail'),
    path('direcciones/<int:pk>/editar/', views.DireccionUpdateView.as_view(), name='direccion_update'),
    path('direcciones/<int:pk>/eliminar/', views.DireccionDeleteView.as_view(), name='direccion_delete'),
]
