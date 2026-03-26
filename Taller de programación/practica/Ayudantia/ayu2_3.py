from typing import Tuple

d=dict()

def tuplas_a_diccionario(n):
  l=[]
  for i in range(n):
    x=input("ingrese su nombre:")
    y=int(input("ingrese su edad:"))
    z= str(x),y
    tuple(z)
    l.append(tuple(z))
    d[i]=i


  return l
print(tuplas_a_diccionario(3))