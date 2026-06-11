from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

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
            return redirect('rutas')

    return render(request, 'inscripcion.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def rutas(request):
    return render(request, 'tareas.html')
