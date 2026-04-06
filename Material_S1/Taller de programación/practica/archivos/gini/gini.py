def mayor_desigualdad(archivo):
    with open(archivo,'r',encoding="UTF-8") as f:
        d=dict()
        for linea in f:
           lista= linea.split(",")
           d[lista[0]]=lista[1].rstrip("\n")
    mayores= sorted(list(d.values()),reverse=True)[0:5]
    a=dict()
    for clave,valor in d.items():
        if valor in mayores:
            a[clave]=valor

    return a

gini_p="gini_by_country.csv"
print(mayor_desigualdad(gini_p))
