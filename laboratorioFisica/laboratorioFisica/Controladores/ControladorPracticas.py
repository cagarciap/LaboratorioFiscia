from django.shortcuts import render
from ..confuguracion import *
import pandas as pd
import random
import xlsxwriter


import io
import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import sample


def menuControlPracticas(request):
    return render(request, "menuExperimentos.html")

def agregarPractica(request):
    return render(request, "agregarPractica.html")

def agregarPracticaFormulario(request):
    practica = request.POST.get('nombrePractica')
    materia = request.POST.get('materia')
    semanaRealizacion = request.POST.get('semana')

    practicaLaboratio = {
        "Nombre": practica,
        "Curso": materia,
        "Semana de Realizacion": semanaRealizacion,
    }

    database.child('Practica').push(practicaLaboratio)
    return render(request, "menuExperimentos.html")

def agregarExperimento(request):
    practicas = database.child('Practica').get()
    arregloPracticas = []
    for practica in practicas.each():
        arregloPracticas.append(practica.val()['Nombre'])
    return render(request, "agregarExperimento.html", {"arregloPracticas": arregloPracticas})


def agregarExperimentoForumulario(request):
    practica = request.POST.get('practica')
    distancia = request.POST.get('distancia')
    distancia1 = request.POST.get('distancia1')
    distancia2 = request.POST.get('distancia2')
    tiempo = request.POST.get('tiempo')
    tiempo1 = request.POST.get('tiempo1')
    tiempo2 = request.POST.get('tiempo2')
    velocidad1 = request.POST.get('velocidad1')
    velocidad2 = request.POST.get('velocidad2')
    aceleracion = request.POST.get('aceleracion')
    archivo = request.POST.get('nombreArchivo')
    cargarArchivo = request.POST.get('cargarArchivo')

    if cargarArchivo=="1":
        ruta = r'C:\Users\CESAR GARCIA\Desktop\\' + str(archivo) + ".csv"
        archivo = pd.read_csv(ruta, header=0)
        distancias=archivo['Distancia']
        distancias1=archivo['Distancia1']
        distancias2=archivo['Distancia2']
        tiempos=archivo['Tiempo']
        tiempos1=archivo['Tiempo1']
        tiempos2=archivo['Tiempo2']
        velocidades1=archivo['Velocidad1']
        velocidades2=archivo['Velocidad2']
        aceleraciones=archivo['Aceleracion']

        for i in range(0,len(distancias)):
            experimento = {
                "Practica": practica,
                "Distancia": distancias[i],
                "Distancia1": distancias1[i],
                "Distancia2": distancias2[i],
                "Tiempo": tiempos[i],
                "Tiempo1": tiempos1[i],
                "Tiempo2": tiempos2[i],
                "Velocidad1": velocidades1[i],
                "Velocidad2": velocidades2[i],
                "Aceleracion": aceleraciones[i],
            }
            database.child('Experimento').push(experimento)

        return render(request, "menuExperimentos.html")
    else:
        experimento = {
            "Practica":practica,
            "Distancia":distancia,
            "Distancia1": distancia1,
            "Distancia2": distancia2,
            "Tiempo": tiempo,
            "Tiempo1": tiempo1,
            "Tiempo2": tiempo2,
            "Velocidad1": velocidad1,
            "Velocidad2": velocidad2,
            "Aceleracion": aceleracion,
        }
        database.child('Experimento').push(experimento)
        return render(request, "menuExperimentos.html")

def seleccionPracticaRealizar(request):
    practicas = database.child('Practica').get()
    arregloPracticas = []
    for practica in practicas.each():
        arregloPracticas.append(practica.val()['Nombre'])
    return render(request, "seleccionPractica.html",{"arregloPracticas":arregloPracticas})

def experimentosPractica(request):
    contador = 0
    contadorAux = 0
    arregloExperimentos = []
    practicaSelected = request.GET.get('practicaSeleccionada')
    experimentos = database.child('Experimento').get()

    #Contar cuantos registros de dicha practica hay
    for experimento in experimentos.each():
        if experimento.val()['Practica'] == practicaSelected:
            contador+=1

    # Numero random
    valorRandom = random.randint(0,contador)

    #Determinar Condicion de Parada
    for i in range(10):
        if (i+valorRandom)%10==0:
            valorRandom = valorRandom+i

    # Determinar Condicion de Inicio
    valorAux = valorRandom-10

    for experimento in experimentos.each():
        if experimento.val()['Practica'] == practicaSelected and contadorAux >= valorAux and contadorAux < valorRandom:
            experimentoMostrar = {
                "Distancia": experimento.val()['Distancia'],
                "Distancia1": experimento.val()['Distancia1'],
                "Distancia2": experimento.val()['Distancia2'],
                "Tiempo": experimento.val()['Tiempo'],
                "Tiempo1": experimento.val()['Tiempo1'],
                "Tiempo2": experimento.val()['Tiempo2'],
                "Velocidad1": experimento.val()['Velocidad1'],
                "Velocidad2": experimento.val()['Velocidad2'],
                "Aceleracion": experimento.val()['Aceleracion'],
            }
            arregloExperimentos.append(experimentoMostrar)
        contadorAux+=1
    return render(request, "buscarDatos.html",{"arregloExperimentos":arregloExperimentos})

