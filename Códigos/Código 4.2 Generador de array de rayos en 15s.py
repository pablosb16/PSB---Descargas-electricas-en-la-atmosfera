###################################################
#                                                 #
#    GENERADOR DE ARCHIVOS CON RAYOS AL AZAR      #
#                                                 #
#    configurado para 15 segundos y 3 rayos       #
#                                                 #
###################################################

import numpy as np
import random
import matplotlib.pyplot as plt

def generar_senal(t, A, alfa, beta):
    numderayos = random.randint(2, 3)  # Al menos 1 rayo
    indices = random.sample(range(len(t) - 300), numderayos)  # Asegura que haya espacio suficiente
    
    y = np.zeros_like(t)
    
    for i in indices:
        fin = i + 300  # Define el rango hasta 300 puntos después de i
        y[i:fin] = A * (np.exp(-alfa * (t[i:fin] - t[i]) * 0.5) - np.exp(-beta * (t[i:fin] - t[i]) * 0.5))
    
    return y

# Parámetros de la señal
A = 200  
alfa = 1 / (10e-6)  # Ajustado para que el pulso decaiga en ~25 µs
beta = 1 / (3.5e-6)  # Ajustado para que tenga la forma esperada

t=np.linspace(0,15,50000)
y=generar_senal(t,A,alfa,beta)
y=y/(max(y)+0.000001)

# Graficar la señal
plt.plot(t, y, label="Señal generada")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.legend()
plt.show()
# Guardar en un archivo de texto para usarlo en otro código
np.savetxt("arch_15s de rayos al azar 1.txt", y)