from .models import Cliente, Producto, Venta, VentaDetalle
from rest_framework import serializers

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
        read_only_fields = ("fecha_registro",)

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"

class VentaDetalleSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    class Meta:
        model = VentaDetalle
        fields = "__all__"
        read_only_fields = ("venta",)

class CrearVentaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaDetalle
        fields = "__all__"
        read_only_fields = ("venta",)

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = "__all__"
        read_only_fields = ("fecha_venta",)


class VentasYDetalleSerializer(serializers.ModelSerializer):
    venta_detalle = VentaDetalleSerializer(many=True, read_only=True, source='ventadetalle_set')
    cliente =  ClienteSerializer()
    class Meta:
        model = Venta
        fields = "__all__"
        read_only_fields = ("fecha_venta",)
       

