d=dict()

def tuplas_a_diccionario(tuplas): 
    for clave, valor in tuplas:
        d[clave]=valor
        
    return d

tupla= [('1','Diamante'), ('4','Trebol'), ('K','Corazon')]
print(tuplas_a_diccionario(tupla))