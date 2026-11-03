"""Funciones auxiliares de reciclaje (las usan las vistas de reciclaje y de reportes)."""
from django.db.models import Q


def activos_o_actual(modelo, actual_pk=None):
    """Elementos activos y, al editar, también el que ya estaba elegido
    (aunque después se haya desactivado). Reportes también lo usa."""
    return modelo.objects.filter(Q(activo=True) | Q(pk=actual_pk))
