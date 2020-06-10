from ..confuguracion import *
import pandas as pd
from django.shortcuts import render
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def menuPracticas(request):
    grupo = request.GET.get('grupo')
    return render(request, "menuPracticas.html", {"grupo":grupo})

def agregarPractica(request):
    grupo = request.GET.get('grupo')
    return render(request, "agregarPracticaLaboratorio.html", {"grupo": grupo})

def verPracticas(request):
    arregloPracticas = []
    grupoSeleccionado = request.GET.get('grupo')
    grupos = database.child('Grupos').get()
    for grupo in grupos.each():
        if grupo.val()['Codigo'] == grupoSeleccionado:
            idGrupo = grupo.key()
            practicas = database.child('Grupos').child(idGrupo).child('Practicas').get()
            for practica in practicas.each():
                arregloPracticas.append(practica.val()['Nombre Practica'])

    for i in arregloPracticas:
        print(i)
    return render(request, "listaPracticas.html", {"grupo": grupoSeleccionado, "arregloPracticas":arregloPracticas})

def actualizarFormulario(request):
    grupoSeleccionado = request.GET.get('grupo')
    practicaSeleccionada = request.GET.get('practica')
    grupos = database.child('Grupos').get()
    idGrupo = "Default"
    for grupo in grupos.each():
        if grupo.val()['Codigo'] == grupoSeleccionado:
            idGrupo = grupo.key()
            break
    if idGrupo != "Default":
        practicas = database.child('Grupos').child(idGrupo).child('Practicas').get()
        for practica in practicas.each():
            if practica.val()['Nombre Practica'] == practicaSeleccionada:
                idPractica = practica.key()
                cantidadExperimentos = practica.val()['Cantidad Experimentos']
                fechaMaximaEntrega = practica.val()['Fecha Maxima Realizacion']
                arregloCampos = practica.val()['Campos']
                break
        stringCampos = ""
        for i in range(0,len(arregloCampos)):
            stringCampos = stringCampos+str(arregloCampos[i])+"\n"
        return render(request, "formularioActualizarPracticaLaboratorio.html", {"grupo": grupoSeleccionado, "practica": practicaSeleccionada, "cantidadExperimentos": cantidadExperimentos, "fechaMaximaEntrega": fechaMaximaEntrega, "campos":stringCampos, "idPractica":idPractica})

def actualizar(request):
    grupoSeleccionado = request.GET.get('grupo')
    practicaSeleccionada = request.GET.get('idpractica')
    experimentos = request.POST.get('experimetos')
    fechaMaxima = request.POST.get('fecha')
    campos = request.POST.get('expecificaciones')
    nombrePractica = request.POST.get('nombrePractica')
    validar = True
    while (validar == True):
        if campos[len(campos)-1] == "\n":
            campos = campos[0:len(campos)-2]
        else:
            validar = False
    arregloCampos = str(campos).split("\n")
    for i in range(0, len(arregloCampos)):
        if i != len(arregloCampos) - 1:
            aux = arregloCampos[i]
            aux = aux[0:len(aux) - 1]
            arregloCampos[i] = aux
    informacionPractica = {
        "Nombre Practica": nombrePractica,
        "Cantidad Experimentos": experimentos,
        "Fecha Maxima Realizacion": fechaMaxima,
        "Campos": arregloCampos
    }
    grupos = database.child('Grupos').get()
    for grupo in grupos.each():
        if grupo.val()['Codigo'] == grupoSeleccionado:
            idGrupo = grupo.key()
            database.child('Grupos').child(idGrupo).child('Practicas').child(practicaSeleccionada).child('Campos').remove()
            database.child('Grupos').child(idGrupo).child('Practicas').child(practicaSeleccionada).set(informacionPractica)
    mensaje = "Se modifico Correctamente la Practica " + str(nombrePractica)
    return render(request, "menuPracticas.html", {"grupo": grupoSeleccionado, "mensaje": mensaje})

def eliminar(request):
    grupoSeleccionado = request.GET.get('grupo')
    practicaSeleccionada = request.GET.get('practica')
    grupos = database.child('Grupos').get()
    idGrupo = "Default"
    for grupo in grupos.each():
        if grupo.val()['Codigo'] == grupoSeleccionado:
            idGrupo = grupo.key()
            break
    if idGrupo != "Default":
        practicas = database.child('Grupos').child(idGrupo).child('Practicas').get()
        for practica in practicas.each():
            if practica.val()['Nombre Practica'] == practicaSeleccionada:
                idPractica = practica.key()
                database.child('Grupos').child(idGrupo).child('Practicas').child(idPractica).remove()
                break
        mensaje = "Se Elimino correctamene la practica " + str(practicaSeleccionada)
    else:
        mensaje = "Ocurrio un error inesperado"
    return render(request, "menuPracticas.html", {"grupo": grupoSeleccionado, "mensaje": mensaje})

