from ..confuguracion import *                   # Se acceder a datos necesarios en configuracion
from django.shortcuts import render             # Se importa la libreria de Render para el redireccionamiento de ventanas

# Metodo que direcciona a la ventana para el formulario para agregar un nuevo grupo al sistema
def formularioAgregarGrupo(request):
    return render(request,"agregarGrupoFormulario.html")

# Metodo para el registro de un nuevo grupo en el sistema
def registroGrupo(request):
    codigoGrupo = request.POST.get('codigoGrupo')                       # Se toma el parametro codigo del grupo que viene por metodo POST
    docente = request.POST.get('docente')                               # Se toma el parametro docente del grupo que viene por metodo POST
    horaClase = request.POST.get('horarioClase')                        # Se toma el parametro horario de la clase del grupo que viene por metodo POST
    horaLaboratorio = request.POST.get('horarioLaboratorio')            # Se toma el parametro horario de laboratorio del grupo que viene por metodo POST

    # Se determinan los datos del grupo para almecenarlo en la base de datos
    grupo = {
        "Codigo": codigoGrupo,
        "Docente": docente,
        "Horario Clase": horaClase,
        "Horario Laboratorio": horaLaboratorio
    }

    # Se almacena en la base de datos el grupo ingresado
    database.child('Grupos').push(grupo)

    # Se direcciona a la ventana principal de los docentes
    mensaje = "Se agrego correctamente el grupo " + str(codigoGrupo)
    return render(request, "controlGrupo.html", {"mensaje": mensaje})


# Metodo que muestra un listado de todos los grupos en el sistema
def listadoGrupos(request):
    arregloGrupos = []                              # arreglo de grupos, variable local

    # Se accede a los grupos que hay registrados en el sistema
    grupos = database.child('Grupos').get()

    for i in grupos.each():
        arregloGrupos.append(i.val()['Codigo'])

    # Se hace un ordenamiento de los grupos
    for i in range(0, len(arregloGrupos) - 1):
        for j in range(i + 1, len(arregloGrupos)):
            if arregloGrupos[j] < arregloGrupos[i]:
                arregloGrupos[i], arregloGrupos[j] = arregloGrupos[j], arregloGrupos[i]

    # Se direcciona a la ventana del listado de los grupos
    return render(request, "listaGrupos.html", {"arregloGrupos":arregloGrupos})


# Metodo para actualizar un grupo (Envia a un formulario los datos de un determinado grupo)
def actualizar(request):
    codigoGrupoSeleccionado = request.GET.get('grupo')              # Codigo del grupo seleccionado

    # Se accede a los grupos registrados en el sistema
    grupos = database.child('Grupos').get()

    for i in grupos.each():
        # Si se llega al grupo seleccionado, se toman los datos de ese grupo y se envian a un formulario para realizar la actualizacion
        if i.val()['Codigo'] == codigoGrupoSeleccionado:
            id = i.key()
            codigo = i.val()['Codigo']
            docente = i.val()['Docente']
            horaClase = i.val()['Horario Clase']
            horaLaboratorio = i.val()['Horario Laboratorio']
            return render(request, "actualizarGrupo.html", {"id":id, "codigo": codigo, "docente": docente, "horaClase": horaClase, "horaLaboratorio": horaLaboratorio})
        else:
            None

# Metdo para actualizar los datos de un grupo
def actualizarGrupo(request):
    # Se toman todos los datos del grupo, no importa que uno de ellos no cambie
    idGrupo = request.GET.get('id')                                        # Se toma el id del grupo que se va a modificar, este valor viene por metodo POST
    codigoGrupo = request.POST.get('codigoGrupo')                          # Se toma el codigo del grupo que se va a modificar, este valor viene por metodo POST
    docente = request.POST.get('docente')                                  # Se toma el docente del grupo que se va a modificar, este valor viene por metodo POST
    horaClase = request.POST.get('horarioClase')                           # Se toma el horario de clase grupo que se va a modificar, este valor viene por metodo POST
    horaLaboratorio = request.POST.get('horarioLaboratorio')               # Se toma el horario de laboratorio del grupo que se va a modificar, este valor viene por metodo POST

    # Se determina la nueva informacion del grupo
    nuevaInformacion = {
        "Codigo": codigoGrupo,
        "Docente": docente,
        "Horario Clase": horaClase,
        "Horario Laboratorio": horaLaboratorio
    }

    database.child('Grupos').child(idGrupo).update(nuevaInformacion)        # Por medio de la sentencia update se modifican los datos del grupo seleccionado
    mensaje = "Se actualizo correctamente el grupo " + str(codigoGrupo)
    return render(request, "controlGrupo.html", {"mensaje": mensaje})

