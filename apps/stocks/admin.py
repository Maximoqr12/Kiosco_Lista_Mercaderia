from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'producto',
        'cantidad',
        'stock_minimo',
        'fecha_actualizacion',
    )
    search_fields = ('producto__nombre',)
    list_filter = ('fecha_actualizacion',)
    ordering = ('producto__nombre',)
