from django.contrib import admin

from .models import Material, PuntoReciclaje, RegistroReciclaje


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'puntos_por_kg', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'descripcion')


@admin.register(PuntoReciclaje)
class PuntoReciclajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'municipio', 'activo')
    list_filter = ('departamento', 'activo')
    search_fields = ('nombre', 'municipio', 'direccion')
    filter_horizontal = ('materiales_aceptados',)


@admin.register(RegistroReciclaje)
class RegistroReciclajeAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'material', 'punto', 'cantidad_kg',
                    'puntos_ganados', 'fecha')
    list_filter = ('material', 'punto')
    search_fields = ('perfil__usuario__username',)
    readonly_fields = ('puntos_ganados', 'fecha')
    list_select_related = ('perfil__usuario', 'material', 'punto')
