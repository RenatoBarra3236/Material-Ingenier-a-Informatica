#Programe la función guaguas_top_2020(archivo) que
#recibe el archivo 1920-2020_final.csv y retorna los diez nombres de guaguas más
#populares durante el año 2020 con su respectiva ocurrencia.

def guaguas_top_2020(archivo):
    with open(archivo, 'r',encoding="UTF_8") as f:
        d=dict()
        for linea in f:
            if "2020" in linea:
                lista=linea.strip().split(";")
                d[lista[1]]=int(lista[3])
    top_10= sorted(d.values(),reverse=True)[:10]

    top_10_dict = {}
    for key, value in d.items():
        if value in top_10:
            top_10_dict[key] = value
    
    return top_10_dict

gua="1920-2020_final.csv"
print(guaguas_top_2020(gua))