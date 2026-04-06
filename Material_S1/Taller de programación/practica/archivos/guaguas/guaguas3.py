#Programe la función guaguas_n_anio(archivo) que
#recibe el archivo 1920-2020_final.csv y retorna un diccionario donde la llave
#corresponde al año y el valor al número de guaguas registradas para ese año.

def guaguas_n_anio(archivo):
    d=dict()
    with open(archivo, 'r',encoding="UTF-8") as f:
        c=0
        for linea in f:
            if c==0:
                c+=1
                continue
            else:
                lista=linea.strip().split(";")
                año=int(lista[0])
                numero=int(lista[3])
                if año in d:
                    d[año]+=numero
                else:
                    d[año]=numero
                
    return d

gua="1920-2020_final.csv"
print(guaguas_n_anio(gua))