"""Formularios de la app usuarios.

Viven aparte de views.py porque una cuenta son dos modelos a la vez (User de
Django y Perfil), y eso no lo resuelve el formulario automático de una vista.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Perfil


class RegistroForm(UserCreationForm):
    """Registro corto: usuario, correo, tipo y contraseña.

    El resto de los datos (nombres, teléfono, fecha de nacimiento) se
    completa después en "Editar perfil" (PerfilForm). Crea el User y su Perfil
    en un solo paso; el Perfil queda en self.perfil. No se usa commit=False
    porque el Perfil necesita el id del User ya guardado.
    """

    email = forms.EmailField(label='Correo electrónico', required=False)
    tipo_usuario = forms.ChoiceField(
        label='Tipo de usuario', choices=Perfil.TIPO_USUARIO, initial='ciudadano'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
        labels = {'username': 'Usuario'}

    field_order = ('username', 'email', 'tipo_usuario', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

    def save(self, commit=True):
        with transaction.atomic():
            usuario = super().save()
            self.perfil = Perfil.objects.create(
                usuario=usuario, tipo_usuario=self.cleaned_data['tipo_usuario']
            )
        return usuario


class PerfilForm(forms.ModelForm):
    """Edición de los datos personales (User) y del Perfil, guardados juntos."""

    first_name = forms.CharField(label='Nombres', max_length=150, required=False)
    last_name = forms.CharField(label='Apellidos', max_length=150, required=False)
    email = forms.EmailField(label='Correo electrónico', required=False)

    class Meta:
        model = Perfil
        fields = ('telefono', 'fecha_nacimiento', 'tipo_usuario')
        labels = {
            'telefono': 'Teléfono',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'tipo_usuario': 'Tipo de usuario',
        }
        # <input type="date"> solo muestra el valor guardado si viene en ISO.
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            for campo in ('first_name', 'last_name', 'email'):
                self.initial[campo] = getattr(self.instance.usuario, campo)

    def save(self, commit=True):
        perfil = super().save(commit=False)
        for campo in ('first_name', 'last_name', 'email'):
            setattr(perfil.usuario, campo, self.cleaned_data[campo])
        if commit:
            with transaction.atomic():
                perfil.usuario.save()
                perfil.save()
        return perfil
