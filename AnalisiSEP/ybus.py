import numpy as np
import sys

def ybus(generador, carga, linea, num_barras, index_li, index_lj, yshunt, longitud):
    matriz_dato = np.concatenate([generador, carga, linea], axis=0)
    salida_bus = np.zeros((num_barras,num_barras),dtype="complex_")


    filas, columnas = matriz_dato.shape

#admitancias de las lineas (fuera de la diagonal)
    for k in range(filas):
        i = int(matriz_dato[k,0].real-1)
        j = int(matriz_dato[k,1].real-1)
        if i != -1 and j != -1:
            if i == -1:
                i += 1
            elif j == -1:
                j += 1
            salida_bus[i,j] = (-1)/(matriz_dato[k,2])
            salida_bus[i,j] = round(salida_bus[i,j],4)
            salida_bus[j,i] = salida_bus[i,j]

#admitancias de la diagonal
    aux = np.sum(salida_bus, axis=1)
    aux = np.diag(aux)

    salida_bus = salida_bus - aux

    for k in range(filas):
        i = int(matriz_dato[k,0].real-1)
        j = int(matriz_dato[k,1].real-1)
        if i == -1 or j == -1:
            if i == -1:
                salida_bus[j,j] = salida_bus[j,j] + 1/matriz_dato[k,2]
            elif j == -1:
                salida_bus[i,i] = salida_bus[i,i] + 1/matriz_dato[k,2]

#Influencia del efecto capacitivo (Y shunt)
    matriz_shunt = np.zeros((num_barras,num_barras),dtype="complex_")
    for k in range(len(index_li)):
        i = index_li[k] -1
        j = index_lj[k] -1
        if longitud[k] >80:
            matriz_shunt[i,i] = matriz_shunt[i,i] + yshunt[k]/2
            matriz_shunt[i,i] = matriz_shunt[i,i] + yshunt[k]/2

    salida_bus = salida_bus + matriz_shunt






    return salida_bus

