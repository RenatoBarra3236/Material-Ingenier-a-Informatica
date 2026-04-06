#Objetivo: Leer un archivo con datos de ventas (fecha, producto, cantidad) y escribir un
#nuevo archivo con un resumen de ventas por producto.

def resumen_ventas(archivo_entrada):
    ventas = {}
    with open(archivo_entrada, 'r', encoding='UTF-8') as f:
        for linea in f:
            lista = linea.strip().split(',')
            fecha = lista[0]
            producto = lista[1]
            cantidad = int(lista[2])
            if producto in ventas:
                ventas[producto] += cantidad
            else:
                ventas[producto] = cantidad
    return ventas

def guardar_datos(datos, archivo_salida):
    with open(archivo_salida, 'w', encoding='UTF-8') as j:
        for key, value in datos.items():
            j.write(f'{key}:{value}\n')

archivo_entrada = 'ventas.txt'
archivo_salida = 'Nuevas_ventas.txt'

datos_ventas = resumen_ventas(archivo_entrada)
guardar_datos(datos_ventas, archivo_salida)





    


