from django.contrib import admin
from .models import MercaderiaRetirada


@admin.register(MercaderiaRetirada)
class MercaderiaRetiradaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'producto',
        'cantidad',
        'motivo',
        'fecha_retiro',
    )
    search_fields = ('producto__nombre', 'observaciones')
    list_filter = ('motivo', 'fecha_retiro')
    ordering = ('-fecha_retiro',)
