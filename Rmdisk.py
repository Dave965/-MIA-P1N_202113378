import os
def com_rmdisk(params):
    path = None

    for x in params:
        param = [w.strip() for w in x.split("=")]
        if param[0].lower() != "path":
            print("--Parametro '"+param[0]+"' no reconocido para el comando 'execute'")
            print()
            return
        
        if len(param)<2:
            print("--El parametro 'path' necesita una direccion")
            print()
            return

        if param[1][0] == '"':
            path = param[1][1:-1]
        else:
            path = param[1]

    if path == None:
        print("--No se encontro el parametro obligatorio 'path'")
        print()
        return

    if not os.path.isfile(path):
        print("--No existe un disco en '"+path+"'")
        print()
        return

    print(">>Seguro que quieres borrar este disco? (Y/N)")
    s = input(">>")

    if s.lower() == 'y':
        os.remove(path)
        print("--Disco removido con exito")
        print()
        return

    print("--No se ha borrado el disco")
    print()
    
