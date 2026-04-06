import csv

n=int(input("cuantas personas ingresan: "))
d=dict()
for i in range(n):
    lista_notas=[]
    nombre=input(f"ingrese nombre persona {i+1}: ")
    notas=input(f"ingresa tus notas {i+1}: ")
    notas=notas.split(",")
    for a in notas:
        lista_notas.append(float(a))
    lista_notas.remove(min(lista_notas))
    d[nombre]=lista_notas

def retorno(datos,archivo_salida):
    with open(archivo_salida,"w",encoding="UTF-8") as f:
        writer=csv.writer(f, delimiter=",")
        writer.writerow([ "Nombre", "nota 1", "nota 2", "nota 3", "nota 4", "nota 5", "nota 6","nota 7","nota 8"])
        for key,value in datos.items():
            row=[key]+value+[""]*(8-len(value))
            writer.writerow(row)

archivo_salida="notas_ayudantías.csv"
retorno(d,archivo_salida)


    