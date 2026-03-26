#Objetivo: Leer un archivo de texto que contiene un párrafo y contar la frecuencia de cada
#palabra, almacenando los resultados en un diccionario.

def contar_palabras(archivo):
    d=dict()
    with open(archivo,'r',encoding='UTF-8') as f:
        for linea in f:
            linea=linea.strip()
            lista=linea.split(' ')
            for i in lista:
                if i in d:
                    d[i]=d[i]+1
                else:
                    d[i]=1
    return d

palabras='texto.txt'
print(contar_palabras(palabras))


