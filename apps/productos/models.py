from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, blank=True)
    categoria = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio_compra = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    precio_venta = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    ESTADOS = [
    ('disponible', 'Disponible'),
    ('retirado', 'Retirado'),
    ]

    estado = models.CharField(
    max_length=20,
    choices=ESTADOS,
    default='disponible',
    )
    def __str__(self):
        return self.nombre
