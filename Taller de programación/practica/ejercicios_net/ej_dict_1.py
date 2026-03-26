def contar_vocales(texto):
    # Inicializar un diccionario con las vocales
    conteo_vocales = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
    
    # Recorrer cada carácter en el texto
    for char in texto.lower():
        if char in conteo_vocales:
            conteo_vocales[char] += 1
    
    return conteo_vocales

# Ejemplo de uso
texto = "Esta es una prueba de contar vocales."
resultado = contar_vocales(texto)
print(resultado)