from Clases import *
from Fhandler import *
import os

def com_chmod(params, lista_particiones, sesion_activa):
    path = None
    ugo = None
    r = False

    if not sesion_activa:
        print("--Este comando requiere una sesion activa")
        print()
        return
    
    if sesion_activa["user"] != "root":
        print("--Solo el usuario root puede ejecutar este comando")
        print()
        return

    for x in params:
        param = [w.strip() for w in x.split("=")]

        if param[0].lower() == "r":
            r = True
            continue
        
        if len(param) != 2:
            print("--Error en el parametro '"+param[0]+"', parametro incompleto")
            print()
            return 

        if param[0].lower() == "ugo":
            if param[1][0] == '"':
                ugo = param[1][1:-1]
            else:
                ugo = param[1]

        elif param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

    if ugo == None:
        print("--No se encontro el parametro obligatorio 'ugo'")
        print()
        return

    if path == None:
        print("--No se encontro el parametro obligatorio 'path'")
        print()
        return 

    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        print("--No existe el id '"+identificador+"' entre las particiones cargadas")
        print()
        return sesion_activa

    perms = []
    try:
        for i in ugo:
            perms.append(int(i))
    except:
        print("--El parametro ugo debe ser numerico")
        print()
        return

    for i in perms:
        if i<0 or i>7:
            print("--Los permisos deben ser un numero del 0 al 7")
            print()
            return

    datos = res[0]["datos"]
    estado = integridadSB(datos)
    if not estado:
        print("--La particion aun no ha sido formateada")
        print()
        return
    
    if r:
        datos = cambiar_permiso_r(path, datos, sesion_activa, perms[0], perms[1], perms[2])
    else:
        datos = cambiar_permiso(path, datos, sesion_activa, perms[0], perms[1], perms[2])
    
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("chmod",params,res[0]["datos"])
    print("Se han actualizado los permisos de la ruta")
    print()
    return 
