from Clases import *
import os
from datetime import datetime

def com_mkdisk(params):
    tam = None
    unidad = 1024*1024
    path = None
    fit = 'F'

    for x in params:
        param = [w.strip() for w in x.split("=")]
        if len(param) != 2:
            print("--Error en el parametro '"+param[0]+"', parametro incompleto")
            print()
            return

        if param[0].lower() == "fit":
            if param[1].lower() == "bf":
                fit = "B"
            elif param[1].lower() == "wf":
                fit = "W"
            elif param[1].lower() == "ff":
                pass
            else:
                print("--Error en el parametro 'fit', ajuste '"+param[1]+"' no reconocido")
                print()
                return
            
        if param[0].lower() == "size":
            try:
                tam = int(param[1])
            except:
                print("--Error en el parametro 'size', se esperaba un numero entero positivo")
                print()
                return
        
        elif param[0].lower() == "unit":
            if param[1].lower() == "k":
                unidad = 1024
            elif param[1].lower() == "m":
                pass
            else:
                print("--Error en el parametro 'unit', unidad '"+param[1]+"' no reconocida")
                print()
                return

        elif param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

    if tam == None:
        print("--No se encontro el parametro obligatorio 'size'")
        print()
        return

    if tam <=0:
        print("--el parametro 'size' debe ser mayor que 0")
        print()
        return

    if path == None:
        print("--No se encontro el parametro obligatorio 'path'")
        print()
        return

    ultimo_disco = path
    
    if os.path.exists(path):
        print("--Ya existe un disco creado en '"+path+"'")
        print()
        return

    directorio = path.rsplit('/',1)[0]

    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    tamano_bytes = tam * unidad
    fecha_creacion = datetime.now()
    n_mbr = MBR()

    n_mbr.setAll(tamano_bytes, fecha_creacion.strftime("%d/%m/%Y %H:%M:%S"), int(fecha_creacion.timestamp()),fit)
    data_serializada = n_mbr.serializar()
    
    with open(path,'wb') as d:
        d.write(data_serializada)
        d.write(b'\0' * (tamano_bytes-len(data_serializada)))
        d.close()

    print("--Disco creado con exito")
    print()

    return ultimo_disco
