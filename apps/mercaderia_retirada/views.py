
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
)

from apps.permisos import (
    AdultoResponsableMixin,
    UsuarioAutenticadoMixin,
)
from apps.stocks.models import Stock, MovimientoMercaderia

from .models import MercaderiaRetirada


class MercaderiaRetiradaListView(
    UsuarioAutenticadoMixin,
    ListView,
):
    model = MercaderiaRetirada
    template_name = (
        'mercaderia_retirada/mercaderia_retirada_list.html'
    )
    context_object_name = 'retiros'
    ordering = ['-fecha_retiro']


class MercaderiaRetiradaCreateView(
    AdultoResponsableMixin,
    CreateView,
):
    model = MercaderiaRetirada
    fields = [
        'producto',
        'cantidad',
        'motivo',
        'observaciones',
    ]
    template_name = (
        'mercaderia_retirada/mercaderia_retirada_create.html'
    )
    success_url = reverse_lazy('mercaderia_retirada:lista')

    @transaction.atomic
    def form_valid(self, form):
        producto = form.cleaned_data['producto']
        cantidad = form.cleaned_data['cantidad']
        motivo = form.cleaned_data['motivo']

        if cantidad <= 0:
            form.add_error(
                'cantidad',
                'La cantidad debe ser mayor a cero.'
            )
            return self.form_invalid(form)

        try:
            stock = Stock.objects.select_for_update().get(
                producto=producto
            )
        except Stock.DoesNotExist:
            form.add_error(
                'producto',
                'Este producto todavía no tiene un registro de stock.'
            )
            return self.form_invalid(form)

        if cantidad > stock.cantidad:
            form.add_error(
                'cantidad',
                'No hay suficientes unidades disponibles.'
            )
            return self.form_invalid(form)

        # Descontar las unidades del inventario.
        stock.cantidad -= cantidad
        stock.save()

        # Guardar el retiro.
        response = super().form_valid(form)

        # Diferenciar un descarte por defecto o daño
        # de un retiro por otro motivo.
        tipo_movimiento = (
            'descarte'
            if motivo in ('defectuoso', 'danado')
            else 'retiro'
        )

        detalle_motivo = dict(
            MercaderiaRetirada.MOTIVOS
        ).get(motivo, motivo)

        observaciones = (
            f"Motivo: {detalle_motivo}. "
            f"{form.cleaned_data['observaciones']}"
        ).strip()

        # Registrar el movimiento en el historial.
        MovimientoMercaderia.objects.create(
            producto=producto,
            tipo=tipo_movimiento,
            cantidad=cantidad,
            observaciones=observaciones,
        )

        return response


class MercaderiaRetiradaDetailView(
    UsuarioAutenticadoMixin,
    DetailView,
):
    model = MercaderiaRetirada
    template_name = (
        'mercaderia_retirada/mercaderia_retirada_detail.html'
    )
    context_object_name = 'retiro'
