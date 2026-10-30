from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'marca',
        'categoria',
        'precio_compra',
        'precio_venta',
    )
    search_fields = ('nombre', 'marca', 'categoria')
    list_filter = ('categoria',)
    ordering = ('nombre',)
