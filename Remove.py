from Clases import *
from Fhandler import *
import os

def com_remove(params, lista_particiones, sesion_activa):
    path = None

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
                
                
    if not path:
        print("--No se encontro el parametro obligatorio 'path'")
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
    conjunto = path.rsplit("/",1)
    ruta = conjunto[0]
    archivo = conjunto[1]

    estado, permiso, datos = revisar_permisos(path,datos,sesion_activa)
    res[0]["datos"] = datos
    if not estado:
        print("--La ruta no existe")
        print()
        return
    
    if permiso[1] != "1":
        print("--El usuario no tiene permiso de escritura sobre el archivo "+ruta)
        print()
        return

    
    existe, datos = eliminar_ruta(path,datos,sesion_activa)
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("remove",params,res[0]["datos"])
    print("--Se ha eliminado el archivo '"+path+"' de manera exitosa")
    print()
    return
