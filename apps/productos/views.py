
from django.db.models import Q
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
from .models import Producto


class ProductoListView(UsuarioAutenticadoMixin, ListView):
    model = Producto
    template_name = 'productos/productos_list.html'
    context_object_name = 'productos'
    ordering = ['nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        busqueda = self.request.GET.get('buscar', '').strip()

        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda)
                | Q(marca__icontains=busqueda)
                | Q(categoria__icontains=busqueda)
            )
        estado = self.request.GET.get('estado', '').strip()

        if estado in dict(Producto.ESTADOS):
            queryset = queryset.filter(estado=estado)

        return queryset

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
    
class ProductoCreateView(AdultoResponsableMixin, CreateView):
    model = Producto
    fields = [
        'nombre',
        'marca',
        'categoria',
        'descripcion',
        'precio_compra',
        'precio_venta',
        'estado',
    ]
    template_name = 'productos/productos_create.html'
    success_url = reverse_lazy('productos:lista')


class ProductoDetailView(UsuarioAutenticadoMixin, DetailView):
    model = Producto
    template_name = 'productos/productos_detail.html'
    context_object_name = 'producto'


class ProductoUpdateView(AdultoResponsableMixin, UpdateView):
    model = Producto
    fields = [
        'nombre',
        'marca',
        'categoria',
        'descripcion',
        'precio_compra',
        'precio_venta',
        'estado',
    ]
    template_name = 'productos/productos_update.html'
    success_url = reverse_lazy('productos:lista')


class ProductoDeleteView(AdultoResponsableMixin, DeleteView):
    model = Producto
    template_name = 'productos/productos_delete.html'
    success_url = reverse_lazy('productos:lista')
