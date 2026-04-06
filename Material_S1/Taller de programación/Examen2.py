import csv

def clima(archivo):
    d=[]
    with open(archivo,"r",encoding="UTF-8") as f:
        next(f)
        for linea in f:
            lista=linea.strip().split(",")
            Ciudad=lista[0]
            T_min=int(lista[1])
            T_max=int(lista[2])
            T_dif=T_max-T_min
            d.append([Ciudad,T_min,T_max,T_dif])
    return d
    
def retorno(datos,archivo_s):
    with open(archivo_s,"w",encoding="UTF-8") as j:
        writer=csv.writer(j, delimiter=",")
        writer.writerow(["Ciudad","T_min","T_max","T_dif"])
        for Ciudad,T_min,T_max,T_dif in datos:
            writer.writerow([Ciudad,T_min,T_max,T_dif])

cli="clima.txt"
datos_cli=clima(cli)

archivo_s="clima_final.csv"
retorno(datos_cli,archivo_s)

