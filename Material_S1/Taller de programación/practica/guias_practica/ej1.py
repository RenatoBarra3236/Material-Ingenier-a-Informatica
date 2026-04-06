import random  

nombres=['Pedro','Daniela','Juan','Paula','Diego','Javiera']
apellidos=['A.', 'C.', 'F.', 'G.', 'S.']
años=[1995,1996, 1997, 1998, 1999, 2000, 2001, 2002]
comunas= ['Santiago', 'Concepcion', 'Las Condes', 'Talcahuano']

d=dict()

def perso(nombres,apellidos,años,comunas,n=15):
    for i in range(n):

        #random.choice es para escoger una eleccion al azar dentro de la lista
        nombre=random.choice(nombres)
        apellido=random.choice(apellidos)
        año=random.choice(años)
        comuna=random.choice(comunas)

        #definiendo los elementos de la lista
        llave= f"{nombre} {apellido}"

        # para no volver a repetir valores
        if llave not in d:
            d[llave]=(año, comuna)

    return d

def contactos(nombre,d1):
    if nombre not in d1:
        return []
    
    comuna_busqueda = d1[nombre][1]
    mismos_contactos = [llave for llave, (año, comuna) in d1.items() if comuna == comuna_busqueda and llave != nombre]
    
    return mismos_contactos

print(perso(nombres,apellidos,años,comunas,n=15))
