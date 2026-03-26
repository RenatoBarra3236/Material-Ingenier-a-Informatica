#Objetivo: Leer un archivo que contiene una lista de nombres (uno por línea) y guardarlos en
#una lista en Python.

def leer_nombre(archivo):
    with open(archivo,"r",encoding="UTF-8") as f:
        lista=[]
        for linea in f:
            nombre=linea.strip()
            lista.append(nombre)
    return lista

nombres="Radios_planetas.txt"
print(leer_nombre(nombres))
