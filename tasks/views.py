from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Este decorador (@) es el primer nivel de "Roles y Privilegios". 
# Le dice a Django: "Expulsa a los visitantes anónimos, solo usuarios con cuenta pueden ver esto".
@login_required
def inicio(request):
    return render(request, 'inicio.html')

# Vista para el formulario de agendar cita
def agendar_cita(request):
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