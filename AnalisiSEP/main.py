import pandas as pd
import numpy as np
import impedancia
import ybus
import potencia
import compensadores
import os
from alive_progress import alive_bar
import time
import sys

#Lectura del archivo excel a trabajar
os.system("clear")
df_gen = pd.read_excel("data_io2.xlsx","GENERATION")                 #Generador
df_lines = pd.read_excel("data_io2.xlsx","LINES")                    #Lineas
df_load = pd.read_excel("data_io2.xlsx","LOAD")                      #Cargas
df_vnom = pd.read_excel("data_io2.xlsx", "V_NOM")                    #COVENIN 159
df_comp = pd.read_excel("data_io2.xlsx", "REACTIVE_COMP")            #Compensadores     
df_comp = df_comp.fillna(2121212)       
df_load = df_load.fillna(2121212)                        

#Numero de barras del sistema electrico de potencia
num_barras_i = max(df_lines.iloc[:,0])
num_barras_j = max(df_lines.iloc[:,1])
num_barras = int(max(num_barras_i,num_barras_j))



#------------------------------------------ ORDENANDO LOS DATOS LEIDOS --------------------------------------------------------
#GENERADOR:
imp_resis_gen = np.array(df_gen.iloc[:,4])                          #Impedancia resistiva
imp_react_gen = np.array(df_gen.iloc[:,5])                          #Impedancia reactiva
phi = np.array(df_gen.iloc[:,3],dtype="float_")                     #Angulo fasor voltaje
voltaje = np.array(df_gen.iloc[:,2])                                #Voltaje de la fuente
barra_gen_i = np.array(df_gen.iloc[:,0])                            #Barra de conexion i
barra_gen_j = np.full((len(df_gen.iloc[:,0])),0)                    #Barra de conexion j


#CARGAS
imp_resis_carga = np.array(df_load.iloc[:,9])                       #Impedancia resistiva
imp_react_carga = np.array(df_load.iloc[:,10])                      #Impedancia reactiva
tipo_carga = np.array(df_load.iloc[:,2])                            #Tipo de carga
barra_carga_i = np.array(df_load.iloc[:,0])                         #Barra de conexion i
barra_carga_j = np.full((len(df_load.iloc[:,0])),0)                 #Barra de conexion j
index_carga = np.concatenate(([barra_carga_i],[barra_carga_j]))     #Matriz de conexion de las cargas
index_carga = np.transpose(index_carga)
i_load = np.array(df_load.iloc[:,4])
q_carga = np.array(df_load.iloc[:,6], dtype = "complex_")
v_carga = np.array(df_load.iloc[:,3])
p_carga = np.array(df_load.iloc[:,5])
s_load = np.array(df_load.iloc[:,7])
fp = np.array(df_load.iloc[:,8])



#LINEAS
#Datos LINES
imp_resis_linea = np.array(df_lines.iloc[:,5])                      #Impedancia resistiva
imp_react_linea = np.array(df_lines.iloc[:,6])                      #Impedancia reactiva
b_shunt = np.array(df_lines.iloc[:,7])                              #admitancia del efecto capacitivo de las lineas
longitud = np.array(df_lines.iloc[:,4])                             #largo de las lineas
barra_linea_i = np.array(df_lines.iloc[:,0])                        #Barra de conexion i
barra_linea_j = np.array(df_lines.iloc[:,1])                        #Barra de conexion j
index_linea = np.concatenate(([barra_linea_i],[barra_linea_j]))     #Matriz de conexion de las cargas
index_linea = np.transpose(index_linea)


#VOLTAJE NOMINAL
#Datos V_NOM
v_nominal = float(df_vnom.iloc[0,1])                                #Voltaje nominal
v_max = float(df_vnom.iloc[0,3])                                    #Voltaje máximo segun COVENIN 159
v_min = float(df_vnom.iloc[0,2])                                    #Voltaje mínimo segun COVENIN 159

#COMPENSADORES
barra_comp_i = np.array(df_comp.iloc[:,0])
barra_comp_j = np.full((len(df_comp.iloc[:,0])),0)
tipo_comp = np.array(df_comp.iloc[:,2])
vnom_comp = np.array(df_comp.iloc[:,3])
qcomp = np.array(df_comp.iloc[:,4])
xcomp = np.array(df_comp.iloc[:,5])

