#Objetivo 1: Escriba una funcion que reciba el nombre de un archivo con las medallas por
#país de los juegos panamericanos y retorne una lista de tuplas, donde cada tupla contiene el
#país (str) y el tipo de medalla (str).

def leer_medallas(medallas):
    medallas_list=[]
    with open(medallas,'r',encoding='UTF-8') as f:
        for linea in f:
            lista=tuple(linea.strip().split(' '))
            lista_sin_ultimo = lista[:-1]
            medallas_list.append(lista_sin_ultimo)

        if medallas_list:
            medallas_list.pop(0) #pop() sirve para eliminar un elemento en la lista
        
    return medallas_list

archivo='medallas.txt'
print(leer_medallas(archivo))