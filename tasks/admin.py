from django.contrib import admin
from .models import Vehiculo, Repuesto, Cita, Reparacion # Importamos todos los modelos

# 1. Configuración del panel de Vehículos
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'anio', 'propietario')
    search_fields = ('placa', 'marca', 'modelo')
    list_filter = ('marca', 'anio')

# 2. Configuración del panel de Citas (¡Corregido!)
class CitaAdmin(admin.ModelAdmin):
    # Usamos los nombres exactos: fecha_hora y motivo_servicio
    list_display = ('vehiculo', 'cliente', 'fecha_hora', 'motivo_servicio', 'estado')
    list_filter = ('estado', 'fecha_hora')
    search_fields = ('vehiculo__placa', 'motivo_servicio', 'cliente__username')
    list_editable = ('estado',)

# 3. Configuración del panel de Repuestos
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_disponible', 'precio')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)

# 4. Configuración del panel de Reparaciones (¡Nuevo!)
class ReparacionAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'estado', 'fecha_ingreso', 'fecha_salida')
    list_filter = ('estado', 'fecha_ingreso')
    search_fields = ('vehiculo__placa',)
    list_editable = ('estado',)

# Registramos los modelos junto con su configuración
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(Repuesto, RepuestoAdmin)
admin.site.register(Reparacion, ReparacionAdmin)

# Un toque estético para cambiar el título superior del panel
admin.site.site_header = "Administración del Sistema"
admin.site.site_title = "Panel de Control"
admin.site.index_title = "Gestión Interna"