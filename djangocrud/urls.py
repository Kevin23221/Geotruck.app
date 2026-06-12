from django.contrib import admin
from django.urls import path
from tareas import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inscripcion/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tareas/', views.rutas, name='rutas'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

