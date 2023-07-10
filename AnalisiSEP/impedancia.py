import numpy as np
import math

#Cálculo de las impedancias de cortocircuito
def generador(g_res,g_reac):
    x =(g_reac)*1j
    impedancia_generador = np.add(g_res,x)
    
    #En caso de no haber una impedancia de cortocircuito añade una resistencia de 10^-6
    for i in range(len(impedancia_generador)):
        if impedancia_generador[i] == 0:
            impedancia_generador[i] == 0+(0.000001)*1j
    return impedancia_generador


#Calculo de las impedancias de las cargas
def carga(c_res,c_reac, tipo):
    recorrido = len(tipo)

    #Indica el tipo de reactancia
    for i in range(recorrido):
        if tipo[i] == "CAP":
            c_reac[i] = c_reac[i]*(-1)
    x = (c_reac)*1j
    impedancia_carga = np.add(c_res,x)
    return impedancia_carga

#Calculo de las impedancias de linea
def linea(l_res,l_reac, longitud, b_shunt):
    y_shunt = b_shunt*1j
    x = l_reac*1j
    impedancia_linea = np.add(l_res,x)
    for i in range(len(longitud)):
        impedancia_linea[i] = impedancia_linea[i]*longitud[i]
    return impedancia_linea, y_shunt

#Calculo de las corrientes inyectadas
def corrientes(voltaje,phi,impedancia_corto):
    #Grados a radianes
    for i in range(len(phi)):
        phi[i]= (phi[i] * math.pi)/180
    
    corriente_inyect = impedancia_corto
    #Voltajes de polar a rectangular
    for i in range(len(voltaje)):
        corriente_inyect[i] = voltaje[i]*(math.cos(phi[i]) + 1j*math.sin(phi[i]))/impedancia_corto[i]
        corriente_inyect[i] = round(corriente_inyect[i],4)
    return corriente_inyect