# Metodo para eliminar un determinado grupo
def eliminar(request):
    verificar = False                                   # Variable local verificar, con el fin de verificar si el grupo si esta registrado en el sistema
    grupoSeleccionado = request.GET.get('grupo')        # Se toma el nombre del grupo que se desee eliminar, este parametro viene por metodo POST

    # Se accede a los grupos que hay registrados en el sistema
    grupos = database.child('Grupos').get()
    for i in grupos.each():
        if i.val()['Codigo'] == grupoSeleccionado:      # Si se encuentra que el grupo buscado esta registrado, se pone la variable verificar en True
            id = i.key()
            database.child('Grupos').child(id).remove() # Se elimina el grupo
            verificar = True

    # Si se elimina el grupo, se muestra un mensaje de exito
    if verificar == True:
        mensaje = "El grupo fue eliminado correctamente"
    else:
    # De lo contrario se muestra un mensaje de error
        mensaje = "Ocurrio un error al eliminar el grupo"
    return render(request, "controlGrupo.html", {"mensaje": mensaje})

# Metodo para ver los resultados de los estudiantes de cada grupo de una practica especifica
def visualizarEstudiantesGrupo(request):
    arregloEstudiantes = []                             # Arreglo de estudiantes registrados en el grupo seleccioando
    grupoSeleccionado = request.GET.get('grupo')        # Grupo selecionado, este parametor viene por metodo POST
    practicaSeleccionada = request.GET.get('practica')  # Practica seleccionada, este parametro viene por metodo POST

    # Se accede a todos los usuarios registrados en el sistema
    usuarios = database.child('Usuarios').get()
    for usuario in usuarios.each():
        informacionUsuario = usuario.val()['Informacion']
        # Si el usuario pertenece al grupo seleccionado, se agrega el arreglo de estudiantes
        if informacionUsuario['Grupo'] == grupoSeleccionado:
            arregloEstudiantes.append(informacionUsuario['Nombre'])

    # Se direcciona a la ventana donde se veran todos los estudiantes del grupo
    return render(request, "verEstudiantesPractica.html", {"arregloEstudiantes": arregloEstudiantes, "grupo": grupoSeleccionado, "practica": practicaSeleccionada})


# Metodo que muestra los resultados de un estudiante en especifico
def resultadosEstudiante(request):
    arregloPracticas = []                                               # Arreglo de practicas, en caso de que el estudiante no tenga practica entregada, se direcciona a la ventana de visualizacion de las practicas del grupo seleccionado
    estudianteSeleccionado = request.GET.get('estudiante')              # Estudiante seleccionado, este parametro viene por metodo POST
    grupoSeleccionado = request.GET.get('grupo')                        # Grupo del estudiante seleccionado, este parametro viene por metodo POST
    practicaSeleccionada = request.GET.get('practica')                  # Practica seleccionada a revisar, este parametro viene por metodo POST
    idEstudiante = ""                                                   # Variable local para el id del estudiante
    idGrupo = ""                                                        # Varaible local para el id del grupo
    idPractica = ""                                                     # Variable local para el id de la practica
    campos = []                                                         # Campos de la practica seleccionada
    experimentosRealizados = []                                         # Experimentos realizados por el estudiante
    contador = 0                                                        # Varaible contador (variable auxiliar)

    # Se determina el id del usuario
    usuarios = database.child('Usuarios').get()
    for usuario in usuarios.each():
        informacionUsuario = usuario.val()['Informacion']
        if informacionUsuario['Nombre'] == estudianteSeleccionado:
            idEstudiante = usuario.key()
            break

    # Se determina el id del grupo
    grupos = database.child('Grupos').get()
    for grupo in grupos.each():
        if grupo.val()['Codigo'] == grupoSeleccionado:
            idGrupo = grupo.key()
            break

    # Se determinan los campos de la practica seleccionada
    practicasGrupo = database.child('Grupos').child(idGrupo).child('Practicas').get()
    for practicaGrupo in practicasGrupo.each():
        arregloPracticas.append(practicaGrupo.val()['Nombre Practica'])
        if practicaGrupo.val()['Nombre Practica'] == practicaSeleccionada:
            campos = practicaGrupo.val()['Campos']

    practicasUsuario = database.child('Usuarios').child(idEstudiante).child('Practicas').get()
    for practica in practicasUsuario.each():
        # Si el estudiante no ha finalizado la practica, se muestra un mensaje de que el estudiante no ha realizado la entrega
        if practica.val()['Estado'] == 'Activa' and practica.val()['Nombre Practica'] == practicaSeleccionada:
            mensaje = "El estudiante no realizo entrega de la practica"
            return render(request, "listaPracticas.html",{"mensaje":mensaje, "grupo":grupoSeleccionado, "arregloPracticas":arregloPracticas})
        else:
            # En caso contrario se determina el id de la practica
            idPractica = practica.key()
        break

    # Se acceden a los experimentos realizados por el estudiante, en la practica determinada
    experimentosUsuario = database.child('Usuarios').child(idEstudiante).child('Practicas').child(idPractica).child('Experimentos').get()
    arregloAux = []
    for experimentoUser in experimentosUsuario.each():
        while contador < len(campos):
            arregloAux.append(experimentoUser.val()[campos[contador]])
            contador = contador + 1
        experimentosRealizados.append(arregloAux)
        arregloAux = []
        contador = 0

    # Se direcciona a la pagina donde se muestra una tabla con los experimentos realizados por el estudiante
    return render(request, "tablaEstudiante.html",{"grupo": grupoSeleccionado, "arregloCampos": campos, "arregloExperimentos": experimentosRealizados, "estudiante": estudianteSeleccionado, "practica": practicaSeleccionada})


