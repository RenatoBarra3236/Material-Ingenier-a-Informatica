#Programe la función
#guaguas_sex_dicc(archivo) que recibe al archivo 1920-2020_final.csv y retorna
#un diccionario donde la llave es el año de inscripción y el valor es una tupla de dos elementos
#en la que cada elemento corresponda al número de guaguas de sexo femenino y masculino.

def guaguas_sex_dicc(archvio):
    d={}
    femenino=0
    masculino=0
    c=0
    with open(archvio,"r",encoding="UTF-8") as f:
        for linea in f:
            if c==0:
                c+=1
                continue
            else:
        
                lista=linea.strip().split(";")
                año=lista[0]
                sexo=lista[2]
                num=lista[3]
                if sexo=="F":
                    femenino+=int(num)
                elif sexo=="M":
                    masculino+=int(num)
                d[año]=(femenino,masculino)
    return d

gua="1920-2020_final.csv"
print(guaguas_sex_dicc(gua))
        