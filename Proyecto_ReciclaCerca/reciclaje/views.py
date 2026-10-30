"""Vistas de reciclaje: CRUD de Material, PuntoReciclaje y RegistroReciclaje.

Rutas a las que estas vistas redirigen (deben existir):
  reciclaje:material_list, reciclaje:punto_list, reciclaje:registro_list.

QUIÉN PUEDE QUÉ
  - Material y PuntoReciclaje: ver es público (quien no es staff solo ve los
    activos); crear, editar y eliminar: solo staff.
  - RegistroReciclaje: exige sesión. Cada usuario gestiona solo los suyos;
    staff ve todos. Al crear, el perfil es el del usuario con sesión.
  - Un Material o Punto con registros no se puede eliminar (PROTECT): se avisa
    y se sugiere desactivarlo con el campo 'activo'.

PUNTOS
  El modelo suma puntos solo al CREAR un registro, así que al editar o
  eliminar uno se ajustan aquí los del perfil. Lo ideal sería moverlo al modelo.
"""
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import ProtectedError, Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from usuarios.views import PerfilRequeridoMixin, SoloMisDatosMixin, SoloStaffMixin

from .models import Material, PuntoReciclaje, RegistroReciclaje


# ---------------------------------------------------------------------------
# Piezas compartidas
# ---------------------------------------------------------------------------

def activos_o_actual(modelo, actual_pk=None):
    """Elementos activos y, al editar, también el que ya estaba elegido
    (aunque después se haya desactivado). Reportes también lo usa."""
    return modelo.objects.filter(Q(activo=True) | Q(pk=actual_pk))


class CatalogoPublicoMixin:
    """Lectura abierta; quien no es staff solo ve los elementos activos."""

    def get_queryset(self):
        qs = super().get_queryset()
        return qs if self.request.user.is_staff else qs.filter(activo=True)


class EliminacionProtegidaMixin:
    """Evita el error 500 al borrar algo referenciado por registros (PROTECT)."""

    mensaje_protegido = 'No se puede eliminar porque tiene registros asociados.'

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, self.mensaje_protegido)
            return HttpResponseRedirect(self.get_success_url())


class CatalogoFormMixin(SoloStaffMixin, SuccessMessageMixin):
    """Alta y edición de un elemento del catálogo (solo staff)."""


# ---------------------------------------------------------------------------
# Material
# ---------------------------------------------------------------------------

class MaterialListView(CatalogoPublicoMixin, ListView):
    model = Material
    ordering = ('categoria', 'nombre')
    paginate_by = 20
    template_name = 'reciclaje/material_list.html'
    context_object_name = 'materiales'


class MaterialDetailView(CatalogoPublicoMixin, DetailView):
    model = Material
    template_name = 'reciclaje/material_detail.html'
    context_object_name = 'material'


class MaterialFormMixin(CatalogoFormMixin):
    model = Material
    fields = ['nombre', 'categoria', 'descripcion', 'puntos_por_kg', 'activo']
    template_name = 'reciclaje/material_form.html'
    context_object_name = 'material'
    success_url = reverse_lazy('reciclaje:material_list')


class MaterialCreateView(MaterialFormMixin, CreateView):
    success_message = 'Material «%(nombre)s» registrado.'


class MaterialUpdateView(MaterialFormMixin, UpdateView):
    success_message = 'Material «%(nombre)s» actualizado.'


class MaterialDeleteView(SoloStaffMixin, EliminacionProtegidaMixin,
                         SuccessMessageMixin, DeleteView):
    model = Material
    template_name = 'reciclaje/material_confirm_delete.html'
    context_object_name = 'material'
    success_url = reverse_lazy('reciclaje:material_list')
    success_message = 'Material eliminado.'
    mensaje_protegido = (
        'No se puede eliminar el material porque ya tiene registros de '
        'reciclaje. Edítalo y desmarca "activo" para dejar de usarlo.'
    )


# ---------------------------------------------------------------------------
# PuntoReciclaje
# ---------------------------------------------------------------------------

class PuntoListView(CatalogoPublicoMixin, ListView):
    queryset = PuntoReciclaje.objects.prefetch_related('materiales_aceptados')
    ordering = ('departamento', 'municipio', 'nombre')
    paginate_by = 20
    template_name = 'reciclaje/punto_list.html'
    context_object_name = 'puntos'


class PuntoDetailView(CatalogoPublicoMixin, DetailView):
    queryset = PuntoReciclaje.objects.prefetch_related('materiales_aceptados')
    template_name = 'reciclaje/punto_detail.html'
    context_object_name = 'punto'


