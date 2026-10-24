from django.contrib import admin

from .models import Reporte, SeguimientoReporte


class SeguimientoInline(admin.TabularInline):
    model = SeguimientoReporte
    extra = 0
    readonly_fields = ('fecha',)


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'estado', 'perfil', 'punto', 'fecha_creacion')
    list_filter = ('tipo', 'estado')
    search_fields = ('titulo', 'descripcion', 'perfil__usuario__username')
    readonly_fields = ('fecha_creacion',)
    list_select_related = ('perfil__usuario', 'punto')
    inlines = [SeguimientoInline]


@admin.register(SeguimientoReporte)
class SeguimientoReporteAdmin(admin.ModelAdmin):
    list_display = ('reporte', 'autor', 'resumen', 'fecha')
    readonly_fields = ('fecha',)
    list_select_related = ('reporte', 'autor__usuario')
