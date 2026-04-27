from django.contrib import admin
from django.urls import path, include
from tasks import views # se importan las vistas que se crearon anteriormente

urlpatterns = [
    path('admin/', admin.site.urls), #panel azul
    path('panel/', views.inicio, name='panel'),# nueva pag 
    path ('', include('tasks.urls')),
]
