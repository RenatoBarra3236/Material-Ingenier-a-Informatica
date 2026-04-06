#Objetivo: Leer un archivo con datos de productos en formato "ID, Nombre, Precio" y
#almacenarlos en un diccionario donde el ID es la clave y el valor es otra tupla con
#nombre y precio

def leer_productos(archivo):
    d=dict()
    with open(archivo,'r',encoding='UTF-8') as f:
        for linea in f:
            lista=linea.strip().split(',')
            d[lista[0]]=(lista[1], lista[2])
            
    return d

producto='productos.txt'
print(leer_productos(producto))