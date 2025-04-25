##################################################
#                                                #
#        CARGA DE ONDA ARBITRARIA EN PYVISA      #
#                                                #
#       Generación y envío de señales custom     #
#         a un generador de funciones            #
#                                                #
##################################################


import pyvisa
import numpy as np


def cargar_datos(file_path):
    y = np.loadtxt(file_path)
    # Normalizar la señal entre 0 y 1
    y = (y - np.min(y)) / (np.max(y) - np.min(y))
    return y

file_path = r'C:/Users/Usuario/Desktop/Lectura de Rayos con Osciloscopio/Código Python Control Osciloscopio/arch_15s de rayos al azar 1.txt'
y = cargar_datos(file_path)



# Dirección del generador de funciones
VISA_ADDRESS = 'USB0::0x0957::0x0407::MY44043637::0::INSTR'

# Crear una onda de prueba
#y = np.array([0, 0.5, 1, 0.5, 0, -0.5, -1, -0.5, 0,1,1])

# Convertir la onda en un string SCPI válido
y_str = ",".join(f"{val:.10f}" for val in y)

# Conectar con el generador
rm = pyvisa.ResourceManager()
generator = rm.open_resource(VISA_ADDRESS)
generator.timeout = 30000

# Cargar la forma de onda en memoria
generator.write("*CLS")  # Limpiar errores previos
generator.write("DATA VOLATILE," + y_str)  # Enviar datos
generator.write("FUNC:USER VOLATILE")  # Seleccionar la memoria cargada

# Configurar salida
generator.write("VOLT 1")  # Ajustar voltaje
generator.write("FREQ 0.1")  # Ajustar frecuencia
generator.write("OUTP ON")  # Activar la salida

# Verificar errores
error = generator.query("SYST:ERR?")
print(f"Estado del sistema: {error}")

print(" Pulso generado y cargado correctamente.")