class PuntoFormMixin(CatalogoFormMixin):
    model = PuntoReciclaje
    fields = [
        'nombre', 'departamento', 'municipio', 'direccion', 'telefono',
        'horario', 'materiales_aceptados', 'activo',
    ]
    template_name = 'reciclaje/punto_form.html'
    context_object_name = 'punto'
    success_url = reverse_lazy('reciclaje:punto_list')


class PuntoCreateView(PuntoFormMixin, CreateView):
    success_message = 'Punto «%(nombre)s» registrado.'


class PuntoUpdateView(PuntoFormMixin, UpdateView):
    success_message = 'Punto «%(nombre)s» actualizado.'


class PuntoDeleteView(SoloStaffMixin, EliminacionProtegidaMixin,
                      SuccessMessageMixin, DeleteView):
    model = PuntoReciclaje
    template_name = 'reciclaje/punto_confirm_delete.html'
    context_object_name = 'punto'
    success_url = reverse_lazy('reciclaje:punto_list')
    success_message = 'Punto eliminado.'
    mensaje_protegido = (
        'No se puede eliminar el punto porque ya tiene registros de '
        'reciclaje. Edítalo y desmarca "activo" para dejar de usarlo.'
    )


# ---------------------------------------------------------------------------
# RegistroReciclaje
# ---------------------------------------------------------------------------

class RegistroAccesoMixin(SoloMisDatosMixin):
    model = RegistroReciclaje
    select_related = ('perfil__usuario', 'punto', 'material')


class RegistroFormMixin(SuccessMessageMixin):
    """Formulario: punto, material y cantidad (el perfil lo pone la vista).
    Las reglas (cantidad > 0, el punto acepta el material) las valida el modelo."""

    model = RegistroReciclaje
    fields = ['punto', 'material', 'cantidad_kg']
    template_name = 'reciclaje/registro_form.html'
    context_object_name = 'registro'
    success_url = reverse_lazy('reciclaje:registro_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        actual = self.object  # None al crear
        form.fields['punto'].queryset = activos_o_actual(
            PuntoReciclaje, actual and actual.punto_id).order_by('nombre')
        form.fields['material'].queryset = activos_o_actual(
            Material, actual and actual.material_id).order_by('nombre')
        return form


class RegistroListView(RegistroAccesoMixin, ListView):
    paginate_by = 20
    template_name = 'reciclaje/registro_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        return super().get_queryset().order_by('-fecha')


class RegistroDetailView(RegistroAccesoMixin, DetailView):
    template_name = 'reciclaje/registro_detail.html'
    context_object_name = 'registro'


class RegistroCreateView(PerfilRequeridoMixin, RegistroFormMixin, CreateView):
    def form_valid(self, form):
        form.instance.perfil = self.perfil
        return super().form_valid(form)  # el modelo calcula y suma los puntos

    def get_success_message(self, cleaned_data):
        return f'¡Registro guardado! Ganaste {self.object.puntos_ganados} puntos.'


class RegistroUpdateView(RegistroAccesoMixin, RegistroFormMixin, UpdateView):
    success_message = 'Registro actualizado.'

    def form_valid(self, form):
        registro = form.instance
        cambios = set(form.changed_data)

        # El modelo solo comprueba que el punto acepte el material al crear.
        if {'punto', 'material'} & cambios and not registro.punto.acepta_material(registro.material):
            form.add_error('material', (
                f"El punto '{registro.punto.nombre}' no acepta {registro.material.nombre}."
            ))
            return self.form_invalid(form)

        with transaction.atomic():
            # Si cambió cantidad o material se recalculan los puntos del
            # registro y se corrige la diferencia en el perfil. Si no, se
            # dejan como estaban (no se re-valora con una tarifa más nueva).
            if {'material', 'cantidad_kg'} & cambios:
                nuevos = registro.calcular_puntos()
                perfil = registro.perfil
                perfil.puntos = max(0, perfil.puntos + nuevos - registro.puntos_ganados)
                perfil.save(update_fields=['puntos'])
                registro.puntos_ganados = nuevos
            return super().form_valid(form)


class RegistroDeleteView(RegistroAccesoMixin, SuccessMessageMixin, DeleteView):
    template_name = 'reciclaje/registro_confirm_delete.html'
    context_object_name = 'registro'
    success_url = reverse_lazy('reciclaje:registro_list')
    success_message = 'Registro eliminado y sus puntos descontados.'

    def form_valid(self, form):
        # Se descuentan del perfil los puntos que este registro le había dado.
        with transaction.atomic():
            perfil = self.object.perfil
            perfil.puntos = max(0, perfil.puntos - self.object.puntos_ganados)
            perfil.save(update_fields=['puntos'])
            return super().form_valid(form)
