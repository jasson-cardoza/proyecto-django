from django.urls import path

from . import views

app_name = 'reciclaje'

urlpatterns = [
    # Materiales
    path('materiales/', views.MaterialListView.as_view(), name='material_list'),
    path('materiales/nuevo/', views.MaterialCreateView.as_view(), name='material_create'),
    path('materiales/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    path('materiales/<int:pk>/editar/', views.MaterialUpdateView.as_view(), name='material_update'),
    path('materiales/<int:pk>/eliminar/', views.MaterialDeleteView.as_view(), name='material_delete'),

    # Puntos de reciclaje
    path('puntos/', views.PuntoListView.as_view(), name='punto_list'),
    path('puntos/nuevo/', views.PuntoCreateView.as_view(), name='punto_create'),
    path('puntos/<int:pk>/', views.PuntoDetailView.as_view(), name='punto_detail'),
    path('puntos/<int:pk>/editar/', views.PuntoUpdateView.as_view(), name='punto_update'),
    path('puntos/<int:pk>/eliminar/', views.PuntoDeleteView.as_view(), name='punto_delete'),

    # Registros de reciclaje
    path('registros/', views.RegistroListView.as_view(), name='registro_list'),
    path('registros/nuevo/', views.RegistroCreateView.as_view(), name='registro_create'),
    path('registros/<int:pk>/', views.RegistroDetailView.as_view(), name='registro_detail'),
    path('registros/<int:pk>/editar/', views.RegistroUpdateView.as_view(), name='registro_update'),
    path('registros/<int:pk>/eliminar/', views.RegistroDeleteView.as_view(), name='registro_delete'),
]
