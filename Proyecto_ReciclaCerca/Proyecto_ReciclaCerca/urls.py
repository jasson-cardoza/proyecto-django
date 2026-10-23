"""
URL configuration for Proyecto_ReciclaCerca project.


"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # Cada aplicación define sus propias rutas en su archivo urls.py.
    path('', include('inicio.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('reciclaje/', include('reciclaje.urls')),
    path('reportes/', include('reportes.urls')),
]

