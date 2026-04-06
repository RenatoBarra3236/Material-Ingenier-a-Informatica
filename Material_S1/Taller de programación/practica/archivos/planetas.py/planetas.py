import csv

def areas(archivo): 
    with open(archivo,"r",encoding="UTF-8") as f:
        d=[]
        for linea in f:
            lista=linea.strip().split(",")
            nombre=(lista[0])
            radio=float(lista[1])
            area=4*3.14*(radio**2)
            d.append((nombre,area))
    return d

def guardar_areas(datos,archivo_s):
    with open(archivo_s,"w",newline="",encoding="UTF-8") as j:
        writer=csv.writer(j)
        writer.writerow(["nombre del planeta", "area de este"])
        for nombre, area in datos:
            writer.writerow([nombre,area])

planetas="Radios_planetas.txt"
datos_areas=areas(planetas)

archivo_s="Areas_planetas.csv"
guardar_areas(datos_areas, archivo_s)

print(f"las areas de guardaron en {archivo_s}")
