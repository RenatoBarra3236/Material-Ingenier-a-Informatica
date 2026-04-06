import random
d=dict()

def naipes():

    #Creamos la baraja
    baraja=[]
    pinta=['Corazones', 'Diamantes', 'Tréboles', 'Picas']
    numeros=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', "14"]
    for p in pinta:
        for n in numeros:
            baraja.append((p,n))
    
    # Función para mezclar la baraja
    random.shuffle(baraja)

    return baraja

def repartir(n):
    if n > 8 or n < 1:
        raise ValueError("El número de jugadores debe estar entre 1 y 8.")
    
    mazo = naipes()
    repartidas = [[] for _ in range(n)]
    
    for i in range(5):
        for j in range(n):
            repartidas[j].append(mazo.pop(0))
           #El método pop() elimina y retorna un elemento de una lista.
    
    return repartidas

# Ejemplo de uso de la función repartir
jugadores = repartir(4)
print("\nCartas repartidas a los jugadores:")
for i, cartas in enumerate(jugadores):
    print(f'Jugador {i+1}: {cartas}')

def ganador(lista):
    def valor_carta(carta):
        return carta[0]
    
    # Ordenar cada mano de cartas de los jugadores
    manos_ordenadas = [sorted(mano, key=valor_carta, reverse=True) for mano in lista]
    
    # Comparar las manos carta por carta
    for i in range(5):
        max_valor = max(mano[i][0] for mano in manos_ordenadas)
        jugadores_con_max_valor = [index for index, mano in enumerate(manos_ordenadas) if mano[i][0] == max_valor]
        
        if len(jugadores_con_max_valor) == 1:
            return jugadores_con_max_valor[0]  # Un solo jugador con la carta más alta en esta posición

    # Si todos las cartas se compararon y aún hay empate, retornar el primero (aunque esto no debería pasar en condiciones normales)
    return jugadores_con_max_valor[0]

# Ejemplo de uso de la función ganador
jugador_ganador = ganador(jugadores)
print(f'\nEl jugador ganador es: Jugador {jugador_ganador + 1}')