def realizar(request):
    contador = 0
    contadorAux = 0
    estudiante = request.GET.get('estudiante')
    grupo = request.GET.get('grupo')
    practicaSeleccionada = request.GET.get('practica')
    idGrupo = "Default"
    verificar = False

    grupos = database.child('Grupos').get()
    for grupoMierda in grupos.each():
        if grupoMierda.val()['Codigo'] == grupo:
            idGrupo = grupoMierda.key()
            break

    if idGrupo != "Default":
        practicas = database.child('Grupos').child(idGrupo).child('Practicas').get()
        experimentos = ""
        campos = []
        experimentosRealizados = []
        for practica in practicas.each():
            if practica.val()['Nombre Practica'] == practicaSeleccionada:
                experimentos = practica.val()['Cantidad Experimentos']
                campos = practica.val()['Campos']
                break


        usuarios = database.child('Usuarios').get()
        for usuario in usuarios.each():
            informacionUsuario = usuario.val()['Informacion']
            if informacionUsuario['Correo'] == estudiante:
                idUsuario = usuario.key()
                break

        practicas = database.child('Usuarios').child(idUsuario).child('Practicas').get()
        try:
            for practica in practicas.each():
                contadorAux = contadorAux + 1
                print("Nombre: " + str(practica.val()['Nombre Practica']) + " seelcted: " + str(practicaSeleccionada))
                if practica.val()['Nombre Practica'] == practicaSeleccionada:
                    idPractica = practica.key()
                    break
            experimentosUsuario = database.child('Usuarios').child(idUsuario).child('Practicas').child(idPractica).child('Experimentos').get()
            arregloAux = []
            for experimentoUser in experimentosUsuario.each():
                while contador < len(campos):
                    arregloAux.append(experimentoUser.val()[campos[contador]])
                    contador = contador + 1
                experimentosRealizados.append(arregloAux)
                arregloAux = []
                contador = 0
        except:
            verificar = True

        arregloAux = []
        descripcionPractica = {
            "Nombre Practica": practicaSeleccionada,
            "Experimentos": arregloAux,
            "Estado": "Activa",
        }
        if contadorAux == 0 and verificar == True:
            database.child('Usuarios').child(idUsuario).child('Practicas').push(descripcionPractica)
        elif verificar == True:
            database.push(descripcionPractica)


        return render(request, "desarrolloPractica.html",
                      {"estudiante": estudiante, "grupo": grupo, "practica": practicaSeleccionada,
                       "experimentos": experimentos, "arregloCampos": campos,
                       "arregloExperimentos": experimentosRealizados})

def terminarPractica(request):
    creacionArchivoExcel = {}
    contador = 0
    arregloPracticas = []
    practicaTerminada = request.GET.get('practica')
    emailEstudiante = request.GET.get('estudiante')
    grupoPractica = request.GET.get('grupo')
    idUsuario = ""
    idGrupo = ""
    idPractica = ""
    campos = []

    usuarios = database.child('Usuarios').get()

    for usuario in usuarios.each():
        informacionUsuario = usuario.val()['Informacion']
        if informacionUsuario['Correo'] == emailEstudiante:
            idUsuario = usuario.key()
            break

    grupos = database.child('Grupos').get()
    for grupo in grupos.each():
        if grupo.val()['Codigo'] == grupoPractica:
            idGrupo = grupo.key()
            break

    practicas = database.child('Grupos').child(idGrupo).child('Practicas').get()
    for practica in practicas.each():
        if practica.val()['Nombre Practica'] == practicaTerminada:
            campos = practica.val()['Campos']
            break

    practicas = database.child('Usuarios').child(idUsuario).child('Practicas').get()
    for practica in practicas.each():
        if practica.val()['Nombre Practica'] == practicaTerminada:
            idPractica = practica.key()
            database.child('Usuarios').child(idUsuario).child('Practicas').child(idPractica).child("Estado").set("Terminada")
            break

    experimentosRealizados = database.child('Usuarios').child(idUsuario).child('Practicas').child(idPractica).child("Experimentos").get()

    while contador < len(campos):
        arregloAux = []
        for experimentoUser in experimentosRealizados.each():
            arregloAux.append(float(experimentoUser.val()[campos[contador]]))
            creacionArchivoExcel[campos[contador]] = arregloAux
        contador = contador + 1

    data = pd.DataFrame(creacionArchivoExcel)
    outfile = r'templates/PracticaLaboratorio.xlsx'
    writer = pd.ExcelWriter(outfile, engine="xlsxwriter", )
    data.to_excel(writer, sheet_name="Consulta", index=None)
    writer.save()

    # Iniciamos los parámetros del script
    remitente = 'lidacoacompany@gmail.com'
    destinatarios = [emailEstudiante]
    asunto = 'Practica de Laboratorio ' + str(practicaTerminada)
    cuerpo = 'Practica Realizada: ' + str(practicaTerminada)+ ' Del grupo: ' + str(grupoPractica)+ '\n Este es un mensaje automatico, por favor no responder'
    ruta_adjunto = 'templates/PracticaLaboratorio.xlsx'
    nombre_adjunto = 'PracticaLaboratorio.xlsx'

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()

    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto

    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')

    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)

    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)

    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login('lidacoacompany@gmail.com', 'Lidacoa123*')

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()

    practicas = database.child('Grupos').child(idGrupo).child('Practicas').get()
    for practica in practicas.each():
        arregloPracticas.append(practica.val()['Nombre Practica'])

    mensajePagia = "La practica fue enviada correctamente a tu correo electronico"
    return render(request, "paginaEstudiante.html", {"mensaje": mensajePagia, "arregloPracticas":arregloPracticas, "grupo":grupoPractica})

