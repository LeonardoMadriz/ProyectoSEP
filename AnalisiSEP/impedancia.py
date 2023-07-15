import numpy as np
import math

#---------------------------------------------IMPEDANCIAS DE LOS GENERADORES------------------------------------------
def generador(g_res,g_reac):
#Impedancia del generador
    x =(g_reac)*1j
    impedancia_generador = np.add(g_res,x)
    
#En caso de no haber una impedancia de cortocircuito añade una resistencia de 10^-6
    for i in range(len(impedancia_generador)):
        if impedancia_generador[i] == 0:
            impedancia_generador[i] == 0+(0.000001)*1j

    return impedancia_generador


#--------------------------------------------IMPEDANCIA DE LAS CARGAS------------------------------------------------
def carga(c_res,c_reac, tipo):
    recorrido = len(tipo)
#Tipo de reactancia(IND,CAP,RES)
    for i in range(recorrido):
        if tipo[i] == "CAP":
            c_reac[i] = c_reac[i]*(-1)

#Impedancia de la carga
    x = (c_reac)*1j
    impedancia_carga = np.add(c_res,x)
    return impedancia_carga

#-------------------------------------------IMPEDANCIAS DE LAS LINEAS------------------------------------------------
def linea(l_res,l_reac, longitud, b_shunt):
#Efecto capacitivo (Y shunt)
    y_shunt = b_shunt*1j*longitud

#Impedancia de la linea
    x = l_reac*1j
    impedancia_linea = np.add(l_res,x)
    for i in range(len(longitud)):
        impedancia_linea[i] = impedancia_linea[i]*longitud[i]
    return impedancia_linea, y_shunt

#--------------------------------------------CORRIENTES INYECTADAS--------------------------------------------------
def corrientes(voltaje,phi,impedancia_corto,num_barra,ind_g):
#Grados a radianes
    for i in range(len(phi)):
        phi[i]= (phi[i] * math.pi)/180

#Corrientes inyectadas
    corriente_inyect = np.zeros((num_barra,1),dtype="complex_")
    for i in range(len(ind_g)):
        indice = ind_g[i]-1
        corriente_inyect[indice] = voltaje[i]*(math.cos(phi[i]) + 1j*math.sin(phi[i]))/impedancia_corto[i] 
    corriente_inyect = np.round(corriente_inyect,4)

    return corriente_inyect

#----------------------------------------------COMPENSADORES--------------------------------------------------------
def compensadores(xcomp, barra, tipo):
    #Tipo de compensador
    for i in range(len(barra)):
        if tipo[i] == "CAP":
            xcomp[i] = xcomp[i]*(-1)
        else:
            continue

    #Calcula la admitancia de los compensadores
    ycomp = np.full((len(barra)),0, dtype="complex_")
    index_bus = np.full((len(barra)),0)
    for i in range(len(xcomp)):
        index_bus[i] = barra[i] - 1
        ycomp[i] = (1/xcomp[i])*1j

    return ycomp, index_bus
