
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from apps.permisos import (
    AdultoResponsableMixin,
    UsuarioAutenticadoMixin,
)

from .models import Stock, MovimientoMercaderia


class StockListView(
    UsuarioAutenticadoMixin,
    ListView,
):
    model = Stock
    template_name = 'stocks/stocks_list.html'
    context_object_name = 'stocks'
    ordering = ['producto__nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuario = self.request.user

        context['es_adulto_responsable'] = (
        usuario.is_superuser
        or usuario.groups.filter(
            name='Adultos responsables'
        ).exists()
    )

        return context


class StockCreateView(
    AdultoResponsableMixin,
    CreateView,
):
    model = Stock
    fields = [
        'producto',
        'cantidad',
        'stock_minimo',
        'fecha_ingreso',
    ]
    template_name = 'stocks/stocks_create.html'
    success_url = reverse_lazy('stocks:lista')

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)

        if self.object.cantidad > 0:
            MovimientoMercaderia.objects.create(
                producto=self.object.producto,
                tipo='ingreso',
                cantidad=self.object.cantidad,
                observaciones='Registro inicial de stock.',
            )

        return response


class StockDetailView(
    UsuarioAutenticadoMixin,
    DetailView,
):
    model = Stock
    template_name = 'stocks/stocks_detail.html'
    context_object_name = 'stock'


class StockUpdateView(
    AdultoResponsableMixin,
    UpdateView,
):
    model = Stock
    fields = [
        'stock_minimo',
        'fecha_ingreso',
    ]
    template_name = 'stocks/stocks_update.html'
    success_url = reverse_lazy('stocks:lista')


class StockDeleteView(
    AdultoResponsableMixin,
    DeleteView,
):
    model = Stock
    template_name = 'stocks/stocks_delete.html'
    success_url = reverse_lazy('stocks:lista')


class MovimientoCreateView(
    AdultoResponsableMixin,
    CreateView,
):
    model = MovimientoMercaderia

    fields = [
        'producto',
        'tipo',
        'cantidad',
        'observaciones',
    ]

    template_name = 'stocks/movimiento_create.html'
    success_url = reverse_lazy('stocks:lista')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Los ingresos y ventas se registran desde aquí.
        # Retiros y descartes se registran en su aplicación.
        form.fields['tipo'].choices = [
            ('ingreso', 'Ingreso'),
            ('venta', 'Venta'),
        ]

        return form

    @transaction.atomic
    def form_valid(self, form):
        producto = form.cleaned_data['producto']
        tipo = form.cleaned_data['tipo']
        cantidad = form.cleaned_data['cantidad']

        if cantidad <= 0:
            form.add_error(
                'cantidad',
                'La cantidad debe ser mayor que cero.'
            )
            return self.form_invalid(form)

        try:
            stock = Stock.objects.select_for_update().get(
                producto=producto
            )

        except Stock.DoesNotExist:
            if tipo == 'venta':
                form.add_error(
                    'producto',
                    'Este producto todavía no tiene stock registrado.'
                )
                return self.form_invalid(form)

            stock = Stock.objects.create(
                producto=producto,
                cantidad=0,
            )

        if tipo == 'ingreso':
            stock.cantidad += cantidad

        elif tipo == 'venta':
            if cantidad > stock.cantidad:
                form.add_error(
                    'cantidad',
                    f'Stock insuficiente. Disponibles: {stock.cantidad}.'
                )
                return self.form_invalid(form)

            stock.cantidad -= cantidad

        stock.save()

        return super().form_valid(form)      
class MovimientoListView(
    AdultoResponsableMixin,
    ListView,
):
    model = MovimientoMercaderia
    template_name = 'stocks/movimientos_list.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha_movimiento']

