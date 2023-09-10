from Mkdisk import *
from Rep import *
from Fdisk import *
from Rmdisk import *
from Mount import *
from Unmount import *
from Mkfs import *
from Login import *
from Logout import *
from Rmgrp import *
from Mkgrp import *
from Mkusr import *
from Rmusr import *
from Mkfile import *
from Cat import *
from Remove import *
from Edit import *
from Rename import *
from Mkdir import *
from Copy import *
from Move import *
from Find import *
from Chown import *
from Chgrp import *
from Chmod import *
from Recovery import *
from Loss import *

particiones_montadas = []
sesion_activa = None
ultimo_disco = ''

def interpretacion_de_comando(comando):
    comando = comando.split("#",1)[0].strip()
    if len(comando) == 0:
        return
    global ultimo_disco, sesion_activa, particiones_montadas
    params = [param.strip() for param in comando.split("-")]

    if params[0].lower() == 'mkdisk':
        ultimo_disco = com_mkdisk(params[1:])
    elif params[0].lower() == 'rmdisk':
        ultimo_disco = com_rmdisk(params[1:])
    elif params[0].lower() == 'fdisk':
        ultimo_disco = com_fdisk(params[1:])
    elif params[0].lower() == 'mount':
        com_mount(params[1:], particiones_montadas)
    elif params[0].lower() == 'lpm':
        print("Lista de particiones montadas")
        for p in particiones_montadas:
            print("--"+p["identificador"])
        print()
    elif params[0].lower() == 'unmount':
        com_unmount(params[1:], particiones_montadas)
    elif params[0].lower() == 'mkfs':
        com_mkfs(params[1:], particiones_montadas)
    elif params[0].lower() == 'login':
        sesion_activa = com_login(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'logout':
        sesion_activa = com_logout(particiones_montadas, sesion_activa)
    elif params[0].lower() == 'mkgrp':
        com_mkgrp(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'rmgrp':
        com_rmgrp(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'mkusr':
        com_mkusr(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'rmusr':
        com_rmusr(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'mkfile':
        com_mkfile(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'cat':
        com_cat(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'remove':
        com_remove(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'edit':
        com_edit(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'rename':
        com_rename(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'mkdir':
        com_mkdir(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'copy':
        com_copy(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'move':
        com_move(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'find':
        com_find(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'chown':
        com_chown(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'chgrp':
        com_chgrp(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'chmod':
        com_chmod(params[1:], particiones_montadas, sesion_activa)
    elif params[0].lower() == 'pause':
        input(">> Pulsa enter para continuar")
    elif params[0].lower() == 'recovery':
        s = "logout\n"+com_recovery(params[1:], particiones_montadas)
        ejecutar_comandos(s)
    elif params[0].lower() == 'loss':
        com_loss(params[1:], particiones_montadas)
    elif params[0].lower() == 'rep':
        com_rep(params[1:], particiones_montadas)
    elif params[0].lower() == 'execute':
        com_execute(params[1:])
    else:
        print("--Comando '"+params[0]+"' no reconocido")
        print()


def ejecutar_comandos(s):
    lineas = s.split("\n")
    for l in lineas:
        print("----------------------------------")
        interpretacion_de_comando(l)

def com_execute(params):
    path = None

    for x in params:
        param = [w.strip() for w in x.split("=")]
        if param[0].lower() != "path":
            print("--Parametro '"+param[0]+"' no reconocido para el comando 'execute'")
            print()
            return
        
        if len(param)<2:
            print("--El parametro 'path' necesita una direccion")
            print()
            return

        if param[1][0] == '"':
            path = param[1][1:-1]
        else:
            path = param[1]

    if path == None:
        print("--No se encontro el parametro obligatorio 'path'")
        print()
        return

    with open(path,'r') as f:
            lineas = f.readlines()
            for l in lineas:
                print("----------------------------------")
                print(l)
                interpretacion_de_comando(l)
            f.close()
    try:
        pass
    except:
        print("--Direccion invalida")
        print()

interpretacion_de_comando("execute -path=a_prueba/Entrada2.txt")
while True:
    comando = input(">>")

    interpretacion_de_comando(comando)
