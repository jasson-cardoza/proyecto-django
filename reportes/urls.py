from django.urls import path

from . import views

app_name = 'reportes'

urlpatterns = [
    # Reportes
    path('', views.ReporteListView.as_view(), name='reporte_list'),
    path('nuevo/', views.ReporteCreateView.as_view(), name='reporte_create'),
    path('<int:pk>/', views.ReporteDetailView.as_view(), name='reporte_detail'),
    path('<int:pk>/editar/', views.ReporteUpdateView.as_view(), name='reporte_update'),
    path('<int:pk>/eliminar/', views.ReporteDeleteView.as_view(), name='reporte_delete'),

    # Seguimientos (comentarios de un reporte)
    path('<int:reporte_pk>/seguimientos/', views.SeguimientoListView.as_view(), name='seguimiento_list'),
    path('<int:reporte_pk>/seguimientos/nuevo/', views.SeguimientoCreateView.as_view(), name='seguimiento_create'),
    path('seguimientos/<int:pk>/editar/', views.SeguimientoUpdateView.as_view(), name='seguimiento_update'),
    path('seguimientos/<int:pk>/eliminar/', views.SeguimientoDeleteView.as_view(), name='seguimiento_delete'),
]
