import csv

def guaguas_escribir_tabla(archivo):
    d={}
    c=0
    with open(archivo, 'r',encoding="UTF-8") as f:
        for linea in f:
            if c==0:
                c+=1
                continue
            else:
                lista=linea.strip().split(";")
                año=lista[0]
                sexo=lista[2]
                num=int(lista[3])

                if año not in d:
                    d[año]={"M":0,"F":0}

                if sexo=="M":
                    d[año]["M"]+=num
                elif sexo=="F":
                    d[año]["F"]+=num

    resultado=[[año,datos["F"],datos["M"]] for año,datos in d.items()] #convertimos el diccionario en lista
    return resultado

def retorno(datos,archivo_salida):
    with open(archivo_salida, 'w',newline='',encoding="UTF-8") as j:
        writer = csv.writer(j, delimiter=';')
        writer.writerow(["Año","f","m"])
        for año,masculino,femenino in datos:
            writer.writerow([año,masculino,femenino])

gua="1920-2020_final.csv"
datos_gua=guaguas_escribir_tabla(gua)

archivo_salida="1920_2020_resumen.csv"
retorno(datos_gua,archivo_salida)



