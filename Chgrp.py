from Clases import *
from Fhandler import *
import os

def com_chgrp(params, lista_particiones, sesion_activa):
    grp = None
    user = None

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

        if param[0].lower() == "user":
            if param[1][0] == '"':
                user = param[1][1:-1]
            else:
                user = param[1]

        elif param[0].lower() == "grp":
            if param[1][0] == '"':
                grp = param[1][1:-1]
            else:
                grp = param[1]

    if user == None:
        print("--No se encontro el parametro obligatorio 'user'")
        print()
        return

    if grp == None:
        print("--No se encontro el parametro obligatorio 'grp'")
        print()
        return 

    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        print("--No existe el id '"+identificador+"' entre las particiones cargadas")
        print()
        return sesion_activa

    datos = res[0]["datos"]
    estado = integridadSB(datos)
    if not estado:
        print("--La particion aun no ha sido formateada")
        print()
        return
    users_creados, datos = traer_archivo("/users.txt", datos)
    lineas = users_creados.split("\n")
    usuarios = [x.split(",") for x in lineas if len(x.split(",")) == 5]
    grupos = [x.split(",") for x in lineas if len(x.split(",")) == 3]

    try:
        us = [x for x in usuarios if x[3] == user][0]
    except:
        print("--No existe el usuario con el nombre '"+user+"' en la particion")
        print()
        return 

    if us[0] == "0":
        print("--El usuario con el nombre '"+user+"' ha sido borrado")
        print()
        return

    try:
        grupo = [x for x in grupos if x[2] == grp][0]
    except:
        print("--No existe el grupo con el nombre '"+grp+"' en la particion")
        print()
        return 

    if grupo[0] == "0":
        print("--El grupo con el nombre '"+grp+"' ha sido borrado")
        print()
        return

    texto = ""
    
    for linea in usuarios:
        if linea == us:
            continue
        for palabra in linea:
            texto+=palabra+","
        texto = texto[:-1]+"\n"

    texto+= us[0]+",U,"+grp+","+user+","+us[4]+"\n"

    for linea in grupos:
        for palabra in linea:
            texto+=palabra+","
        texto = texto[:-1]+"\n"

    datos = escribir_archivo("/users.txt", datos, texto)
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("chgrp",params,res[0]["datos"])
    print("Se ha cambiado el grupo del usuario con exito")
    print()
    return 
