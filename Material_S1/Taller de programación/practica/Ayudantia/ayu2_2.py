def n_consonantes(frase):
    d=dict()
    conso="qwrtypsdfghjklñzxcvbnm"
    c=0
    palabras=frase.split(" ")

    for i in palabras:
        c=0
        for n in i:
            if n in conso:
                c+=1
        d[i]=c
    return d
    
print(n_consonantes(input("ingrese su texto:")))


    