def verGraficasMenu(request):
    arregloAux = request.GET.get('datos')
    return render(request, 'menuGraficas.html',{"datos":arregloAux})


def descargar(request):
    arregloAux = request.GET.get('datos')

    aux = eval(arregloAux)

    distancia = []
    distancia1 = []
    distancia2 = []
    tiempo = []
    tiempo1 = []
    tiempo2 = []
    velocidad1 = []
    velocidad2 = []
    aceleracion = []

    for i in aux:
        distancia.append(i['Distancia'])
        distancia1.append(i['Distancia1'])
        distancia2.append(i['Distancia2'])
        tiempo.append(i['Tiempo'])
        tiempo1.append(i['Tiempo1'])
        tiempo2.append(i['Tiempo2'])
        velocidad1.append(i['Velocidad1'])
        velocidad2.append(i['Velocidad2'])
        aceleracion.append(i['Aceleracion'])

    data = pd.DataFrame({
        'Distancia': distancia,
        'Distancia1': distancia1,
        'Distancia2': distancia2,
        'Tiempo': tiempo,
        'Tiempo1': tiempo1,
        'Tiempo2': tiempo2,
        'Velocidad1': velocidad1,
        'Velocidad2': velocidad2,
        'Aceleracion': aceleracion,

    })

    outfile = r'C:\Users\CESAR GARCIA\Desktop\Practica.xlsx'
    writer = pd.ExcelWriter(outfile, engine="xlsxwriter", )
    data.to_excel(writer, sheet_name="Hola", index=None)
    writer.save()
    mensaje = "Se desargo Correctamente"

    return render(request, 'signIn.html',{"messg":mensaje})

def definirGrafica(request):
    print("----------------------------------------------------------------------------------------------------")
    arregloAux = request.GET.get('datos')
    grafica = request.GET.get('grafica')

    print("ArregloAux: " + str(arregloAux))
    print("Grafica: " + str(grafica))

    aux = eval(arregloAux)
    distancia2 = []
    tiempo2 = []
    velocidad2 = []
    aceleracion = []

    for i in aux:
        distancia2.append(i['Distancia2'])
        tiempo2.append(i['Tiempo2'])
        velocidad2.append(i['Velocidad2'])
        aceleracion.append(i['Aceleracion'])

    print("Distancia: " + str(distancia2))

    print("Aceleracion: " + str(aceleracion))

    print("Tiempo: " + str(tiempo2))

    if grafica=="XvsT":
        print("Entra Grafica XvsT")
        return render(request, 'Grafico.html',{"grafica":grafica,"datos":distancia2,"arregloTiempos":tiempo2})
    elif grafica=="VvsT":
        print("Entra Grafica VvsT")
        return render(request, 'Grafico.html',{"grafica": grafica,"arregloTiempos": tiempo2,"datos": velocidad2})
    elif grafica=="AvsT":
        print("Entra Grafica AvsT")
        return render(request, 'Grafico.html',{"grafica": grafica,"arregloTiempos": tiempo2,"datos": aceleracion})


def desarrolloGraficos(request):
    grafica = request.GET.get('grafica')


    datos = request.GET.get('datos')
    datos = datos[1:len(datos) - 1]
    datos = datos.split(",")

    arregloTiempos = request.GET.get('arregloTiempos')
    arregloTiempos = arregloTiempos[1:len(arregloTiempos) - 1]
    arregloTiempos = arregloTiempos.split(",")

    for i in range(0,len(datos)):
        if float(datos[i]):
            datos[i]=float(datos[i])

    for i in range(0, len(arregloTiempos)):
        if float(arregloTiempos[i]):
            arregloTiempos[i] = float(arregloTiempos[i])

    ejeYGrafica = datos
    ejeXGrafica = arregloTiempos

    f = plt.figure()

    ejeXGrafica = [1,2,3,4,5,6,7,8,9]
    ejeYGrafica = [1,2,3,4,5,6,9,7,8]

    axes = f.add_axes([0.15, 0.15, 0.75, 0.75])
    axes.plot(ejeXGrafica,ejeYGrafica,lw=5, c='y', marker='o', ms=10, mfc='red') # lw: ancho de la linea; c: color de la linea; marker: detalle punto; ms: tamaño (grosor) del detalle; mfc: color del detalle
    axes.set_xlabel("t (seg)")
    axes.set_ylabel("x (m)")

    if grafica=="XvsT":
        axes.set_ylabel("x (m)")
    elif grafica == "VvsT":
        axes.set_ylabel("v (m/seg)")
    elif grafica == "AvsT":
        axes.set_ylabel("a (m/seg^2")


    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    f.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response

