from django.db import models
from django.contrib.auth.models import User


class Ruta(models.Model):
    conductor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="rutas")
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    distancia_km = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion = models.TextField(blank=True)
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="rutas_creadas")
    lat_actual = models.FloatField(null=True, blank=True)
    lng_actual = models.FloatField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origen} → {self.destino}"


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


class UbicacionVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    lat = models.FloatField()
    lng = models.FloatField()
    velocidad = models.FloatField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)


class Conductor(models.Model):
    ESTADO_CHOICES = [
        ('activo',      'Activo'),
        ('inactivo',    'Inactivo'),
        ('en_ruta',     'En ruta'),
        ('suspendido',  'Suspendido'),
    ]
    nombre          = models.CharField(max_length=120)
    cedula          = models.CharField(max_length=30, unique=True)
    licencia        = models.CharField(max_length=60)
    telefono        = models.CharField(max_length=20, blank=True)
    email           = models.EmailField(blank=True)
    fecha_nacimiento= models.DateField(null=True, blank=True)
    fecha_ingreso   = models.DateField(auto_now_add=True)
    estado          = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    foto            = models.ImageField(upload_to='conductores/', null=True, blank=True)
    observaciones   = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"


class Viaje(models.Model):
    conductor_nombre   = models.CharField(max_length=120)
    conductor_licencia = models.CharField(max_length=60, blank=True)
    conductor_cedula   = models.CharField(max_length=30, blank=True)
    placa              = models.CharField(max_length=20)
    modelo             = models.CharField(max_length=80, blank=True)
    fecha_salida       = models.DateField(null=True, blank=True)
    fecha_llegada      = models.DateField(null=True, blank=True)
    origen             = models.CharField(max_length=150)
    destino            = models.CharField(max_length=150)
    km_recorridos      = models.PositiveIntegerField(null=True, blank=True)
    tipo_carga         = models.CharField(max_length=120, blank=True)
    recursos           = models.CharField(max_length=200, blank=True)
    observaciones      = models.TextField(blank=True)
    total_operativo    = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    total_adicional    = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    total_viaje        = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    creado_en          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origen} → {self.destino} ({self.placa})"


class GastoViaje(models.Model):
    CATEGORIA_CHOICES = [
        ('Peaje', 'Peaje'), ('Combustible', 'Combustible'),
        ('Manifiesto de carga', 'Manifiesto de carga'), ('Hospedaje', 'Hospedaje'),
        ('Almuerzo', 'Almuerzo'), ('Desayuno', 'Desayuno'), ('Cena', 'Cena'),
        ('Servicio mecánico', 'Servicio mecánico'), ('Otro', 'Otro'),
    ]
    viaje       = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='gastos')
    descripcion = models.CharField(max_length=200)
    categoria   = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    monto       = models.DecimalField(max_digits=12, decimal_places=0)


class EvidenciaViaje(models.Model):
    viaje  = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='evidencias')
    imagen = models.ImageField(upload_to='evidencias/')


class UbicacionConductor(models.Model):
    conductor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ubicaciones')
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conductor.username} - {self.timestamp}"