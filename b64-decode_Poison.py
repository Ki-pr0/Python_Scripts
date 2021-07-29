#!/usr/bin/python3
# Script para decodear unas 13 veces una cadena en base64 en la maquina Poison de HTB

from base64 import b64decode

pass_en = "CADENA EN BASE64 A DECODEAR"
# bucle para decodear X veces
for i in range(13):
  pass_en = b64decode(pass_en)
  
print(pass_en)
