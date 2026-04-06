def resumen_calificaciones(lista):
  d,l = dict(), []
  for i in range(len(lista)):
    l.append(lista[i][1])
  d["max"], d["min"],d["med"] = lista[l.index(max(l))], lista[l.index(min(l))], sum(l)/len(l)
  return d

l = [('Ana', 90), ('Bob', 85), ('Carla', 77)] 
print(resumen_calificaciones(l))