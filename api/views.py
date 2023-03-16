from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializer import *
# Create your views here.
class LoginView(APIView):
    def post(self, request):        
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,"usuario":username})
        else:
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ClientesView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProductoView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class VentaViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    def create(self, request, *args, **kwargs):
        venta_serializer = self.get_serializer(data=request.data)
        venta_serializer.is_valid(raise_exception=True)
        venta = venta_serializer.save()


        venta_detalle_serializer = CrearVentaDetalleSerializer(data=request.data["venta_detalle"], many=True)
        venta_detalle_serializer.is_valid(raise_exception=True)
        venta_detalle_serializer.save(venta=venta)

        headers = self.get_success_headers(venta_serializer.data)
        return Response(venta_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VentaDetalleViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    queryset = VentaDetalle.objects.all()
    serializer_class = VentaDetalleSerializer

class ListVentasDetalle(APIView):
    def get(self, request):
        ventas = Venta.objects.all()
        serializer = VentasYDetalleSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK )

class ListClientesProductos(APIView):

    def get(self, request):
        productos = Producto.objects.all()
        clientes = Cliente.objects.all()
        serializerProductos = ProductoSerializer(productos, many=True)
        serializerClientes = ClienteSerializer(clientes, many=True)
        return Response({"clientes":serializerClientes.data, "productos":serializerProductos.data}, status=status.HTTP_200_OK)
