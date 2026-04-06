numero=int(input("ingrese un numero: "))
if numero%2==0 and numero%5==0:
    print("el numero es par y multiplo de 5")
elif numero%2==0:
    print("el numero es par")
elif numero%2 !=0 and numero%5==0:
    print("el numero es impar y multiplo de 5")
else:
    print("el numero es impar")