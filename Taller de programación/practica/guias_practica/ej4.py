def contar_vocales(frase):

    d={"a":0, "e":0, "i":0, "o":0, "u":0}

    for i in frase.lower():
        if i in d:
            d[i] += 1

    return d

texto = "hola querida mia cuento tiempo"
print(contar_vocales(texto))
        
        