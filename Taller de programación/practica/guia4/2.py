num= input("ingresa los numeros separados por comas: ")
lista=[float(numero) for numero in num.split(",")]
suma=sum(lista)
promedio= suma/len(lista)
print(suma,promedio)