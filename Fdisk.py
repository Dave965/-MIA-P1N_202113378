from Clases import *
import os

def com_fdisk(params):
    size = None
    unit = 1024
    path = None
    name = None
    delete = False
    add = None
    fit = "W"
    _type = "P"
    skip = False

    for x in params:
        param = [w.strip() for w in x.split("=")]
        if skip:
            skip = False
            continue
        
        if param[0].lower() == "delete":
            delete = True
        
        if len(param) != 2:
            print("--Error en el parametro '"+param[0]+"', parametro incompleto")
            print()
            return

        if param[0].lower() == "size":
            try:
                size = int(param[1])
            except:
                print("--Error en el parametro 'size', se esperaba un numero entero positivo")
                print()
                return
        
        elif param[0].lower() == "unit":
            if param[1].lower() == "k":
                pass
            elif param[1].lower() == "m":
                unit = 1024*1024
            elif param[1].lower() == "b":
                unit = 1
            else:
                print("--Error en el parametro 'unit', unidad '"+param[1]+"' no reconocida")
                print()
                return

        elif param[0].lower() == "path":
            if param[1][0] == '"':
                path = param[1][1:-1]
            else:
                path = param[1]

        elif param[0].lower() == "name":
            if param[1][0] == '"':
                name = param[1][1:-1]
            else:
                name = param[1]
                
        elif param[0].lower() == "type":
            if param[1][0] == '"':
                _type = param[1][1:-1]
            else:
                _type = param[1]

        elif param[0].lower() == "add":
            try:
                add = int(param[1])
            except:
                try:
                    sig = params.index(x)+1
                    par = [w.strip() for w in params[sig].split("=")]
                    add = -int(par[0])
                    skip = True
                except:
                    print("--Add debe ser un numero entero")
                    print()
                    return
                

    if path == None:
        print("--No se encontro el parametro obligatorio 'path'")
        print()
        return

    if name == None:
        print("--No se encontro el parametro obligatorio 'name'")
        print()
        return

    if not os.path.exists(path):
        print("--No existe un disco en '"+path+"'")
        print()
        return
    
    mbr = MBR()
    ultimo_disco = path
    
    with open(path,"rb") as f:
        mbr.deserializar(f.read())
        f.close()

    
    if delete:
        for i in range(len(mbr.mbr_partition)):
            x = mbr.mbr_partition[i]
            if x.part_name.decode().strip("\x00") == name:
                mbr.mbr_partition[i] = Partition()
                contenido = b"\x00"*x.part_s

                with open(path,'r+b') as d:
                    pre = d.read()[:x.part_start]
                    d.seek(0)
                    post = d.read()[x.part_start+x.part_s:]
                    d.seek(0)
                    d.write(pre+contenido+post)
                    d.close()

                data_serializada = mbr.serializar()

                with open(path,'r+b') as d:
                    post = d.read()[len(data_serializada):]
                    d.seek(0)
                    d.write(data_serializada)
                    d.write(post)
                    d.close()

                print("Particion eliminada exitosamente")
                print()
                return

        print("--La particion no existe en el disco")
        print()
        return

    if add:
        add = add*unit
        if add < 0:
            for i in range(len(mbr.mbr_partition)):
                x = mbr.mbr_partition[i]
                if x.part_name.decode().strip("\x00") == name:
                    if x.part_s+add <0:
                        print("--No hay suficiente espacio en la particion")
                        print()
                        return
                    else:
                        x.part_s = x.part_s+add
                        mbr.mbr_partition[i] = x
                        data_serializada = mbr.serializar()

                        with open(path,'r+b') as d:
                            post = d.read()[len(data_serializada):]
                            d.seek(0)
                            d.write(data_serializada)
                            d.write(post)
                            d.close()
                            
                        print("Cambio en el tamano de la particion realizado con exito")
                        print()
                        return
            
            extendida = [x for x in mbr.mbr_partition if x.part_type.decode().lower() == "e"]
            if len(extendida) != 0:
                extendida = extendida[0]
                with open(path,"rb") as f:
                    f.seek(extendida.part_start)
                    contenido = f.read(extendida.part_s)
                    f.close()
                ebr = EBR()
                porcion = contenido 
                aceptados = ["1","0"]
                while True:
                    ebr.deserializar(porcion)
                    if ebr.part_name.decode().strip('\x00') == name:
                        if ebr.part_s+add <0:
                            print("--No hay suficiente espacio en la particion")
                            print()
                            return
                        else:
                            ebr.part_s = ebr.part_s+add
                            data_serializada = ebr.serializar()
                            pre = contenido[:ebr.part_start-sizeEBR]
                            post = contenido[ebr.part_start-sizeEBR+len(data_serializada):]
                            contenido = pre+data_serializada+post

                            with open(path,'r+b') as d:
                                pre = d.read()[:extendida.part_start]
                                d.seek(0)
                                post = d.read()[extendida.part_start+extendida.part_s:]
                                d.seek(0)
                                d.write(pre+contenido+post)
                                d.close()

                            print("Cambio en el tamano de la particion realizado con exito")
                            print()
                            return
                        
                    if ebr.part_status.decode() not in aceptados or ebr.part_next == -1:
                        break
                    porcion = contenido[ebr.part_next:]

                print("--La particion no existe en el disco")
                print()
                return
        else:
            mbr.mbr_partition.sort(key=lambda x: x.part_start)
            for i in range(len(mbr.mbr_partition)):
                x=mbr.mbr_partition[i]
                if x.part_name.decode().strip("\x00") == name:
                    disponible = 0

                    if i < 3:
                        disponible = mbr.mbr_partition[i+1].part_start-(x.part_start+x.part_s)
                    else:
                        disponible = mbr.mbr_tamano-(x.part_start+x.part_s)

                    if disponible >= add:
                        x.part_s = x.part_s+add
                        mbr.mbr_partition[i] = x
                        data_serializada = mbr.serializar()

                        with open(path,'r+b') as d:
                            post = d.read()[len(data_serializada):]
                            d.seek(0)
                            d.write(data_serializada)
                            d.write(post)
                            d.close()
                            
                        print("Cambio en el tamano de la particion realizado con exito")
                        print()
                        return
                    print("--No hay suficiente espacio para expandir la particion")
                    print()
                    return
            
                            
            extendida = [x for x in mbr.mbr_partition if x.part_type.decode().lower() == "e"]
            if len(extendida) != 0:
                extendida = extendida[0]
                with open(path,"rb") as f:
                    f.seek(extendida.part_start)
                    contenido = f.read(extendida.part_s)
                    f.close()
                ebr = EBR()
                mi_ebr = EBR()
                porcion = contenido 
                aceptados = ["1","0"]

                while True:
                    ebr.deserializar(porcion)
                    if ebr.part_name.decode().strip('\x00') == name:
                        mi_ebr.deserializar(porcion)
                        break
                    
                    if ebr.part_status.decode() not in aceptados or ebr.part_next == -1:
                        break
                    porcion = contenido[ebr.part_next:]

                if mi_ebr.part_status.decode() not in aceptados:
                    print("--La particion no existe en el disco")
                    print()
                    return
                
                porcion = contenido
                inicio = 0
                rangos_ocupados = []
                while True:
                    ebr.deserializar(porcion)
                    rangos_ocupados.append((inicio,ebr.part_start+ebr.part_s))
                    inicio = inicio+sizeEBR+ebr.part_s
                    if ebr.part_next == -1:
                        break
                    porcion = contenido[ebr.part_next:]
                rangos_ocupados.sort(key=lambda x: x[0])

                for i in range(len(rangos_ocupados)):
                    size = 0
                    if i<len(rangos_ocupados)-1:
                        size = rangos_ocupados[i+1][0]-rangos_ocupados[i][1]       
                    else:
                        size = extendida.part_s-rangos_ocupados[i][1]

                    if rangos_ocupados[i][1] == mi_ebr.part_start+mi_ebr.part_s:
                        if size >= add:
                            mi_ebr.part_s += add
                            data_serializada = mi_ebr.serializar()
                            pre = contenido[:mi_ebr.part_start-sizeEBR]
                            post = contenido[mi_ebr.part_start-sizeEBR+len(data_serializada):]
                            contenido = pre+data_serializada+post
                            with open(path,'r+b') as d:
                                pre = d.read()[:extendida.part_start]
                                d.seek(0)
                                post = d.read()[extendida.part_start+extendida.part_s:]
                                d.seek(0)
                                d.write(pre+contenido+post)
                                d.close()
                            print("Cambio en el tamano de la particion realizado con exito")
                            print()
                            return
                    
                        print("--No hay suficiente espacio para expandir la particion")
                        print()
                        return        

        print("--La particion no existe en el disco")
        print()
        return

    if size == None:
        print("--No se encontro el parametro obligatorio 'size'")
        print()
        return
    if size < 0:
        print("--el parametro 'size' debe ser un entero mayor o igual que 0")
        print()
        return  

    for x in mbr.mbr_partition:
        if x.part_name == name:
            print("--Ya existe una particion con el nombre '"+name+"'")
            print()
            return ultimo_disco

    if _type.lower() == "l":
        part = [x for x in mbr.mbr_partition if x.part_type.decode().lower() == "e"]
        if len(part) == 0:
            print("--No se puede crear una particion logica sin una extendida")
            print()
            return
        part = part[0]
        with open(path,"rb") as f:
            f.seek(part.part_start)
            contenido = f.read(part.part_s)
            f.close()

        ebr = EBR()
        n_ebr = EBR()
        porcion = contenido 
        aceptados = ["1","0"]
        nombres = []
        while True:
            ebr.deserializar(porcion)
            nombres.append(ebr.part_name.decode().strip("\x00"))  
            if ebr.part_status.decode() not in aceptados or ebr.part_next == -1:
                break
            porcion = contenido[ebr.part_next:]

        if name in nombres:
            print("--Ya existe una particion logica con ese nombre")
            print()
            return

        porcion = contenido
        ebr.deserializar(porcion)
        rangos_ocupados = []
        inicio = 0
        size = size*unit

        indice_inicio = None

        if ebr.part_status.decode() not in aceptados:
            if part.part_s < sizeEBR+size:
                print("--No hay espacio en la particion extendida para la particion logica")
                print()
                return
            indice_inicio = 0
        else:
            while True:
                ebr.deserializar(porcion)
                rangos_ocupados.append((inicio,inicio+sizeEBR+ebr.part_s))
                inicio = inicio+sizeEBR+ebr.part_s
                if ebr.part_next == -1:
                    break
                porcion = contenido[ebr.part_next:]
            

        if indice_inicio == None:
            rangos_ocupados.sort(key=lambda x: x[0])
            longitudes = [] #inicio,tamano
            f = 0
            for i in range(len(rangos_ocupados)-1):
                f = i+1
                longitudes.append((rangos_ocupados[i][1],rangos_ocupados[i+1][0]-rangos_ocupados[i][1]))
            longitudes.append((rangos_ocupados[f][1],part.part_s-rangos_ocupados[f][1]))
                
            if part.part_fit.decode() == 'F':
                for x in longitudes:
                    if x[1] >= size+sizeEBR:
                        indice_inicio = x[0]
                        break
            elif part.part_fit.decode() == 'F':
                longitudes.sort(key=lambda x: x[1]-size)
                for x in longitudes:
                    if x[1] >= size+sizeEBR:
                        indice_inicio = x[0]
                        break
            else:
                longitudes.sort(key=lambda x: x[1]-size, reverse=True)
                for x in longitudes:
                    if x[1] >= size+sizeEBR:
                        indice_inicio = x[0]
                        break

        if indice_inicio == None:
            print("--No hay espacio en la particion extendida para la particion logica")
            print()
            return

        n_ebr.setAll("0", fit, indice_inicio+sizeEBR, size, -1, name)
        data_serializada = n_ebr.serializar()

        pre = contenido[:indice_inicio]
        post = contenido[indice_inicio+len(data_serializada):]
        contenido = pre+data_serializada+post
        
        if indice_inicio != 0:
            ebr.setNext(indice_inicio)
            data_serializada = ebr.serializar()
            pre = contenido[:ebr.part_start-sizeEBR]
            post = contenido[ebr.part_start-sizeEBR+len(data_serializada):]
            contenido = pre+data_serializada+post

        with open(path,'r+b') as d:
            pre = d.read()[:part.part_start]
            d.seek(0)
            post = d.read()[part.part_start+part.part_s:]
            d.seek(0)
            d.write(pre+contenido+post)
            d.close()

        print("Se ha creado la particion "+name+" de manera exitosa")
        print()
        return
        

    size = size*unit
    inicio = len(mbr.serializar())
    mbr.mbr_partition.sort(key=lambda x: x.part_start)

    particion_disponible = 5

    longitudes = []
    
    for i in range(len(mbr.mbr_partition)):
        x=mbr.mbr_partition[i]

        if x.part_start <= 0 and i < particion_disponible:
            particion_disponible = i
            continue
        
        if x.part_start <= 0:
            continue

        longitudes.append((inicio, x.part_start-inicio))
        inicio = x.part_start+x.part_s

    if particion_disponible == 5:
        print("--No se ha podido completar la operacion, tabla de particiones llena")
        print()
        return ultimo_disco

    longitudes.append((inicio,mbr.mbr_tamano-inicio))

    encontrado = False

    if _type.lower() == "e":
        tipos = [x.part_type.decode().lower() for x in mbr.mbr_partition]
        if "e" in tipos:
            print("--No se puede crear mas de una particion extendida")
            print()
            return ultimo_disco
            

    if mbr.dsk_fit.decode() == 'F':
        for x in longitudes:
            if x[1] >= size:
                mbr.mbr_partition[particion_disponible].setAll('0', _type, fit, x[0]+1, size, name)
                encontrado = True
                break
    elif mbr.dsk_fit.decode() == 'B':
        longitudes.sort(key=lambda x: x[1]-size)
        for x in longitudes:
            if x[1] >= size:
                mbr.mbr_partition[particion_disponible].setAll('0', _type, fit, x[0]+1, size, name)
                encontrado = True
                break
    else:
        longitudes.sort(key=lambda x: x[1]-size, reverse=True)
        for x in longitudes:
            if x[1] >= size:
                mbr.mbr_partition[particion_disponible].setAll('0', _type, fit, x[0]+1, size, name)
                encontrado = True
                break

    if not encontrado:
        print("--No se ha podido completar la operacion, el tamano maximo que hay disponible en disco es "+str(sorted(longitudes, key=lambda x: x[1], reverse=True)[0][1])+" byte(s) y se intento alocar "+str(size)+" byte(s)")
        print()
        return ultimo_disco

    data_serializada = mbr.serializar()

    with open(path,'r+b') as d:
        post = d.read()[len(data_serializada):]
        d.seek(0)
        d.write(data_serializada)
        d.write(post)
        d.close()

    print("Se ha creado la particion "+name+" con tamano de "+str(size)+" byte(s) de manera exitosa")    
    print()
    return ultimo_disco

