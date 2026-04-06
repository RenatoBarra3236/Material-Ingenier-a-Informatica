palabra=[]
palabra_invertida=[]
palabras=input("ingresa palabras hasta escribir salir: ")   
palabras.lower()
while palabras != "salir":
    palabra.append(palabras)
    palabras=input("ingresa palabra:")

for j in palabra:
    pa=j[::-1]
    palabra_invertida.append(pa)
print(palabra_invertida)
