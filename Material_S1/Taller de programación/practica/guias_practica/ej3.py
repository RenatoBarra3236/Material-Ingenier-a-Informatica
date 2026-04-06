d=dict()

def frecuencia_elementos(lista):
    for i in lista:
        if i in d:
            d[i]+=1
        else:
            d[i]=1
    return d

lista=[1,2,2,3,4,3,3]
print(frecuencia_elementos(lista))
