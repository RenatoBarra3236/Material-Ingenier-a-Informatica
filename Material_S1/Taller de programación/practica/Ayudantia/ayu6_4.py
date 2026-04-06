def tuplas_sin_duplicados(tupla):
    lista_f=[]
    for i in tupla:
        lista_sin=[]
        for c in i:
            if c not in lista_sin:
                lista_sin.append(c)
        lista_f.append(tuple(lista_sin))
    return lista_f

tuplas=((1,2,5,2,1),("a","a","b"),(4,4,33),("hola","HOLA","chao"))
print(tuplas_sin_duplicados(tuplas))