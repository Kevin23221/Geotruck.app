from django.contrib import admin
from django.urls import path
from tareas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('inscripcion/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('dashboard/rutas/', views.rutas, name='rutas'),
    path('rutas/agregar/', views.agregar_ruta, name='agregar_ruta'),
    path('rutas/eliminar/<int:ruta_id>/', views.eliminar_ruta, name='eliminar_ruta'),

    path('dashboard/vehiculos/', views.vehiculos, name='vehiculos'),
    path('vehiculos/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),

    path('dashboard/mapas', views.mapa_view, name='mapas'),
    path('reportes/', views.reportes, name='reportes'),

    path('dashboard/bitacoras/', views.viaje_crear, name='viaje-crear'),
    path('dashboard/bitacoras/lista/', views.viaje_crear, name='viaje-historial'),
    path('dashboard/bitacoras/<int:viaje_id>/editar/', views.viaje_editar, name='viaje-editar'),

    path('dashboard/conductores/', views.conductores, name='conductores'),
    path('conductores/agregar/', views.agregar_conductor, name='agregar_conductor'),
    path('conductores/eliminar/<int:conductor_id>/', views.eliminar_conductor, name='eliminar_conductor'),

    path('api/guardar-ubicacion/', views.guardar_ubicacion, name='guardar_ubicacion'),
    path('api/ubicaciones-activas/', views.ubicaciones_activas, name='ubicaciones_activas'),
    path('conductor/', views.panel_conductor, name='panel_conductor'),
    path('api/ruta-conductor/<int:conductor_id>/', views.ruta_conductor, name='ruta_conductor'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)