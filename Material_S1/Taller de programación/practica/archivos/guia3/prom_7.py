#Objetivo: Leer un archivo con información de empleados (ID, nombre, departamento) y
#generar un nuevo archivo que agrupe a los empleados por departamento.

def agrupar_empleados(archivo_entrada, archivo_salida):
    depa={}
    with open(archivo_entrada,'r',encoding='UTF-8') as f:
        for linea in f:
            lista=linea.strip().split(',')
            id=lista[0]
            nombre=lista[1]
            departamento=lista[2]
            if departamento in depa:
                depa[departamento].append(nombre)
            else:
                depa[departamento] = [nombre]
    
    with open(archivo_salida, 'w', encoding='UTF-8') as j:
        for llave, valor in depa.items():
            nombre = ', '.join(valor)
            j.write(f'{llave}:{nombre}\n')

archivo_entrada = 'empleados.txt'
archivo_salida = 'grupo_empleados.txt'

agrupar_empleados(archivo_entrada, archivo_salida)          
                


