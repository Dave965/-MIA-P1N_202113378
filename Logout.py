from Clases import *
from Fhandler import *
import os

def com_logout(lista_particiones, sesion_activa):
    if not sesion_activa:
        print("--No hay sesion activa")
        print()
        return

    res = [x for x in lista_particiones if x["identificador"] == sesion_activa["particion"]]
    if len(res) == 0:
        print("--No existe el id '"+sesion_activa["particion"]+"' entre las particiones cargadas")
        print()

    sesion_activa = None
    print("Se ha cerrado sesion")
    print()

    res[0]["datos"] = guardar_journaling("logout",[],res[0]["datos"])
    return sesion_activa
