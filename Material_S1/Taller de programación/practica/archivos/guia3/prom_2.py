#Objetivo: Leer un archivo que contiene pares de datos (nombre, edad) separados por
#comas en cada línea y almacenarlos en una lista de tuplas.

def leer_datos_personales(archivo):
    d=dict()
    with open(archivo,"r",encoding="UTF-8") as f:
        for linea in f:
            lista=tuple(linea.strip().split(","))
            d[lista]=lista

    return d

datos="datos_personales.txt"
print(leer_datos_personales(datos))
            
