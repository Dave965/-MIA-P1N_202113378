from Clases import *
from Fhandler import *
import os

def com_mkdir(params, lista_particiones, sesion_activa):
    path = None
    r = False


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
    if estado:
        print("--Ya existe una carpeta con ese nombre")
        print()
        return 
    
    if r:
        estado, datos = crear_ruta(path,datos,sesion_activa)
        if not estado:
            res[0]["datos"] = datos 
            return
    else:
        estado, permiso, datos = revisar_permisos(ruta,datos,sesion_activa)
        res[0]["datos"] = datos 
        if not estado:
            print("--La ruta no existe")
            print()
            return
        
        if permiso[1] != "1":
            print("--El usuario no tiene permiso de Escritura en la carpeta "+ruta)
            print()
            return
            
        estado, datos = crear_carpeta(path,datos,sesion_activa)
        res[0]["datos"] = datos
        
        if not estado:
            print("--No se pudo crear la carpeta")
            print()
            return

    
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("mkdir",params,res[0]["datos"])
    print("Se ha creado la carpeta '"+path+"' de manera exitosa")
    print()
    return
