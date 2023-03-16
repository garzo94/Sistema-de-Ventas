
from .views import *
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'clientes', ClientesView)
router.register(r'productos', ProductoView)
router.register(r'venta', VentaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('ventas/', ListVentasDetalle.as_view(), name='login'),
    path('cli/', ListClientesProductos.as_view(), name='clientes-productos'),
]