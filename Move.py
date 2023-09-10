from Clases import *
from Fhandler import *
import os

def com_move(params, lista_particiones, sesion_activa):
    path = None
    destino = None

    if not sesion_activa:
        print("--Este comando requiere una sesion activa")
        print()
        return
    
    for x in params:
        param = [w.strip() for w in x.split("=")]

        if param[0].lower() == "r":
            r = True
        elif len(param) != 2:
            print("--Error en el parametro '"+param[0]+"', parametro incompleto")
            print()
            return sesion_activa

        if param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

        if param[0].lower() == "destino":
            if param[1][0] == '"':
                destino = param[1][1:-1]
            else:
                destino = param[1]
                
    if not path:
        print("--No se encontro el parametro obligatorio 'path'")
        print()
        return

    if not destino:
        print("--No se encontro el parametro obligatorio 'destino'")
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

    datos = mover(path,destino,datos,sesion_activa)
    
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("move",params,res[0]["datos"])
    return
