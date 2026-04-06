#Programe la función leer_guaguas(archivo) que
#recibe el archivo 1920-2020_final.csv y retorna una tupla donde el prime valor de la
#tupla corresponda a una lista con los nombres de columnas del archivo y el segundo
#elemento corresponda a una lista de listas donde cada elemento de la lista principal contenga la
#fila del archivo

def leer_guaguas(archivo):
    lista_parametros=[]
    lista_datos=[]
    with open(archivo,"r") as f:
        cont=0
        for linea in f:
            if cont==0:
                lista_parametros=tuple(linea.strip().split(";"))
                cont=cont+1
            else:
                lista_datos.append(list(linea.strip().split(";")))
            
    return lista_parametros,lista_datos

gua="1920-2020_final.csv"
print(leer_guaguas(gua))



    