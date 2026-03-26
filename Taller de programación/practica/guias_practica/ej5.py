def listas_a_diccionarios(claves,valores):
    return dict(zip(claves,valores))

print(listas_a_diccionarios(["a","b","c"],[1,2,3]))