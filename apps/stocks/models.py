
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Stock(models.Model):
    producto = models.OneToOneField(
        'productos.Producto',
        on_delete=models.CASCADE,
        related_name='stock'
    )
    cantidad = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    fecha_ingreso = models.DateField(
        default=timezone.localdate
    )

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"


class MovimientoMercaderia(models.Model):

    TIPOS = [
        ('ingreso', 'Ingreso'),
        ('retiro', 'Retiro'),
        ('venta', 'Venta'),
        ('descarte', 'Descarte'),
    ]

    producto = models.ForeignKey(
        'productos.Producto',
        on_delete=models.PROTECT,
        related_name='movimientos'
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS
    )

    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    fecha_movimiento = models.DateTimeField(
        auto_now_add=True
    )

    observaciones = models.TextField(blank=True)

    def __str__(self):
        return (
            f"{self.get_tipo_display()} - "
            f"{self.producto.nombre} - "
            f"{self.cantidad} unidades"
        )
