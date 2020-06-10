"""laboratorioFisica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .Controladores import ControladorSesion, ControladorPracticas, ControladorGrupos, ControladorPracticasLaboratorio

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',ControladorSesion.signIn),
    #url(r'^$',ControladorSesion.signIn),
    url(r'^InicioSesion/',ControladorSesion.postsign, name="InicioSesio"),
    url(r'^logout/', ControladorSesion.logout, name="log"),
    url(r'^controlPracticas/', ControladorPracticas.menuControlPracticas, name="controlPracticas"),
    url(r'^agregarGrupo/', ControladorGrupos.formularioAgregarGrupo, name="agregarGrupo"),
    url(r'^verGrupos/', ControladorGrupos.listadoGrupos, name="verGrupos"),
    url(r'^registroGrupo/', ControladorGrupos.registroGrupo, name="registroGrupo"),
    url(r'^actualizarGrupo/', ControladorGrupos.actualizar, name="actualizarGrupo"),
    url(r'^eliminarGrupo/', ControladorGrupos.eliminar, name="eliminarGrupo"),
    url(r'^formularioActualizarGrupo/', ControladorGrupos.actualizarGrupo, name="formularioActualizarGrupo"),
    url(r'^practicas/', ControladorPracticasLaboratorio.menuPracticas, name="practicas"),
    url(r'^agregarPractica/', ControladorPracticasLaboratorio.agregarPractica, name="agregarPractica"),
    url(r'^registroPractica/', ControladorPracticasLaboratorio.asignacionPractica, name="registroPractica"),
    url(r'^registroUsuario/', ControladorSesion.registroFormulario, name="registroUsuario"),
    url(r'^registroEstudiante/', ControladorSesion.registroUsuario, name="registroEstudiante"),
    url(r'^verPracticas/', ControladorPracticasLaboratorio.verPracticas, name="verPracticas"),
    url(r'^actualizarPracticaFormulario/', ControladorPracticasLaboratorio.actualizarFormulario, name="actualizarPracticaFormulario"),
    url(r'^actualizarPractica/', ControladorPracticasLaboratorio.actualizar, name="actualizarPractica"),
    url(r'^eliminarPractica/', ControladorPracticasLaboratorio.eliminar, name="eliminarPractica"),
    url(r'^realizarPractica/', ControladorPracticasLaboratorio.realizar, name="eliminarPractica"),
    url(r'^agregarExperimento/', ControladorPracticasLaboratorio.agregarExperimento, name="agregarExperimento"),
    url(r'^terminarPractica/', ControladorPracticasLaboratorio.terminarPractica, name="terminarPractica"),
    url(r'^verEstudiantes/', ControladorGrupos.visualizarEstudiantesGrupo, name="verEstudiantes"),
    url(r'^resultadosEstudiante/', ControladorGrupos.resultadosEstudiante, name="resultadosEstudiante"),








    url(r'^agregarPractica/', ControladorPracticas.agregarPractica, name='agregarPractica'),
    url(r'^formularioAgregarPractica/', ControladorPracticas.agregarPracticaFormulario, name='formularioAgregarPractica'),
    url(r'^agregarExperimento/', ControladorPracticas.agregarExperimento, name='agregarExperimento'),
    url(r'^formularioAgregarExperimento/', ControladorPracticas.agregarExperimentoForumulario, name='formularioAgregarExperimento'),
    url(r'^seleccionPractica/', ControladorPracticas.seleccionPracticaRealizar, name='seleccionPractica'),
    url(r'^consultar/', ControladorPracticas.experimentosPractica, name='consultar'),
    url(r'^downloadExperimentos/', ControladorPracticas.descargar, name='downloadExperimentos'),
    url(r'^verGraficas/', ControladorPracticas.verGraficasMenu, name='verGraficas'),
    url(r'^graficosRealizados/', ControladorPracticas.desarrolloGraficos, name='graficosRealizados'),
    url(r'^verGraficaEspecifica/', ControladorPracticas.definirGrafica, name='verGraficaEspecifica'),
]
