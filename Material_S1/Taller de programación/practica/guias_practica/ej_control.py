def num_caracteres(n):
    dicc_n_caracteres=dict()
    caracteres="qwertyuiopasdfghjklñzxcvbnm"
    
    for i in range(n):
        x=input("Ingrese un texto:")
        c=0
        for j in x:
            if j in caracteres:
                c+=1
        dicc_n_caracteres[x]=c
    return dicc_n_caracteres

print(num_caracteres(2))
        




