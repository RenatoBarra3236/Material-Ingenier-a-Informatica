d=dict()

def costo(frutas,precio):
    x=input("que fruta desea llevar?:")
    y=int(input("cuanta kilos de esa fruta va a llevar?:"))
    while x not in frutas:
        x=input("ingrese una fruta valida:")
    z= d[precio]*y
    d[frutas]=z

print(costo(["platana","manzana","pera","naranja"]),[1.35,0.80,0.85,0.70])
    
