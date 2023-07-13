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
def Cargas(imp_carga, Vth, bus_i_carga):
    
    for k in range(len(bus_i_carga)):
        if bus_i_carga[k] != 0:

            admitancia = 1/imp_carga
            #print(imp_carga)
            #print(admitancia)
            admitanciaConjugada = np.conjugate(admitancia)
                        
            S_carga = np.zeros((len(admitanciaConjugada), 1), dtype="complex_")
            
            #Potencia aparente carga
            for m in range(len(admitanciaConjugada)):
                S_carga[m] = ((Vth[m]) ** 2) * (admitanciaConjugada[m])

            #Potencia activa carga
            P_carga = np.zeros((len(S_carga), 1), dtype="float_")
            for s in range(len(S_carga)):
                P_carga[s, 0] = S_carga[s, 0].real

            #Potencia reactiva carga
            Q_carga = np.zeros((len(S_carga), 1), dtype="float_")
            for t in range(len(S_carga)):
                Q_carga[t, 0] = S_carga[t, 0].imag

    #print(f"Sc {k}: {S_carga}\n\nPc: {P_carga}\n\nQc: {Q_carga}")
    return S_carga, P_carga, Q_carga

#------------------------------------------------ LINEFLOW --------------------------------------------------------
def lineflow(indice_l, dato_lineas, longitud, voltline):
    filas, columnas = indice_l.shape
    impline = np.zeros((filas,1),dtype="complex_")
    z_ij = np.zeros((filas,1),dtype="complex_")
    z_ji = np.zeros((filas,1),dtype="complex_")
    impline = dato_lineas[:,0] + dato_lineas[:,1]*1j
    impline = 1/(impline*longitud)

    for k in range(filas):
        v_i = voltline[indice_l[k,0] - 1,0]
        v_j = voltline[indice_l[k,1] - 1,0]
        corr_i = (v_i - v_j)*impline[k]
        corr_j = (v_j - v_i)*impline[k]
        z_ij [k,0] = v_i * np.conjugate(corr_i)
        z_ji[k,0] = v_j * np.conjugate(corr_j)

    Pij = np.real(z_ij)
    Qij = np.imag(z_ij)
    Pji = np.real(z_ji)
    Qji = np.imag(z_ji)

    return Pij, Qij, Pji, Qji

#-------------------------------------------------BALANCE DE POTENCIAS-------------------------------------------------
def balance(p_gen, q_gen, p_load, q_load):
    p_entregado = p_gen.sum(axis=0)
    q_entregado = q_gen.sum(axis=0)

    p_carga = p_load.sum(axis=0)
    q_carga = q_load.sum(axis=0)

    delta_p = p_entregado - p_carga
    delta_q = q_entregado - q_carga
    return delta_p, delta_q