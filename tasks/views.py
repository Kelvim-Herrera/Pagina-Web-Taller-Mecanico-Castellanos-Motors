from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cita, Vehiculo

# Este decorador (@) es el primer nivel de "Roles y Privilegios". 
# Le dice a Django: "Expulsa a los visitantes anónimos, solo usuarios con cuenta pueden ver esto".
@login_required
def inicio(request):
    return render(request, 'inicio.html')

# Vista para el formulario de agendar cita
@login_required
def agendar_cita(request):
    if request.method == 'POST':
        # 1. Atrapamos los datos del HTML
        v_placa = request.POST.get('placa')
        v_marca = request.POST.get('marca')
        v_fecha = request.POST.get('fecha')
        v_hora = request.POST.get('hora')
        v_servicio = request.POST.get('servicio')

        # 2. Resolver el Vehículo (Si no existe en la BD, lo creamos)
        vehiculo_obj, creado = Vehiculo.objects.get_or_create(
            placa=v_placa,
            defaults={
                'propietario': request.user,
                'marca': v_marca,
                'modelo': 'No especificado', 
                'anio': 2026 
            }
        )

        # 3. Unir la fecha y la hora en un solo formato para Django
        fecha_y_hora_combinada = f"{v_fecha} {v_hora}"

        # 4. Creamos la Cita usando los nombres exactos de tu models.py
        nueva_cita = Cita(
            cliente=request.user,          # Tu modelo usa 'cliente'
            vehiculo=vehiculo_obj,         # Le pasamos el objeto Vehiculo que encontramos o creamos
            fecha_hora=fecha_y_hora_combinada, # El campo DateTimeField
            motivo_servicio=v_servicio     # Tu modelo usa 'motivo_servicio'
        )
        nueva_cita.save() # Guardado exitoso

        messages.success(request, 'Cita agendada correctamente.')
        return redirect('inicio')
        
    return render(request, 'agendar_cita.html')

def login_view(request):
    if request.method == 'POST':
        # Capturamos los datos del formulario de login
        correo = request.POST.get('username') 
        password = request.POST.get('password')

        # Django verifica si existe un usuario con ese correo y esa contraseña
        user = authenticate(request, username=correo, password=password)

        if user is not None:
            # Si los datos son correctos, iniciamos la sesión
            login(request, user)
            return redirect('inicio') # Lo enviamos a la pantalla principal
        else:
            # Si se equivocó en algo, mostramos un mensaje de error
            messages.error(request, 'Correo o contraseña incorrectos.')
            
    # Si entra por GET, solo mostramos el formulario
    return render(request, 'login.html')

def registro_view(request):
    if request.method == 'POST':
        # Capturamos los datos que el usuario escribió en el HTML usando el atributo 'name'
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        # Validamos que el usuario no exista y lo creamos en la base de datos
        if not User.objects.filter(username=correo).exists():
            # Usamos el correo como 'username' para facilitar el login después
            user = User.objects.create_user(username=correo, email=correo, password=password, first_name=nombre, last_name=apellido)
            user.save()
            return redirect('login') # Si el registro es exitoso, lo enviamos a la pantalla de login
        else:
            # Si el correo ya existe, enviamos un mensaje de error
            messages.error(request, 'Este correo ya está registrado.')
    
    # Si entra por GET (solo cargando la página), mostramos el formulario vacío
    return render(request, 'registro.html')  
@login_required
def mis_citas(request):
    # Buscamos en la base de datos las citas del usuario actual.
    # Usamos select_related('vehiculo') para optimizar la consulta y traer los datos de la otra tabla de una vez.
    citas_usuario = Cita.objects.filter(cliente=request.user).select_related('vehiculo').order_by('-fecha_hora')
    
    # Le pasamos esos datos al HTML a través de un diccionario (contexto)
    contexto = {
        'citas': citas_usuario
    }
    return render(request, 'mis_citas.html', contexto) 