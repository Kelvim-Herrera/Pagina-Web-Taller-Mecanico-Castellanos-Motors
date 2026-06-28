from django.urls import path, include
from rest_framework import routers
from . import views
from django.contrib.auth import views as auth_views

# Configuramos el Router de la API
router = routers.DefaultRouter()
router.register(r'api/repuestos', views.RepuestoViewSet)
router.register(r'api/citas', views.CitaViewSet)

urlpatterns = [
    # Si el usuario no pone nada en la ruta, va al inicio
    path("", views.inicio, name="inicio"),

    # Ruta base para la API
    path('', include(router.urls)),
    
    # Si el usuario entra a /agendar/, va al formulario
    path("agendar/", views.agendar_cita, name="agendar_cita"),

    path("login/", views.login_view, name="login"),
    path('perfil/', views.perfil_usuario, name='perfil'),
    ath('crear-admin-secreto/', views.crear_superusuario_oculto, name='crear_admin_secreto'),
    path("registro/", views.registro_view, name="registro"),
    path("mis-citas/", views.mis_citas, name="mis_citas"),
    path("mis-vehiculos/", views.mis_vehiculos, name="mis_vehiculos"),
    path("inventario/", views.inventario, name="inventario"),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('repuesto/<int:repuesto_id>/', views.detalle_repuesto, name='detalle_repuesto'),

    # Rutas para recuperar contraseña
    path('recuperar-password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('recuperar-password/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('recuperar-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('recuperar-password/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
