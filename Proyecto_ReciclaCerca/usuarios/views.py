"""Vistas de usuarios: CRUD de Perfil (la cuenta) y de Direccion.

Rutas a las que estas vistas redirigen (deben existir):
  usuarios:perfil_detail, usuarios:perfil_list, usuarios:direccion_list
  e inicio:inicio.

QUIÉN PUEDE QUÉ
  - Registro (PerfilCreateView): cualquiera. Crea User + Perfil e inicia sesión.
  - PerfilListView: solo staff.
  - Perfil y Direccion (ver / editar / eliminar): su dueño o staff; si no, 404.
    Eliminar un Perfil borra la cuenta completa (User y, en cascada, todo lo suyo).
  - El único rol con privilegios extra es is_staff.
"""
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import PerfilForm, RegistroForm
from .models import Direccion, Perfil


# ---------------------------------------------------------------------------
# Piezas compartidas (reciclaje y reportes también las importan)
# ---------------------------------------------------------------------------

class SoloStaffMixin(UserPassesTestMixin):
    """Solo is_staff. Sin sesión redirige al login; con sesión da 403."""

    def test_func(self):
        return self.request.user.is_staff


class SoloMisDatosMixin(LoginRequiredMixin):
    """Staff ve todo; el resto solo lo suyo.

    Cada vista indica `model`, `campo_dueno` (la ruta hasta el User dueño,
    p. ej. 'perfil__usuario') y, si quiere, `select_related`.
    """

    campo_dueno = 'perfil__usuario'
    select_related = ()

    def get_queryset(self):
        qs = self.model.objects.select_related(*self.select_related)
        if not self.request.user.is_staff:
            qs = qs.filter(**{self.campo_dueno: self.request.user})
        return qs


class PerfilRequeridoMixin(LoginRequiredMixin):
    """Exige sesión y una cuenta con Perfil (queda en self.perfil).

    Casi todas las tablas apuntan a Perfil, así que una cuenta sin él
    (p. ej. un superusuario creado por consola) no puede registrar datos.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                self.perfil = request.user.perfil
            except Perfil.DoesNotExist:
                raise PermissionDenied('Tu cuenta no tiene un perfil asociado.') from None
        return super().dispatch(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# Perfil
# ---------------------------------------------------------------------------

class PerfilAccesoMixin(SoloMisDatosMixin):
    model = Perfil
    campo_dueno = 'usuario'
    select_related = ('usuario',)

    def get_object(self, queryset=None):
        if self.pk_url_kwarg not in self.kwargs:  # ruta sin pk = "mi perfil"
            try:
                return self.request.user.perfil
            except Perfil.DoesNotExist:
                raise PermissionDenied('Tu cuenta no tiene un perfil asociado.') from None
        return super().get_object(queryset)


class PerfilListView(SoloStaffMixin, ListView):
    queryset = Perfil.objects.select_related('usuario')
    ordering = ('usuario__username',)
    paginate_by = 20
    template_name = 'usuarios/perfil_list.html'
    context_object_name = 'perfiles'


class PerfilDetailView(PerfilAccesoMixin, DetailView):
    template_name = 'usuarios/perfil_detail.html'
    context_object_name = 'perfil'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['direcciones'] = self.object.direcciones.order_by(
            '-es_principal', 'departamento', 'municipio'
        )
        return contexto


class PerfilCreateView(CreateView):
    """Registro de una cuenta nueva. Abierto al público."""

    form_class = RegistroForm
    template_name = 'usuarios/perfil_registro.html'

    def form_valid(self, form):
        usuario = form.save()
        login(self.request, usuario)
        messages.success(self.request, '¡Tu cuenta fue creada con éxito!')
        return HttpResponseRedirect(
            reverse('usuarios:perfil_detail', kwargs={'pk': form.perfil.pk})
        )


class PerfilUpdateView(PerfilAccesoMixin, SuccessMessageMixin, UpdateView):
    form_class = PerfilForm
    template_name = 'usuarios/perfil_form.html'
    context_object_name = 'perfil'
    success_message = 'Perfil actualizado correctamente.'

    def get_success_url(self):
        return reverse('usuarios:perfil_detail', kwargs={'pk': self.object.pk})


class PerfilDeleteView(PerfilAccesoMixin, DeleteView):
    template_name = 'usuarios/perfil_confirm_delete.html'
    context_object_name = 'perfil'

    def form_valid(self, form):
        # Se borra el User (no solo el Perfil) para no dejar una cuenta que
        # inicia sesión pero no tiene perfil. El Perfil cae en cascada.
        usuario = self.object.usuario
        es_propia = usuario.pk == self.request.user.pk
        usuario.delete()
        if es_propia:
            logout(self.request)
        messages.success(self.request, 'La cuenta fue eliminada.')
        return HttpResponseRedirect(
            reverse('inicio:inicio' if es_propia else 'usuarios:perfil_list')
        )


# ---------------------------------------------------------------------------
# Direccion
# ---------------------------------------------------------------------------

class DireccionAccesoMixin(SoloMisDatosMixin):
    model = Direccion
    select_related = ('perfil__usuario',)


class DireccionFormMixin(SuccessMessageMixin):
    """Alta y edición comparten campos y destino. Un perfil solo puede tener
    una dirección principal: la última que se guarde."""

    fields = ['departamento', 'municipio', 'detalle', 'es_principal']
    template_name = 'usuarios/direccion_form.html'
    success_url = reverse_lazy('usuarios:direccion_list')

    def form_valid(self, form):
        with transaction.atomic():
            respuesta = super().form_valid(form)
            if self.object.es_principal:
                Direccion.objects.filter(perfil=self.object.perfil).exclude(
                    pk=self.object.pk
                ).update(es_principal=False)
        return respuesta


class DireccionListView(DireccionAccesoMixin, ListView):
    paginate_by = 20
    template_name = 'usuarios/direccion_list.html'
    context_object_name = 'direcciones'

    def get_queryset(self):
        return super().get_queryset().order_by(
            'perfil__usuario__username', '-es_principal', 'departamento', 'municipio'
        )


class DireccionDetailView(DireccionAccesoMixin, DetailView):
    template_name = 'usuarios/direccion_detail.html'
    context_object_name = 'direccion'


class DireccionCreateView(PerfilRequeridoMixin, DireccionFormMixin, CreateView):
    model = Direccion
    success_message = 'Dirección agregada.'

    def form_valid(self, form):
        form.instance.perfil = self.perfil
        return super().form_valid(form)


class DireccionUpdateView(DireccionAccesoMixin, DireccionFormMixin, UpdateView):
    context_object_name = 'direccion'
    success_message = 'Dirección actualizada.'


class DireccionDeleteView(DireccionAccesoMixin, SuccessMessageMixin, DeleteView):
    template_name = 'usuarios/direccion_confirm_delete.html'
    context_object_name = 'direccion'
    success_url = reverse_lazy('usuarios:direccion_list')
    success_message = 'Dirección eliminada.'
