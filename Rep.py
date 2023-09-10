from Clases import *
from Fhandler import *
import os

def com_rep(params,lista_particiones):
    name = None
    path = None
    identificador = None
    ruta = None

    for x in params:
        param = [w.strip() for w in x.split("=")]
        
        if len(param) != 2:
            print("--Error en el parametro '"+param[0]+"', parametro incompleto")
            print()
            return sesion_activa

        if param[0].lower() == "name":
            if param[1][0] == '"':
                name = param[1][1:-1]
            else:
                name = param[1]

        if param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

        if param[0].lower() == "id":
            if param[1][0] == '"':
                identificador = param[1][1:-1]
            else:
                identificador = param[1]

        if param[0].lower() == "ruta":
            if param[1][0] == '"':
                ruta = param[1][1:-1]
            else:
                ruta = param[1]

    if not name:
        print("--No se encontro el parametro obligatorio 'name'")
        print()
        return

    if not path:
        print("--No se encontro el parametro obligatorio 'path'")
        print()
        return

    if not identificador:
        print("--No se encontro el parametro obligatorio 'id'")
        print()
        return

    res = [x for x in lista_particiones if x["identificador"] == identificador]
    if len(res) == 0:
        print("--No existe el id '"+identificador+"' entre las particiones cargadas")
        print()
        return

    datos = res[0]["datos"]


    if name == "tree":
        estado = integridadSB(datos)
        if not estado:
            print("--La particion aun no ha sido formateada")
            print()
            return
        s = repTree(datos)
        src = graphviz.Source(s)
        src.render(path, view=False)
        os.remove(path)
    elif name == "bm_block":
        estado = integridadSB(datos)
        if not estado:
            print("--La particion aun no ha sido formateada")
            print()
            return
        with open(path,'w') as d:
            d.write(repBitmap(datos,"b"))
            d.close()
    elif name == "bm_inode":
        estado = integridadSB(datos)
        if not estado:
            print("--La particion aun no ha sido formateada")
            print()
            return
        with open(path,'w') as d:
            d.write(repBitmap(datos,"i"))
            d.close()
    elif name == "inode":
        estado = integridadSB(datos)
        if not estado:
            print("--La particion aun no ha sido formateada")
            print()
            return
        s = repInodo(datos)
        src = graphviz.Source(s)
        src.render(path, view=False)
        os.remove(path)
    elif name == "block":
        estado = integridadSB(datos)
        if not estado:
            print("--La particion aun no ha sido formateada")
            print()
            return
        s = repBlock(datos)
        src = graphviz.Source(s)
        src.render(path, view=False)
        os.remove(path)
    elif name == "sb":
        estado, s = repSB(datos)
        if not estado:
            print("--La particion aun no ha sido formateada")
            print()
            return 
        src = graphviz.Source(s)
        src.render(path, view=False)
        os.remove(path)
    elif name == "file":
        estado = integridadSB(datos)
        if not estado:
            print("--La particion aun no ha sido formateada")
            print()
            return
        if ruta == None:
            print("--No se encontro el parametro obligatorio 'ruta'")
            print()
            return
        s, datos = traer_archivo(ruta,datos)
        with open(path,'w') as d:
            d.write(s)
            d.close()
    elif name == "ls":
        estado = integridadSB(datos)
        if not estado:
            print("--La particion aun no ha sido formateada")
            print()
            return
        if ruta == None:
            print("--No se encontro el parametro obligatorio 'ruta'")
            print()
            return
        s, datos = repLs(ruta,datos)
        src = graphviz.Source(s)
        src.render(path, view=False)
        os.remove(path)

    elif name == "journaling":
        estado, s = repJournaling(datos)
        if not estado:
            print("--El comando debe ser aplicado sobre una particion con EXT3")
            print()
            return
        
        src = graphviz.Source(s)
        src.render(path, view=False)
        os.remove(path)
    elif name == "disk":
        p = res[0]["path"]
        mbr = MBR()
        with open(p,"rb") as f:
            mbr.deserializar(f.read())
            f.close()
        src = graphviz.Source(mbr.showdisk(p))
        src.render(path, view=False)
        os.remove(path)

    elif name == "mbr":
        p = res[0]["path"]
        mbr = MBR()
        with open(p,"rb") as f:
            mbr.deserializar(f.read())
            f.close()

        src = graphviz.Source(mbr.imprimir(p))
        src.render(path, view=False)
        os.remove(path)
    else:
        print("--No se reconoce el nombre del reporte")

    datos = res[0]["datos"]
    print("Reporte creado con exito")
    print()
