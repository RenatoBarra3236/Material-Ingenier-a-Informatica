d=dict()
with open("Radios_planetas.txt","r",encoding="UTF-8") as f:
    for linea in f:
        lista=linea.strip().split(",")
        d[lista[0]]=4*3.14*(float(lista[1])**2)

with open("Areas_planetas.txt","w",encoding="UTF-8") as j:
    for llave, valor in d.items():
        j.write(f"{llave}:{valor}\n")