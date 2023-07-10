import pandas as pd
import numpy as np
import impedancia

#Lectura del archivo excel a trabajar
df_gen = pd.read_excel("data_io.xlsx","GENERATION")                 #Generador
df_lines = pd.read_excel("data_io.xlsx","LINES")                    #Lineas
df_load = pd.read_excel("data_io.xlsx","LOAD")                      #Cargas


#Numero de barras del sistema electrico de potencia
num_barras_i = max(df_lines.iloc[:,1])
num_barras_j = max(df_lines.iloc[:,2])
num_barras = max(num_barras_i,num_barras_j)


#Ordenando los datos del sistemas electrico de potencia(SEP)
#GENERADOR:
imp_resis_gen = np.array(df_gen.iloc[:,4])                          #Impedancia resistiva
imp_react_gen = np.array(df_gen.iloc[:,5])                          #Impedancia reactiva
phi = np.array(df_gen.iloc[:,3])                                    #Angulo fasor voltaje
voltaje = np.array(df_gen.iloc[:,2])                                #Voltaje de la fuente
barra_gen_i = np.array(df_gen.iloc[:,0])                            #Barra de conexion i
barra_gen_j = np.full((len(df_gen.iloc[:,0])),0)                    #Barra de conexion j
index_gen =  np.concatenate(([barra_gen_i],[barra_gen_j]), axis=0)  #Matrix de conexion de lo generadores
index_gen = np.transpose(index_gen) 

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
    imp_gen = impedancia.generador(imp_resis_gen,imp_react_gen)
    imp_carga = impedancia.carga(imp_resis_carga, imp_react_carga, tipo_carga)
    imp_linea, y_shunt = impedancia.linea(imp_resis_linea,imp_react_linea,longitud, b_shunt)
    corrientes_inyectadas = impedancia.corrientes(voltaje,phi,imp_gen)
    print("corrientes inyectadas: ", corrientes_inyectadas)
    print("impedancias generador: ", imp_gen)
    print("impedancias de linea: ", imp_linea)
    print("impedancia de carga: ", imp_carga)

if __name__ == "__main__":
    run()
