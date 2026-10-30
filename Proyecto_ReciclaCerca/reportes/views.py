"""Vistas de reportes: CRUD de Reporte y de SeguimientoReporte.

Un Reporte es un aviso de un usuario (punto lleno, contenedor dañado, basura
acumulada, sugerencia) y los Seguimientos son los comentarios que se le van
agregando hasta resolverlo.

Rutas a las que estas vistas redirigen (deben existir):
  reportes:reporte_list y reportes:reporte_detail.

QUIÉN PUEDE QUÉ  (todo exige sesión iniciada)
  - Reporte: cada usuario ve, edita y elimina solo los suyos; staff ve todos.
    El estado solo lo cambia staff; al marcarlo 'resuelto' se guarda la fecha
    de resolución y si se reabre se borra.
  - Seguimiento: se ve y se agrega en los reportes a los que se tiene acceso
    (el dueño y staff). Editar o eliminar: solo su autor o staff.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from reciclaje.models import PuntoReciclaje
from reciclaje.views import activos_o_actual
from usuarios.views import PerfilRequeridoMixin, SoloMisDatosMixin

from .models import Reporte, SeguimientoReporte


# ---------------------------------------------------------------------------
# Reporte
# ---------------------------------------------------------------------------

class ReporteAccesoMixin(SoloMisDatosMixin):
    model = Reporte
    select_related = ('perfil__usuario', 'punto')


class ReporteFormMixin(SuccessMessageMixin):
    """Alta y edición: el punto (opcional) se elige entre los activos y, al
    editar, también el que ya tenía el reporte."""

    template_name = 'reportes/reporte_form.html'
    context_object_name = 'reporte'
    success_url = reverse_lazy('reportes:reporte_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        actual = self.object  # None al crear
        form.fields['punto'].queryset = activos_o_actual(
            PuntoReciclaje, actual and actual.punto_id).order_by('nombre')
        return form


class ReporteListView(ReporteAccesoMixin, ListView):
    paginate_by = 20
    template_name = 'reportes/reporte_list.html'
    context_object_name = 'reportes'

    def get_queryset(self):
        return super().get_queryset().order_by('-fecha_creacion')


class ReporteDetailView(ReporteAccesoMixin, DetailView):
    template_name = 'reportes/reporte_detail.html'
    context_object_name = 'reporte'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['seguimientos'] = self.object.seguimientos.select_related(
            'autor__usuario').order_by('fecha')
        return contexto


class ReporteCreateView(PerfilRequeridoMixin, ReporteFormMixin, CreateView):
    model = Reporte
    fields = ['tipo', 'titulo', 'descripcion', 'punto']
    success_message = 'Reporte «%(titulo)s» enviado.'

    def form_valid(self, form):
        form.instance.perfil = self.perfil
        return super().form_valid(form)  # el estado inicial es 'pendiente'


class ReporteUpdateView(ReporteAccesoMixin, ReporteFormMixin, UpdateView):
    fields = ['tipo', 'titulo', 'descripcion', 'punto', 'estado']
    success_message = 'Reporte actualizado.'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_staff:
            # Un campo fuera del formulario se ignora aunque lo manden en el
            # POST: así nadie se marca su propio reporte como resuelto.
            del form.fields['estado']
        return form

    def form_valid(self, form):
        if 'estado' in form.changed_data:
            form.instance.fecha_resolucion = (
                timezone.now() if form.instance.estado == 'resuelto' else None
            )
        return super().form_valid(form)


class ReporteDeleteView(ReporteAccesoMixin, SuccessMessageMixin, DeleteView):
    template_name = 'reportes/reporte_confirm_delete.html'
    context_object_name = 'reporte'
    success_url = reverse_lazy('reportes:reporte_list')
    success_message = 'Reporte eliminado.'


# ---------------------------------------------------------------------------
# SeguimientoReporte
# ---------------------------------------------------------------------------

class ReporteDeLaUrlMixin(LoginRequiredMixin):
    """Carga el reporte de la URL (kwarg reporte_pk) como self.reporte; 404 si
    el usuario no tiene acceso. Tras guardar vuelve al detalle del reporte."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            qs = Reporte.objects.select_related('perfil__usuario')
            if not request.user.is_staff:
                qs = qs.filter(perfil__usuario=request.user)
            self.reporte = get_object_or_404(qs, pk=kwargs['reporte_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['reporte'] = self.reporte
        return contexto

    def get_success_url(self):
        return reverse('reportes:reporte_detail', kwargs={'pk': self.reporte.pk})


class SeguimientoAutorMixin(SoloMisDatosMixin):
    """Editar o eliminar un comentario: su autor o staff."""

    model = SeguimientoReporte
    campo_dueno = 'autor__usuario'
    select_related = ('reporte', 'autor__usuario')
    template_name = 'reportes/seguimiento_form.html'
    context_object_name = 'seguimiento'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['reporte'] = self.object.reporte
        return contexto

    def get_success_url(self):
        return reverse('reportes:reporte_detail', kwargs={'pk': self.object.reporte_id})


class SeguimientoListView(ReporteDeLaUrlMixin, ListView):
    template_name = 'reportes/seguimiento_list.html'
    context_object_name = 'seguimientos'

    def get_queryset(self):
        return self.reporte.seguimientos.select_related(
            'autor__usuario').order_by('fecha')


class SeguimientoCreateView(ReporteDeLaUrlMixin, PerfilRequeridoMixin,
                            SuccessMessageMixin, CreateView):
    model = SeguimientoReporte
    fields = ['comentario']
    template_name = 'reportes/seguimiento_form.html'
    success_message = 'Comentario agregado.'

    def form_valid(self, form):
        form.instance.reporte = self.reporte
        form.instance.autor = self.perfil
        return super().form_valid(form)


class SeguimientoUpdateView(SeguimientoAutorMixin, SuccessMessageMixin, UpdateView):
    fields = ['comentario']
    success_message = 'Comentario actualizado.'


class SeguimientoDeleteView(SeguimientoAutorMixin, SuccessMessageMixin, DeleteView):
    template_name = 'reportes/seguimiento_confirm_delete.html'
    success_message = 'Comentario eliminado.'
