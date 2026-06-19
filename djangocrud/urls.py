from django.contrib import admin
from django.urls import path
from tareas import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('inscripcion/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tareas/', views.rutas, name='rutas'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/rutas/', views.rutas, name='rutas'),                                       
    path('rutas/agregar/', views.agregar_ruta, name='agregar_ruta'),                  
    path('rutas/eliminar/<int:ruta_id>/', views.eliminar_ruta, name='eliminar_ruta'),
    path('dashboard/vehiculos/', views.vehiculos, name='vehiculos'),
    path('vehiculos/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)