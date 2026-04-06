import random

def apuesta(n,m):
    tombola=[]
    dinero=0
    c=0
    for i in range(25):
        tombola.append(random.randrange(1,11))
        if n in tombola:
            c+=1
    if c>3:
        print("usted a ganado: ")
        dinero=m*2
    else:
        print("usted a perdido: ")

    return tombola,dinero

print(apuesta(4,100))