def agregarExperimento(request):
    practicaSeleccionada = request.GET.get('practica')
    emailEstudiante = request.GET.get('estudiante')
    experimentos = request.GET.get('experimentos')
    grupoSeleccionado = request.GET.get('grupo')
    idGrupo = "Default"
    campos = []
    experimentoRealizado = {}
    idUsuario = ""
    experimentosRealizados = []
    contador = 0
    idPracticaUser = ""

    grupos = database.child('Grupos').get()
    for grupo in grupos.each():
        if grupo.val()['Codigo'] == grupoSeleccionado:
            idGrupo = grupo.key()
            break

    if idGrupo != "Default":
        practicas = database.child('Grupos').child(idGrupo).child('Practicas').get()

        for practica in practicas.each():
            if practica.val()['Nombre Practica'] == practicaSeleccionada:
                campos = practica.val()['Campos']

    for i in range(0,len(campos)):
        experimentoRealizado[campos[i]] = request.POST.get(campos[i])
    usuarios = database.child('Usuarios').get()
    for usuario in usuarios.each():
        informacionUsuario = usuario.val()['Informacion']
        if informacionUsuario['Correo'] == emailEstudiante:
            idUsuario = usuario.key()
            break

    practicasUsuario = database.child('Usuarios').child(idUsuario).child('Practicas').get()
    for practicaUser in practicasUsuario.each():
        if practicaUser.val()['Nombre Practica'] == practicaSeleccionada:
            idPracticaUser = practicaUser.key()
            database.child('Usuarios').child(idUsuario).child('Practicas').child(idPracticaUser).child('Experimentos').push(experimentoRealizado)

    experimentosUsuario = database.child('Usuarios').child(idUsuario).child('Practicas').child(idPracticaUser).child('Experimentos').get()
    arregloAux = []
    for experimentoUser in experimentosUsuario.each():
        while contador < len(campos):
            arregloAux.append(experimentoUser.val()[campos[contador]])
            contador = contador + 1
        experimentosRealizados.append(arregloAux)
        arregloAux = []
        contador = 0

    return render(request, "desarrolloPractica.html", {"estudiante": emailEstudiante, "grupo": grupoSeleccionado, "practica": practicaSeleccionada,"experimentos": experimentos, "arregloCampos": campos,"arregloExperimentos": experimentosRealizados})


def asignacionPractica(request):
    arregloPractica = []
    arregloContador = []
    grupo = request.GET.get('grupo')
    experimentos = request.POST.get('experimetos')
    fechaMaxima = request.POST.get('fecha')
    nombre = request.POST.get('nombrePractica')
    especificaciones = request.POST.get('expecificaciones')
    arregloCampos = str(especificaciones).split("\n")
    for i in range(0,len(arregloCampos)):
        if i != len(arregloCampos)-1:
            aux = arregloCampos[i]
            aux = aux[0:len(aux)-1]
            arregloCampos[i] = aux
    grupos = database.child('Grupos').get()
    for i in grupos.each():
        if i.val()['Codigo'] == grupo:
            id = i.key()

            informacionPractica = {
                "Nombre Practica": nombre,
                "Cantidad Experimentos":experimentos,
                "Fecha Maxima Realizacion": fechaMaxima,
                "Campos": arregloCampos
            }
            database.child('Grupos').child(id).child("Practicas").push(informacionPractica)

    for j in range(0,len(arregloCampos)):
        arregloPractica.append(arregloCampos[j])

    for i in range(0, int(experimentos)):
        arregloContador.append(i+1)

    mensaje = "La practica fue asignada correctamente"
    return render(request, "menuPracticas.html", {"mensaje": mensaje})