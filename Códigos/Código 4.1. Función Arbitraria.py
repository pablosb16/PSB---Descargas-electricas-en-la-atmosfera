# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Código para cargar una forma de onda arbitraria en un generador de funciones usando PyVISA.
"""
import pyvisa
import numpy as np
import matplotlib.pyplot as plt

# Dirección del generador de funciones (ajustar si es necesario)
VISA_ADDRESS = 'USB0::0x0957::0x0407::MY44043637::0::INSTR'

# Archivo con la forma de onda
def cargar_datos(file_path):
    y = np.loadtxt(file_path)
    # Normalizar la señal entre 0 y 1
    y = (y - np.min(y)) / (np.max(y) - np.min(y))
    return y

file_path = r'C:\Users\Usuario\Desktop\Código Python Control Osciloscopio\arch_15s de rayos al azar 1.txt'
y = cargar_datos(file_path)
y=np.array([0,0.5,1,0.5,0,-0.5,-1,-0.5,0])
# for i in range (len(y)):
#     if i == 0:
#         str_array = "%.10f" % y[i]
#     else:
#         str_array = str_array + ",%.10f" % y[i]
        
# Reducir el tamaño si es necesario (ajustar según el modelo del generador)

y_str = ",".join(map(lambda val: f"{val:.10f}", y))

# plt.plot(y)
# plt.title("Forma de onda cargada")
# plt.show()


# Conectar con el generador
rm = pyvisa.ResourceManager()
dispositivos = rm.list_resources()

generator = rm.open_resource(VISA_ADDRESS)
generator.timeout = 30000


generator.write("DATA VOLATILE," + y_str)



# generator.write("VOLT 1")  # 1V de amplitud
# generator.write("FREQ 1")  # 10Hz (ajustar según lo necesario)


# Verificar si hubo errores
# error = generator.query("SYST:ERR?")
# print(f"Estado del sistema: {error}")

print("✅ Pulso generado y cargado correctamente.")