from django.urls import path
from .views import (
    MercaderiaRetiradaListView,
    MercaderiaRetiradaCreateView,
    MercaderiaRetiradaDetailView,
)

app_name = 'mercaderia_retirada'

urlpatterns = [
    path('', MercaderiaRetiradaListView.as_view(), name='lista'),
    path('crear/', MercaderiaRetiradaCreateView.as_view(), name='crear'),
    path('<int:pk>/', MercaderiaRetiradaDetailView.as_view(), name='detalle'),
]
