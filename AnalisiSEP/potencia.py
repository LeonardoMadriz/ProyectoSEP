import numpy as np
import math

#--------------------------------------------------- POTENCIA DEL GENERADOR -----------------------------------------
def generador(imp_gen, voltaje, phi, vth, index_gen):

    #Pasamos el voltaje del generador a su forma rectangular
    voltaje_generado=np.zeros((len(voltaje),1),dtype="complex_")
    for i in range(len(voltaje)):
        voltaje_generado[i,0] = voltaje[i]*(math.cos(phi[i]) + math.sin(phi[i])*1j)

    #Calculo de la corriente del generador
    corriente_generado=np.zeros((len(voltaje),1),dtype="complex_")
    for i in range(len(voltaje)):
        indice_vth = index_gen[i] - 1
        voltaje_carga = voltaje_generado[i,0] - vth[indice_vth,0]
        corriente_generado[i,0] = voltaje_carga/imp_gen[i]
    
    #Potencia de los generadores
    p_generado=np.zeros((len(voltaje),1),dtype="complex_")
    q_generado=np.zeros((len(voltaje),1),dtype="complex_")
    
    p_generado = (voltaje_generado * np.conjugate(corriente_generado)).real
    q_generado = (voltaje_generado * np.conjugate(corriente_generado)).imag
        
    return p_generado, q_generado
#---------------------------------------------------- POTENCIA DE LA CARGA ------------------------------------------