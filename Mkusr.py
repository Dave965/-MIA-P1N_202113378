from Clases import *
from Fhandler import *
import os

def com_mkusr(params, lista_particiones, sesion_activa):
    user = None
    password = None
    grp = None

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
        
        if len(param) != 2:
            print("--Error en el parametro '"+param[0]+"', parametro incompleto")
            print()
            return sesion_activa

        if param[0].lower() == "user":
            if param[1][0] == '"':
                user = param[1][1:-1]
            else:
                user = param[1]

        if param[0].lower() == "pass":
            if param[1][0] == '"':
                password = param[1][1:-1]
            else:
                password = param[1]

        if param[0].lower() == "grp":
            if param[1][0] == '"':
                grp = param[1][1:-1]
            else:
                grp = param[1]


    if not user:
        print("--No se encontro el parametro obligatorio 'user'")
        print()
        return

    if not password:
        print("--No se encontro el parametro obligatorio 'pass'")
        print()
        return

    if not grp:
        print("--No se encontro el parametro obligatorio 'grp'")
        print()
        return

    if len(user) > 10:
        print("--El nombre de usuario debe tener como maximo 10 caracteres")
        print()
        return

    if len(password) > 10:
        print("--El password del usuario debe tener como maximo 10 caracteres")
        print()
        return
    
    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        print("--No existe el id '"+sesion_activa["particion"]+"' entre las particiones cargadas")
        print()
        return

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
    us = [x for x in usuarios if x[3] == user]
    grupo = [x for x in grupos if x[2] == grp]

    if len(us) > 0:
        print("--Ya existe un usuario con nombre '"+user+"' entre los usuarios creados")
        print()
        return

    if len(grupo) < 1:
        print("--No existe un grupo con nombre '"+grp+"' entre los grupos creados")
        print()
        return

    if grupo[0] == "0":
        print("--El grupo '"+grp+"' fue eliminado.")
        print()
        return

    texto = ""
    
    for linea in usuarios:
        for palabra in linea:
            texto+=palabra+","
        texto = texto[:-1]+"\n"

    texto+= str(len(usuarios)+1)+",U,"+grp+","+user+","+password+"\n"

    for linea in grupos:
        for palabra in linea:
            texto+=palabra+","
        texto = texto[:-1]+"\n"

    
    
    datos = escribir_archivo("/users.txt", datos, texto)
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("mkusr",params,res[0]["datos"])
    
    print("Usuario '"+user+"' creado exitosamente")
    print()
    return
