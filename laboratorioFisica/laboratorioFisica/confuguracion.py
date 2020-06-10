from django.shortcuts import render
import pyrebase                     # Se importa la libreria de pyrebase para el uso de firebase
from django.contrib import auth

# Se crea la conexion a firebase
config = {
    'apiKey': "AIzaSyBnLmnZzCSe4ycoZHtjTpET-emfCDjZsWc",
    'authDomain': "base-datos-fisica.firebaseapp.com",
    'databaseURL': "https://base-datos-fisica.firebaseio.com",
    'projectId': "base-datos-fisica",
    'storageBucket': "base-datos-fisica.appspot.com",
    'messagingSenderId': "367086774500",
    'appId': "1:367086774500:web:875ac8ad80e821b8d2e4f1",
}

firebase = pyrebase.initialize_app(config)          # Se inicializa el servicio de storage de firebase
authe = firebase.auth()                             # Se inicia el servicio de autenticacion de firebase
database = firebase.database()                      # Se crea la base de datos en firebase