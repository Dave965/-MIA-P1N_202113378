from Clases import *
from Fhandler import *
import os

def com_login(params, lista_particiones, sesion_activa):
    user = None
    password = None
    identificador = None

    if sesion_activa:
        print("--Ya se ha iniciado sesion")
        print()
        return sesion_activa

    for x in params:
        param = [w.strip() for w in x.split("=")]
        
        if len(param) != 2:
            print("--Error en el parametro '"+param[0]+"', parametro incompleto")
            print()
            return sesion_activa

        if param[0].lower() == "user":
            if param[1][0] == '"':
                user = param[1][1:-1]
            else:
                user = param[1]

        elif param[0].lower() == "pass":
            if param[1][0] == '"':
                password = param[1][1:-1]
            else:
                password = param[1]

        
        elif param[0].lower() == "id":
            if param[1][0] == '"':
                identificador = param[1][1:-1]
            else:
                identificador = param[1]

    if user == None:
        print("--No se encontro el parametro obligatorio 'user'")
        print()
        return sesion_activa

    if password == None:
        print("--No se encontro el parametro obligatorio 'pass'")
        print()
        return sesion_activa

    if identificador == None:
        print("--No se encontro el parametro obligatorio 'id'")
        print()
        return sesion_activa

    res = [x for x in lista_particiones if x["identificador"] == identificador]
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
        usuarios = [x for x in usuarios if x[3] == user][0]
    except:
        print("--No existe el usuario con el nombre '"+user+"' en la particion")
        print()
        return sesion_activa

    if usuarios[0] == "0":
        print("--El usuario con el nombre '"+user+"' ha sido borrado")
        print()
        return sesion_activa

    if usuarios[4] != password:
        print("--password incorrecto")
        print()
        return sesion_activa

    grupo = [x for x in grupos if x[2] == usuarios[2]][0]

    uid = int(usuarios[0])
    gid = int(grupo[0])

    sesion_activa = {"particion":identificador, "user":user, "grupo": usuarios[2], "uid":uid, "gid":gid}
    res[0]["datos"] = guardar_journaling("login",params,res[0]["datos"])
    print("Sesion del usuario '"+user+"' iniciada con exito en el disco '"+identificador+"'")
    print()
    return sesion_activa
