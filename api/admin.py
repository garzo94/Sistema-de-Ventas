from django.contrib import admin

# Register your models here.
from .models import Cliente, Producto, Venta, VentaDetalle
# Register your models here.


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo_electronico', 'direccion', 'fecha_registro')

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio' )


class VentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_venta', 'precio_total' )

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Venta, VentaAdmin)