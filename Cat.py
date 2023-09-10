from Clases import *
from Fhandler import *
import os

def com_cat(params, lista_particiones, sesion_activa):
    file = []

    if not sesion_activa:
        print("--Este comando requiere una sesion activa")
        print()
        return

    for x in params:
        param = [w.strip() for w in x.split("=")]
        
        if len(param) != 2:
            print("--Error en el parametro '"+param[0]+"', parametro incompleto")
            print()
            return 

        if param[0].lower().startswith("file"):
            if param[1][0] == '"':
                file.append(param[1][1:-1])
            else:
                file.append(param[1])

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
    s = ""
    for f in file:
        s+=f+"\n"
        existe, permiso, datos = revisar_permisos(f, datos,sesion_activa)
        if not existe:
            s+="--No existe el archivo\n"
            s+="\n"
            continue
        if permiso[0] == "0":
            s+="--El usuario no tiene permiso de lectura\n"
            s+="\n"
            continue
        
        x, datos = traer_archivo(f,datos)
        s+=x
        s+="\n\n"

    res[0]["datos"] = datos
    print(s)