def run():
#---------------------------------------------- CALCULO DE LAS IMPEDANCIAS---------------------------------------------- 
    #Generadores
    imp_gen = impedancia.generador(imp_resis_gen,imp_react_gen)
    gen =  np.concatenate(([barra_gen_i],[barra_gen_j],[imp_gen]), axis=0)
    gen = np.transpose(gen)
    #print("impedancia generador",imp_gen)
    
    #Cargas
    imp_carga = impedancia.carga(imp_resis_carga, imp_react_carga, tipo_carga, barra_carga_i, i_load, q_carga, v_carga,s_load, p_carga, fp)
    imp_carga = np.round(imp_carga,4)
    carga = np.concatenate(([barra_carga_i],[barra_carga_j],[imp_carga]),axis=0)
    carga = np.transpose(carga)
    print("impedancia carga",1/imp_carga)

    #Lineas
    imp_linea, y_shunt = impedancia.linea(imp_resis_linea,imp_react_linea,longitud, b_shunt)
    linea = np.concatenate(([barra_linea_i],[barra_linea_j],[imp_linea]),axis=0)      
    linea = np.transpose(linea)
    #print("impedancia de la linea",imp_linea)
    dato_linea = np.concatenate(([imp_resis_linea],[imp_react_linea]),axis=0)
    dato_linea = np.transpose(dato_linea)

    #Compensadores
    y_comp, barra_bus = impedancia.compensadores(xcomp, barra_comp_i,tipo_comp, vnom_comp, qcomp)
   
#------------------------------------------------- CALCULO DE YBUS, VTH Y ZTH --------------------------------------------------
    #Corrientes inyectadas
    corrientes_inyectadas = impedancia.corrientes(voltaje,phi,imp_gen,num_barras, barra_gen_i)

    #Y bus
    y_bus = ybus.ybus(gen, carga, linea, num_barras,barra_linea_i,barra_linea_j,y_shunt, longitud, barra_bus, y_comp)
    print(y_bus)

    #Z de thevenin
    zth, zbus = ybus.Zth(y_bus)
    #print(zbus)

    #Voltajes de thevenin
    vth,vth_rect = ybus.Vth(zbus,corrientes_inyectadas,num_barras)
   #print(vth)
    
    #GBUS
    g_bus = ybus.gbus(y_bus,num_barras)

    #BBUS
    b_bus = ybus.bbus(y_bus,num_barras)

#------------------------------------------------ COMPENSADORES ------------------------------------------------------------

    check_com1, check_com2 = compensadores.test_compen(vth, v_max, v_min, num_barras, v_nominal)
    #print(check_com1,check_com2)

    #comprobando si se necesita compensar
    verificador = list(filter(lambda x: 'CAP' in x, check_com2))
    verificador2 = list(filter(lambda x: 'IND' in x, check_com2))

    if len(verificador) == 0 and len(verificador2) == 0:
        print("\n  [*] No es necesario compensar, según COVENIN 159")
    else:
        x_comp = compensadores.compensador_pasivo(num_barras,vth,v_min, v_max, zbus, v_nominal)
        print("\n  [*] Se requiere compensación en las barras:")
        for i in range(len(check_com2)):
            print("\t",check_com1[i],"---",check_com2[i])
        print("\n  [*] Se recomiendan los siguientes compensadores: ")
        for i in range(len(x_comp)):
            print("\t",x_comp[i])

#------------------------------------------------ CALCULO DE LAS POTENCIAS ------------------------------------------------

    #Potencia del generador
    p_gen, q_gen= potencia.generador(imp_gen, voltaje, phi, vth_rect, barra_gen_i)
    #print(q_gen)

    #Potencia de la carga
    p_load, q_load  = potencia.Cargas(imp_carga, vth, barra_carga_i)

    #Lineflow (Flujo de potencias)
    p_ij, q_ij, p_ji, q_ji = potencia.lineflow(index_linea, dato_linea, longitud, vth_rect)
    #print(p_ij)
    #print(" ")
    #print(q_ij)

    #Balance de potencias
    delta_p, delta_q = potencia.balance(p_gen, q_gen, p_load, q_load)
    #print(delta_p)
    #print(delta_q)

    #Barra de carga
    etapa = 10
    print("\n  [*] Ya casi terminamos: ")
    with alive_bar(etapa) as bar:
        for i in range(etapa):
            bar()
            time.sleep(1)
    print("\nListo\n")
        

if __name__ == "__main__":
    run()
