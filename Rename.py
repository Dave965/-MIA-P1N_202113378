from Clases import *
from Fhandler import *
import os

def com_rename(params, lista_particiones, sesion_activa):
    path = None
    name = None
    
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

        if param[0].lower() == "name":
            if param[1][0] == '"':
                name = param[1][1:-1]
            else:
                name = param[1]
                
    if not path:
        print("--No se encontro el parametro obligatorio 'path'")
        print()
        return

    if not name:
        print("--No se encontro el parametro obligatorio 'name'")
        print()
        return

    if len(name) > 12:
        print("--El nombre puede tener como maximo 12 caracteres")
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

    estado, permiso, datos = revisar_permisos(ruta+"/"+name,datos,sesion_activa)
    res[0]["datos"] = datos 
    if estado:
        print("--Ya existe una ruta con el nuevo nombre")
        print()
        return

    estado, permiso, datos = revisar_permisos(path,datos,sesion_activa)
    res[0]["datos"] = datos
    
    if permiso[1] != "1":
        print("--El usuario no tiene permiso de Escritura en la ruta "+path)
        print()
        return

    estado, datos = cambiar_nombre(path, datos, name, sesion_activa)
    res[0]["datos"] = datos
    
    res[0]["datos"] = guardar_journaling("rename",params,res[0]["datos"])
    print("--Se ha Cambiado el nombre de la ruta '"+path+"' de manera exitosa")
    print()
    return
