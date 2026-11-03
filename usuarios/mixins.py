"""Mixins de permisos compartidos por las vistas de usuarios, reciclaje y reportes.

  SoloStaffMixin       -> solo is_staff.
  SoloMisDatosMixin    -> staff ve todo; el resto solo lo suyo.
  PerfilRequeridoMixin -> exige sesión y una cuenta con Perfil.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .models import Perfil


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
