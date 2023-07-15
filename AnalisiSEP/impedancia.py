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
def carga(c_res,c_reac, tipo, barra, corriente,potencia_reac,voltaje,potencia_aparente, potencia_acti, fp):
    recorrido = len(barra)

    impedancia_carga = np.full((len(barra)),0, dtype="complex_")
    x = np.full((len(barra)),0, dtype="complex_")

    for i in range(recorrido):
        if c_res[i] != 2121212 and c_reac[i] != 2121212:
            if tipo[i] == "CAP":
                c_reac[i] = c_reac[i]*(-1)

            x[i] = (c_reac[i])*1j
            impedancia_carga[i] = np.add(c_res[i],x[i])

        elif corriente[i] != 2121212 and potencia_reac[i] != 2121212:
            potencia_reac[i] = (potencia_reac[i])*(10**3)
            impedancia_carga[i] = potencia_reac[i] / corriente[i]**2
            if tipo[i] == "CAP":
                impedancia_carga[i] = impedancia_carga[i] * (-1j)
            impedancia_carga[i] = impedancia_carga[i]*(1j)

        elif voltaje[i] != 2121212 and potencia_acti[i] != 2121212 and potencia_reac[i] == 2121212 and fp[i] == 2121212:
            impedancia_carga[i] = (voltaje[i]**2)/potencia_acti[i]
            impedancia_carga[i] = np.conjugate(impedancia_carga[i])


        elif voltaje[i] != 2121212 and potencia_reac[i] != 2121212 and potencia_acti[i] != 2121212:
            s_datos = 1j
            if tipo[i] == "CAP":
                potencia_reac[i] = potencia_reac[i]*(-1j)
            potencia_reac[i] = potencia_reac[i]*(1j)
            s_datos = potencia_acti[i] + potencia_reac[i]
            impedancia_carga[i] = voltaje[i]**2/s_datos

        elif voltaje[i] != 2121212 and potencia_acti[i] != 2121212 and fp[i] != 2121212:
            modulo_impedancia = 1j
            imaginario = 1j
            modulo_impedancia = voltaje[i]/potencia_acti[i]
            real = math.cos(math.acos(fp[i]))
            imaginario = math.sin(math.acos(fp[i]))*1j

            if tipo[i] == "CAP":
                imaginario = imaginario*(-1)

            impedancia_carga[i] = modulo_impedancia*(real + imaginario)
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
    corriente_inyect = corriente_inyect

    return corriente_inyect

#----------------------------------------------COMPENSADORES--------------------------------------------------------
def compensadores(xcomp, barra, tipo, vnom, qcomp):
    ycomp = np.full((len(barra)),0, dtype="complex_")
    index_bus = np.full((len(barra)),0)
    for i in range(len(barra)):
        if xcomp[i] != 2121212:

        #Tipo de compensador
            if tipo[i] == "CAP":
                xcomp[i] = xcomp[i]*(-1)

            index_bus[i] = barra[i] - 1
            ycomp[i] = (1/xcomp[i])*(-1j)

        else:
            index_bus[i] = barra[i] - 1
            ycomp[i] = (vnom[i]**2)/qcomp[i]
            ycomp[i] = (1/ycomp[i])*1j

            if tipo[i] == "CAP":
                ycomp[i] = ycomp[i]*(-1)

    return ycomp, index_bus
