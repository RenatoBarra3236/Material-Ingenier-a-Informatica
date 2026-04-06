num=[]
for numero in range(3): 
    numero=int(input("ingresa 3 numeros: "))
    num.append(numero)
    if numero == num:
        numero=int(input("ingresa un numero distinto: "))

    num_sets= set(num)
    num_tupla=tuple(num)

print(num_tupla,num_sets)
    


