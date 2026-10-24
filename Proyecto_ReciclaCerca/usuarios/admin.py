from django.contrib import admin

from .models import Direccion, Perfil


class DireccionInline(admin.TabularInline):
    model = Direccion
    extra = 0


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_usuario', 'telefono', 'puntos', 'fecha_registro')
    list_filter = ('tipo_usuario',)
    search_fields = ('usuario__username', 'usuario__first_name',
                     'usuario__last_name', 'telefono')
    readonly_fields = ('fecha_registro',)
    list_select_related = ('usuario',)
    inlines = [DireccionInline]


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'departamento', 'municipio', 'es_principal')
    list_filter = ('departamento', 'es_principal')
    search_fields = ('municipio', 'detalle', 'perfil__usuario__username')
    list_select_related = ('perfil__usuario',)
