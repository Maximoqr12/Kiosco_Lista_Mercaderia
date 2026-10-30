from django.db import models


class MercaderiaRetirada(models.Model):

    MOTIVOS = [
        ('defectuoso', 'Defectuoso al recibir'),
        ('danado', 'Producto dañado'),
        ('retirado', 'Retirado'),
        ('otro', 'Otro'),
    ]
    producto = models.ForeignKey(
        'productos.Producto',
        on_delete=models.PROTECT,
        related_name='retiros'
    )
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(
        max_length=20,
        choices=MOTIVOS
    )
    fecha_retiro = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"
