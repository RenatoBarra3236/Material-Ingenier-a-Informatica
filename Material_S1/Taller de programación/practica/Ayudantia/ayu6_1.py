d=dict()

def listas_a_diccionario(claves,valores):
    for i in range(len(claves)):
        d[claves[i]]=valores[i]
    return d

print(listas_a_diccionario(["a","b","c"],[1,2,3]))
