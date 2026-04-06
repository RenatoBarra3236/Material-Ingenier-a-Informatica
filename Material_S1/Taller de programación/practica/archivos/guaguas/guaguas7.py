#Programe la función efecto_romane(nombre, archivo)
#que recibe al archivo 1920-2020_final.csv y el string nombre ; y retorna una
#estructura de datos (lista, tupla o diccionario) con el número de guaguas registradas con el
#nombre de alguno de los personajes principales de la teleserie Romané para el año de emisión
#2000 y el año anterior. Algunos de estos nombres pueden ser: Branco, Milenka y Yovanka

def efecto_romane(nombre,archivo):
    d={}
    c=0
    with open(archivo,'r',encoding="UTF-8") as f:
        next(f) #saltar cabecera (si existe)
        for linea in f:
            lista=linea.strip().split(";")
            año=lista[0]
            if año in ["1999","2000"]:
                num=lista[1].count(nombre)
                if año in d:
                    d[año]+=num
                else:
                    d[año]=num
    return d

gua="1920-2020_final.csv"
print(efecto_romane("Milenka",gua))



