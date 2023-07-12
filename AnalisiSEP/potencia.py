import numpy as np
import math

#--------------------------------------------------- POTENCIA DEL GENERADOR -----------------------------------------
def generador(imp_gen, voltaje, phi, vth, index_gen):
#Voltajes de polar a rectangular
    voltaje_rect = np.zeros((len(voltaje),1), dtype="complex_")
    #Grados a radianes
    for i in range(len(phi)):
        phi[i]= (phi[i] * math.pi)/180
    #Paso de polar a rectangular
    for i in range(len(voltaje)):
        voltaje_rect[i] = voltaje[i]*(math.cos(phi[i]) + math.sin(phi[i])*1j)
    
#Calculo de la corriente por el generador
    #Voltaje que ve la impedancia de cortocircuito
    vol_carga = np.zeros((1,len(voltaje)),dtype="complex_")
    for i in range(len(voltaje)):
        vol_carga[0,i] = np.subtract(voltaje_rect[i,0],vth[index_gen[i],0])
    #Calculo de la corriente del generador
    i_gen= vol_carga/imp_gen
    
#Calculamos la potencia de los generadores
    i_conjugada = np.conjugate(i_gen)
    s_gen = np.zeros((len(i_conjugada),1), dtype="complex_")
    for i in range(len(i_conjugada)):
        s_gen[i,0] = voltaje_rect[i,0] * i_conjugada[0,i]

    #Potencia activa del generador
    p_gen = np.zeros((len(s_gen),1), dtype="float_")
    for i in range(len(s_gen)):
        p_gen[i,0] = s_gen[i,0].real

    #Potencia reactiva del generador
    q_gen = np.zeros((len(s_gen),1), dtype="float_")
    for i in range(len(s_gen)):
        q_gen[i,0] = s_gen[i,0].imag

    return p_gen, q_gen