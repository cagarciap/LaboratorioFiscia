from ..confuguracion import *         # Se acceder a datos necesarios en configuracion
from ..confuguracion import authe     # Se importa la libreria de Autenticacion de firebase para manejo de Django
from django.shortcuts import render   # Se importa la libreria de Render para el redireccionamiento de ventanas

# Metodo que direcciona a la ventana de inicio de sesion
def signIn(request):
    return render(request, "inicioSesion.html")

# Medodo que cierra la sesion y direcciona a la pagina principal: inicio de sesion
def logout(request):
    auth.logout(request)
    return render(request,'inicioSesion.html')


"""def signUp(request):
    return render(request,"signUp.html")"""

# Metodo que inicia la sesion
def postsign(requets):

    email = requets.POST.get('email')           # Se toma el parametro de usuario que llega por metodo POST
    passw = requets.POST.get("passw")           # Se toma el parametro de contraseña que llega por metodo POST
    permisos = ""                               # Variable local que determina los permisos del usuario (Estudiante)
    grupo = ""                                  # Variavle local que determina el nombre del grupo del usuario (Estudiante)
    idGrupoEstudiante = "Default"               # Varivale local que determina el id del grupo del estudiante, por defecto es Default
    arregloPracticas = []                       # Arreglo de practicas que hay activas para el grupo

    # Trate de iniciar la sesion
    try:
        user= authe.sign_in_with_email_and_password(email,passw)            # Se inicia la sesion
    except:
    # En caso contrario: datos invalidos de usuario y/o contraseña
        message= "credencial invalida"
        return render(requets,"inicioSesion.html",{"messg":message})        # Vuelva a la pagina principal y muestre mensaje de error de usuario y/o contraseña

    # Se activa la sesion
    session_id=user['idToken']
    requets.session['uid']=str(session_id)

    # Se obtienen todos los usuarios registrados en el sistema
    usuarios = database.child('Usuarios').get()


    for usuario in usuarios.each():
        # Accedo a la informacion del usuario. Nota: No se accede a la contraseña por seguridad
        informacionUsuario = usuario.val()['Informacion']

        # Si el usuario es el que inicia la sesion, determino el grupo y los permisos del estudiante. Nota: permisos hace referencia a:
        """Si es un estudiante solo podra realizar practicas de laboratorio, si es un docente podra agregar grupos, agregar practicas a los grupos y tener un 
        control de estos aspectos"""
        if informacionUsuario['Correo'] == email:
            permisos = informacionUsuario['Estado']
            grupo = informacionUsuario['Grupo']
            break

    if permisos == "estudiante":                # Es decir, si es estudiante
        grupos = database.child('Grupos').get()
        for grupoBaseDatos in grupos.each():
            # Determino el id del grupo del estudiante
            if grupoBaseDatos.val()['Codigo'] == grupo:
                idGrupoEstudiante = grupoBaseDatos.key()
                break
        if idGrupoEstudiante != "Default":
            # Accedo a las practicas que hay activas para el grupo
            practicas = database.child('Grupos').child(idGrupoEstudiante).child('Practicas').get()
            for practica in practicas.each():
                arregloPracticas.append(practica.val()['Nombre Practica'])
            # Si es un estudiante se direcciona a la ventana principal del estudiante
            return render(requets, "paginaEstudiante.html", {"email": email, "arregloPracticas":arregloPracticas, "grupo": grupo})
    else:
        # Si es un docente se direcciona a la ventana principal del docente
        return render(requets, "controlGrupo.html", {"email": email})


"""def postsignup(request):
    name = request.POST.get('name')     
    email = request.POST.get('email')
    passw = request.POST.get('passw')

    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
    except:
        message = "Unable to create acocount try again"
        return render(request, "signUp.html", {"messg": message})

    data = {"name": name}
    database.child("users").child(uid).child("details").set(data)

    return render(request, "signIn.html")"""


# Metodo que direcciona a la ventana de registro de un estudiante. Nota: es importante mostrar los grupos activos para que el estudiante se pueda registrar con su grupo correspondiente
def registroFormulario(request):
    # Creo un arreglo con los grupos que hay activos
    grupos = database.child('Grupos').get()
    arregloGrupos = []
    for i in grupos.each():
        arregloGrupos.append(i.val()['Codigo'])
    # Direcciono a la ventana del formulario de registro
    return render(request, "formularioRegistro.html",{"arregloGrupos":arregloGrupos})


# Metodo para el registro de un usuario
def registroUsuario(request):
    nombre = request.POST.get('nombre')         # Tomo el parametro nombre que viene por metodo POST
    correo = request.POST.get('email')          # Tomo el parametro correo que viene por metodo POST
    password = request.POST.get('passw')        # Tomo el parametro contraseña que viene por metodo POST
    grupo = request.POST.get('grupo')           # Tomo el parametro grupo que viene por metodo POST
    validar = False                             # Metodo para validar si un usuario ya esta registrado en el sistema

    # Busco en los usuarios registrados, si el usuario que esta intentando registrarse, ya se encuentra registrado
    usuarios = database.child('Usuarios').get()
    for usuario in usuarios.each():
        infoEstudiante = usuario.val()['Informacion']
        nombreEstudiante = infoEstudiante['Nombre']
        if nombre == nombreEstudiante:
            validar = True          # En caso verdadero, validar se pone en True y no permite el registro
            break

    # Si no se encontro un usuario se procede con el registro
    if validar == False:
        try:
            user = authe.create_user_with_email_and_password(correo, password)      # Se crea el usuario por medio del servicio de autenticacion de firebase
            uid = user['localId']
        except:
            mensaje = "Intentalo de nuevo, ocurrio un error"                        # Si hay error al crear el usuario se muestra el error
            return render(request, "formularioRegistro.html", {"mensaje": mensaje})

        # Se determinan los datos del estudiante
        data = {
            "Nombre": nombre,
            "Correo":correo,
            "Grupo":grupo,
            "Estado":"estudiante",
        }

        # Se almacena el estudiante en la base de datos
        database.child("Usuarios").child(uid).child("Informacion").set(data)
        mensaje = "El estudiante fue registrado correctamente"

    else:
        mensaje = "Error: El estudiante con correo electronico " + str(correo) + " ya está registrado en el sistema"

    # Una vez el proceso termine (bien sea que se registre o no el usuario) se direcciona a la ventana de inicio de sesion
    return render(request, "inicioSesion.html", {"mensaje":mensaje})
