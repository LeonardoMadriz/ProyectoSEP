import numpy as np

#---------------------------------VERIFICACION DE LAS BARRAS QUE NECESITAN COMPENSACION---------------------------------
def test_compen(vth, vmax, vmin,num_barras, v_nom):
    filas_vth, columna_vth = vth.shape
    mensaje = []
    tipo_com = []
    for i in range(filas_vth):
        if vth[i,0] > vmax:
            mensaje.append(f"Barra: [{i+1}]")
            tipo_com.append("IND")
        elif vth[i,0] < vmin:
            mensaje.append(f"Barra: [{i+1}]")
            tipo_com.append("CAP")
        else:
            mensaje.append(f"Barra: [{i+1}]")
            tipo_com.append("X")

    #------------------------------CALCULO DE LA BARRA CON LA PEOR CONDICION--------------------------------------------
    distancia=[]
    for i in range(num_barras):
        distancia.append(abs(vth[i,0] - v_nom))

    return mensaje,tipo_com

#---------------------------------------OBTENIENDO VALORES DE LOS COMPENSADORES-----------------------------------------
def compensador_pasivo(num_barras, vth, vmin, vmax,zbus,v_nom):
    xcomp = np.zeros((num_barras,1),dtype="complex_")
    qcomp = np.zeros((num_barras,1),dtype="complex_")
    for k in range(num_barras):
        if vth[k,0] < vmin or vth[k,0] > vmax:
        #obtencion de los datos de Vth, Zth, Vnominal y Xth para montar la ecuacion cuadratica
            xth = zbus[k,k].imag
            zth_mod = abs(zbus[k,k])
            vth_mod = vth[k,0]

        #Construimos la ecuacion cuadratica
            a = zth_mod**2
            b = 2*xth*v_nom**2
            c = v_nom**4-((v_nom**2)*vth_mod**2)
            coeficientes = [a,b,c]
            raices = np.roots(coeficientes)
            qcomp[k,0]=max(raices)

        #Calculamos la reactancia de compensacion
            xcomp[k,0]=v_nom**2/qcomp[k]
            return xcomp