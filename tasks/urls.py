from django.urls import path
from . import views

urlpatterns = [
    # Si el usuario no pone nada en la ruta, va al inicio
    path('', views.inicio, name='inicio'),
    
    # Si el usuario entra a /agendar/, va al formulario
    path('agendar/', views.agendar_cita, name='agendar_cita'),

    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    path('mis-vehiculos/', views.mis_vehiculos, name='mis_vehiculos'),
    path('inventario/', views.inventario, name='inventario'),
]