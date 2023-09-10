from Clases import *
from Fhandler import *
import os

def com_mkfile(params, lista_particiones, sesion_activa):
    path = None
    r = False
    size = 0
    cont = None

    cadena = "0123456789"
    texto_archivo = ""

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

        if param[0].lower() == "size":
            size = int(param[1])

        if param[0].lower() == "cont":
            if param[1][0] == '"':
                cont = param[1][1:-1]
            else:
                cont = param[1]
                
    if not path:
        print("--No se encontro el parametro obligatorio 'path'")
        print()
        return

    if size <0:
        print("--Size debe ser un numero positivo")
        print()
        return

    texto_archivo = cadena*int(size/10)+cadena[:(size%10)]
        
    if cont:
        if not os.path.exists(cont):
            print("--No existe un archivo en la ruta '"+cont+"'")
            print()
            return

        with open(cont,"r") as f:
            texto_archivo = f.read()
            f.close()    

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
        print("--Ya existe un archivo con ese nombre")
        print()
        return 
    
    if r:
        estado, datos = crear_ruta(ruta,datos,sesion_activa)
        if not estado:
            res[0]["datos"] = datos 
            return

        estado, datos = crear_archivo(path,datos,sesion_activa)
        if not estado:
            res[0]["datos"] = datos 
            print("--No se pudo crear el archivo")
            print()
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
            
        estado, datos = crear_archivo(path,datos,sesion_activa)
        res[0]["datos"] = datos 
        if not estado:
            print("--No se pudo crear el archivo")
            print()
            return

    datos = escribir_archivo(path, datos, texto_archivo)
    res[0]["datos"] = datos
    res[0]["datos"] = guardar_journaling("mkfile",params,res[0]["datos"])
    print("Se ha creado el archivo '"+path+"' de manera exitosa")
    print()
    return
