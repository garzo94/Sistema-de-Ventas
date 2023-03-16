from django.db import models
from django.db.models import Sum
import itertools
import decimal
# Create your models here.

class Cliente(models.Model):
    TIPO_CHOICES = [
        ('A', 'Tipo A'),
        ('B', 'Tipo B'),
        ('C', 'Tipo C'),
    ]
    
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True)
    tipo_cliente = models.CharField(max_length=1, blank=True, choices=TIPO_CHOICES)

    def actualizar_clasificacion(self):
        clientes = Cliente.objects.annotate(total_ventas=models.Sum('venta__precio_total')).order_by('-total_ventas')
        total_ventas = Venta.objects.aggregate(Sum('precio_total'))['precio_total__sum']
        participacion = [round((c.total_ventas/total_ventas)*100,2) if c.total_ventas is not None else 0 for c in clientes ]
        acumulado = list(itertools.accumulate(participacion))
        print(clientes,"clientes!!")
        print(participacion,"particip!!")
        print(acumulado,"acumulado!!")
        updates = []
        for cli, acum in zip(clientes, acumulado):
            if acum < 80:
                cli.tipo_cliente = "A"
            elif acum >= 80 and acum < 95:
                cli.tipo_cliente = "B"
            else:
                cli.tipo_cliente = "C"
            updates.append(cli)

        Cliente.objects.bulk_update(updates, ['tipo_cliente'])

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_venta = models.DateField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cliente.actualizar_clasificacion()



class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    

class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)