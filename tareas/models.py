from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    distancia_km = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion = models.TextField(blank=True)
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origen} → {self.destino} ({self.distancia_km} km)"
    

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    destino_asignado = models.CharField(max_length=100, blank=True)
    conductor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehiculos')
    foto = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"