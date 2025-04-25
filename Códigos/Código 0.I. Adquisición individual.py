# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:54:17 2025

@author: Usuario
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:14:05 2025

@author: Usuario
"""
import pyvisa
import numpy as np
import os
import time
from datetime import datetime

tiempoi = time.time()

# Configurar conexión con el osciloscopio
rm = pyvisa.ResourceManager()
osc = rm.open_resource("TCPIP0::169.254.211.4::inst0::INSTR")  
osc.timeout = 60000  # Tiempo de espera de 30 segundos


# Configurar parámetros de adquisición
osc.write("TIM:SCAL 1E-5")  # Base de tiempo de 10 ms/div
osc.write("CHAN1:SCAL 1E0")  # Escala de voltaje 1V/div
osc.write("FORM REAL")  # Datos en formato binario
osc.write("CHAN:DATA:POIN 1024")  
osc.write("FORM:BORD LSBF")
# Iniciar adquisición
osc.write("SING")
osc.query("*OPC?")  # Esperar a que termine la adquisición

# Obtener datos
osc.write("CHAN:DATA?")
datos_bin = osc.read_raw()

# Mostrar los primeros 20 bytes para inspeccionar el encabezado
# print("Encabezado de los datos (primeros 20 bytes):")
# print(datos_bin[:20])

# El encabezado tiene la forma #4 (por ejemplo) y se debe saltar
# El primer byte es un '#', el siguiente es el número (4 en este caso)
# Así que saltamos los primeros 4 bytes (1 byte para '#' y 3 bytes para el número)
encabezado_len = 8  # Asumimos que el encabezado ocupa 4 bytes (ajustar si es necesario)
print(datos_bin[:20])
# Saltamos el encabezado (primeros 4 bytes)
datos_bin = datos_bin[encabezado_len:]

print(datos_bin[:20])
# Asegurarnos de que el tamaño de los datos es múltiplo de 4 antes de la conversión
tamano_datos = len(datos_bin)
if tamano_datos % 4 != 0:
    # print(f"Advertencia: El tamaño de los datos no es múltiplo de 4, ajustando tamaño.")
    tamano_valido = tamano_datos - (tamano_datos % 4)  # Redondear al múltiplo de 4 más cercano
    datos_bin = datos_bin[:tamano_valido]

# Verificación antes de convertir
# print(f"Tamaño de los datos binarios después de ajustes: {len(datos_bin)} bytes")

# Convertir los datos binarios a un array de numpy (float32)
try:
    datos = np.frombuffer(datos_bin, dtype=np.float32)
    # print(f"Datos adquiridos: {len(datos)} puntos")
    # print(f"Primeros 5 valores: {datos[:5]}")  # Imprimir los primeros 5 valores para asegurarse de que la conversión fue exitosa
except Exception as e:
    print(f"Error al procesar los datos: {e}")
    datos = np.array([], dtype=np.float32)

# Generar el nombre del archivo con fecha y hora
fecha_hora = datetime.now().strftime("%d_%m_%Y__%H-%M-%S")
carpeta = os.path.join(os.path.expanduser("~"), "Desktop", "Datos_Osciloscopio")
os.makedirs(carpeta, exist_ok=True)
nombre_archivo = os.path.join(carpeta, f"Datos_{fecha_hora}.bin")

# Guardar los datos en formato binario
with open(nombre_archivo, "wb") as f:
    f.write(datos_bin)

tiempof = time.time()
# print(f"Datos guardados en {nombre_archivo}")
print(f'Tardó {tiempof - tiempoi} segundos.')
