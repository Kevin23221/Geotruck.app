from django.contrib import admin
from django.urls import path
from tareas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('inscripcion/', views.inscripcion, name='inscripcion'),
    path('tareas/', views.rutas, name='tareas'),
]
