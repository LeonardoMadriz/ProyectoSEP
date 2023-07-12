import pandas as pd
import numpy as np
import impedancia
import ybus
import potencia

#Lectura del archivo excel a trabajar
df_gen = pd.read_excel("data_io.xlsx","GENERATION")                 #Generador
df_lines = pd.read_excel("data_io.xlsx","LINES")                    #Lineas
df_load = pd.read_excel("data_io.xlsx","LOAD")                      #Cargas


#Numero de barras del sistema electrico de potencia
num_barras_i = max(df_lines.iloc[:,0])
num_barras_j = max(df_lines.iloc[:,1])
num_barras = int(max(num_barras_i,num_barras_j))



#----------------------------------------------------- ORDENANDO LOS DATOS LEIDOS --------------------------------------------------------
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

#LINEAS
df_lines.dropna()
imp_resis_linea = np.array(df_lines.iloc[:,5])                      #Impedancia resistiva
imp_react_linea = np.array(df_lines.iloc[:,6])                      #Impedancia reactiva
b_shunt = np.array(df_lines.iloc[:,7])                              #admitancia del efecto capacitivo de las lineas
longitud = np.array(df_lines.iloc[:,4])                             #largo de las lineas
barra_linea_i = np.array(df_lines.iloc[:,0])                        #Barra de conexion i
barra_linea_j = np.array(df_lines.iloc[:,1])                        #Barra de conexion j
index_linea = np.concatenate(([barra_linea_i],[barra_linea_j]))     #Matriz de conexion de las cargas
index_linea = np.transpose(index_linea)



def run():
#---------------------------------------------- CALCULO DE LAS IMPEDANCIAS---------------------------------------------- 
    #Generadores
    imp_gen = impedancia.generador(imp_resis_gen,imp_react_gen)
    gen =  np.concatenate(([barra_gen_i],[barra_gen_j],[imp_gen]), axis=0)
    gen = np.transpose(gen)
    gen = np.round(gen,4)
    
    #Cargas
    imp_carga = impedancia.carga(imp_resis_carga, imp_react_carga, tipo_carga)
    carga = np.concatenate(([barra_carga_i],[barra_carga_j],[imp_carga]),axis=0)
    carga = np.transpose(carga)
    carga = np.round(carga,4)

    #Lineas
    imp_linea, y_shunt = impedancia.linea(imp_resis_linea,imp_react_linea,longitud, b_shunt)
    linea = np.concatenate(([barra_linea_i],[barra_linea_j],[imp_linea]),axis=0)      
    linea = np.transpose(linea)
    linea = np.round(linea,4)
   
#------------------------------------------------- CALCULO DE YBUS, VTH Y ZTH --------------------------------------------------
    #Corrientes inyectadas
    corrientes_inyectadas = impedancia.corrientes(voltaje,phi,imp_gen,num_barras, barra_gen_i)

    #Y bus
    y_bus = ybus.ybus(gen, carga, linea, num_barras,barra_linea_i,barra_linea_j,y_shunt, longitud)

    #Z de thevenin
    zth, zbus = ybus.Zth(y_bus)

    #Voltajes de thevenin
    vth,vth_rect = ybus.Vth(zbus,corrientes_inyectadas,num_barras)
    
    #GBUS
    g_bus = ybus.gbus(y_bus,num_barras)

    #BBUS
    b_bus = ybus.bbus(y_bus,num_barras)

#------------------------------------------------ CALCULO DE LAS POTENCIAS ------------------------------------------------

    #Potencia del generador
    p_gen, q_gen= potencia.generador(imp_gen, voltaje, phi, vth_rect, barra_gen_i)





if __name__ == "__main__":
    run()
