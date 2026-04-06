from random import randrange

def cantidad(n):
    L=[]
    cont=0
    x= int(input("Cuan largo quiere su lista?:"))
    for i in range(x):
        L.append(randrange(x))
    for j in L:
        if j == n:
            cont+=1
    print(L)
    return f"existen {cont} numeros "

print(cantidad(5))