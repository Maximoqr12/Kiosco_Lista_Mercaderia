
from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('', views.StockListView.as_view(), name='lista'),

    path(
        'crear/',
        views.StockCreateView.as_view(),
        name='crear'
    ),

    path(
        'movimientos/crear/',
        views.MovimientoCreateView.as_view(),
        name='movimiento_crear'
    ),

    path('<int:pk>/', views.StockDetailView.as_view(), name='detalle'),

    path(
        '<int:pk>/editar/',
        views.StockUpdateView.as_view(),
        name='editar'
    ),

    path(
        '<int:pk>/eliminar/',
        views.StockDeleteView.as_view(),
        name='eliminar'
    ),
    path(
        'movimientos/',
        views.MovimientoListView.as_view(),
        name='movimientos'
    ),
]
