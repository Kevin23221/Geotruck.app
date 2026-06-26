from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Ruta, Vehiculo, Viaje, GastoViaje, EvidenciaViaje
from decimal import Decimal
import json

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # Validaciones de seguridad
        if not username or not email or not password1:
            messages.error(request, 'Todos los campos son obligatorios.')
        elif password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Ese correo ya está registrado.')
        else:

            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f'¡Bienvenido a GeoTruck, {username}!')
            return redirect('dashboard')

    return render(request, 'inscripcion.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def rutas(request):
    lista_rutas = Ruta.objects.all().order_by('-fecha_creacion')
    return render(request, 'rutas.html', {'rutas': lista_rutas})

@login_required(login_url='login')
def agregar_ruta(request):
    if request.method == 'POST':
        origen      = request.POST.get('origen', '').strip()
        destino     = request.POST.get('destino', '').strip()
        distancia   = request.POST.get('distancia_km', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()

        if origen and destino and distancia:
            Ruta.objects.create(
                origen=origen,
                destino=destino,
                distancia_km=distancia,
                descripcion=descripcion,
                creada_por=request.user
            )
            messages.success(request, 'Ruta agregada correctamente.')
        else:
            messages.error(request, 'Origen, destino y distancia son obligatorios.')

    return redirect('rutas')

@login_required(login_url='login')
def eliminar_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id)

    if request.user.is_staff or ruta.creada_por == request.user:
        ruta.delete()
        messages.success(request, 'Ruta eliminada.')
    else:
        messages.error(request, 'No tienes permiso para eliminar esta ruta.')

    return redirect('rutas')

@login_required(login_url='login')
def vehiculos(request):
    lista = Vehiculo.objects.all().select_related('conductor')
    usuarios = User.objects.all()
    return render(request, 'vehiculos.html', {'vehiculos': lista, 'usuarios': usuarios})

@login_required(login_url='login')
def agregar_vehiculo(request):
    if request.method == 'POST':
        placa        = request.POST.get('placa', '').strip().upper()
        marca        = request.POST.get('marca', '').strip()
        modelo       = request.POST.get('modelo', '').strip()
        destino      = request.POST.get('destino_asignado', '').strip()
        conductor_id = request.POST.get('conductor_id')
        foto         = request.FILES.get('foto')

        if placa and marca and modelo:
            if Vehiculo.objects.filter(placa=placa).exists():
                messages.error(request, 'Ya existe un vehículo con esa placa.')
            else:
                conductor = User.objects.filter(id=conductor_id).first() if conductor_id else None
                Vehiculo.objects.create(
                    placa=placa,
                    marca=marca,
                    modelo=modelo,
                    destino_asignado=destino,
                    conductor=conductor,
                    foto=foto
                )
                messages.success(request, 'Vehículo agregado correctamente.')
        else:
            messages.error(request, 'Placa, marca y modelo son obligatorios.')

    return redirect('vehiculos')

@login_required(login_url='login')
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    if request.user.is_staff or vehiculo.conductor == request.user:
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este vehículo.')

    return redirect('vehiculos')


def mapa_view(request):

    rutas_activas = Ruta.objects.filter(activa=True).select_related('conductor')

    ubicaciones = []

    for ruta in rutas_activas:
        if ruta.lat_actual is not None and ruta.lng_actual is not None:
            ubicaciones.append({
                "lat": ruta.lat_actual,
                "lng": ruta.lng_actual,
                "conductor": ruta.conductor.username if ruta.conductor else "Sin conductor",
                "origen": ruta.origen,
                "destino": ruta.destino
            })

    context = {
        "ubicaciones_json": json.dumps(ubicaciones),
        "total_rutas": rutas_activas.count(),
    }

    return render(request, "mapas.html", context)

CATS_OP = {'Peaje', 'Combustible', 'Manifiesto de carga'}

@login_required(login_url='login')
def viaje_crear(request):
    if request.method == 'POST':
        v = Viaje.objects.create(
            conductor_nombre   = request.POST.get('conductor_nombre', ''),
            conductor_licencia = request.POST.get('conductor_licencia', ''),
            conductor_cedula   = request.POST.get('conductor_cedula', ''),
            placa              = request.POST.get('placa', ''),
            modelo             = request.POST.get('modelo', ''),
            fecha_salida       = request.POST.get('fecha_salida') or None,
            fecha_llegada      = request.POST.get('fecha_llegada') or None,
            origen             = request.POST.get('origen', ''),
            destino            = request.POST.get('destino', ''),
            km_recorridos      = request.POST.get('km_recorridos') or None,
            tipo_carga         = request.POST.get('tipo_carga', ''),
            recursos           = request.POST.get('recursos', ''),
            observaciones      = request.POST.get('observaciones', ''),
        )
        descs  = request.POST.getlist('gastos_descripcion[]')
        cats   = request.POST.getlist('gastos_categoria[]')
        montos = request.POST.getlist('gastos_monto[]')
        op = ad = Decimal('0')
        for desc, cat, monto in zip(descs, cats, montos):
            if monto:
                val = Decimal(monto)
                GastoViaje.objects.create(viaje=v, descripcion=desc, categoria=cat, monto=val)
                if cat in CATS_OP: op += val
                else: ad += val
        v.total_operativo = op
        v.total_adicional = ad
        v.total_viaje     = op + ad
        v.save()
        for img in request.FILES.getlist('evidencias'):
            EvidenciaViaje.objects.create(viaje=v, imagen=img)
        return redirect('viaje-historial')

    viajes = Viaje.objects.order_by('-creado_en')
    return render(request, 'bitacoras.html', {'viajes': viajes})