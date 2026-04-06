def actualizar_inventario(d,tuplas):
  for clave, valor in tuplas:
    if clave in d:
      d[clave]+=valor
    else:
      d[clave]=valor


  return d

d={"manzana":25, "banana":36, "zanahoria":50}
nuevo_envio=[("manzana", 10), ("zanahoria", 20), ("leche", 15)]

print(actualizar_inventario(d,nuevo_envio))