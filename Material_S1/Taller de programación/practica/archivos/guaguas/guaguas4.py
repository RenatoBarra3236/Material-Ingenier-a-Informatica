#Programe la función
#guaguas_sexo_anio(año, archivo) que recibe el string año y el archivo
#1920-2020_final.csv , y retorna una tupla de dos elementos con el número de guaguas
#de sexo femenino y masculino registrados para el año

def guaguas_n_anio(año, archivo):
    femenino=0
    masculino=0
    with open(archivo, 'r', encoding="UTF-8") as f:
        for linea in f:
            if año in linea:
                lista=linea.strip().split(";")
                sexo=lista[2]
                num=int(lista[3])
                if sexo=="F":
                    femenino+=num
                elif sexo=="M":
                    masculino+=num
    
    return (femenino,masculino)
gua="1920-2020_final.csv"
print(guaguas_n_anio("2010", gua))
        
        
                

