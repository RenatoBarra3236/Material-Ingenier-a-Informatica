def casos_covid(archivo):
    with open(archivo,"r",encoding="UTF-8") as f: #encoding="UTF-8" sirve para 
        d=dict()
        for l in f: #recorremos las lines dado que son str
            if "Biob" in l: #si biobio esta en las lineas
                lista= l.split(",") #creamos una lista de todos los str separados por ,
                d[lista[2]]=float(lista[-1][0:len(lista[-1])-1]) #el diccionario que toma la comuna y el valor 
    Mayo= sorted(list(d.values()),reverse=True)[0:5] #definimos una variable con los 5 primeros datos mayores
    a=dict() #creamos un nuevo diccionario
    for key, valor in d.items(): #para llave, valores en el diccionario de los items de la primera lista
        if valor in Mayo: #verificar si el valor esta en ,la variable Mayo
            a[key]=valor #asignamos los valores al nuevo diccionario
                    
    return a

contagios="2020-05-01-CasosConfirmados.csv" #definimos una variable con el nombre del archivo
print(casos_covid(contagios))
            