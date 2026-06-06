from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

def home(request):
    return render(request, 'home.html')

def inscripcion(request):

    if request.method == "GET":
        return render (request, 'inscripcion.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'inscripcion.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe.'
                })
        return render(request, 'inscripcion.html', {
                    'form': UserCreationForm,
                    'error': 'Contraseña no coincide.'
        })

def rutas(request):
    return render(request, 'tareas.html')