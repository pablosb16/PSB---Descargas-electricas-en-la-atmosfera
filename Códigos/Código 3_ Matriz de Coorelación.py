# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 11:18:15 2025

@author: Usuario
"""

import os
import struct
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

directory = r'C:\Users\Usuario\Desktop\Datos_Osciloscopio'

def read_binary_file(file_path):
    """Lee un archivo binario y devuelve los valores en una lista."""
    data = []
    try:
        with open(file_path, 'rb') as file:
            while True:
                byte_data = file.read(4)
                if not byte_data:
                    break
                try:
                    float_value = struct.unpack('f', byte_data)[0]
                    data.append(float_value)
                except struct.error:
                    print(f"Error al leer datos en {file_path}, posible archivo corrupto.")
                    return None
    except Exception as e:
        print(f"No se pudo leer {file_path}: {e}")
        return None
    return np.array(data) if data else None

# Leer todos los archivos en la carpeta
data_dict = {}
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        print(f"Leyendo archivo: {filename}")
        data = read_binary_file(file_path)
        if data is not None:
            data_dict[filename] = data

if not data_dict:
    print("No se encontraron datos válidos para procesar.")
    exit()

# Asegurar que todos los arrays tienen la misma longitud recortándolos al mínimo común
def equalize_lengths(data_dict):
    min_length = min(len(arr) for arr in data_dict.values())
    return {key: arr[:min_length] for key, arr in data_dict.items()}

data_dict = equalize_lengths(data_dict)

# Convertir los datos a una matriz
matrix = np.array(list(data_dict.values()))

# Verificar si la matriz tiene suficientes datos para la correlación
if matrix.shape[0] < 2:
    print("No hay suficientes archivos con datos válidos para calcular la correlación.")
    exit()

# Calcular la matriz de correlación
corr_matrix = np.corrcoef(matrix) 

'''
se usa la correlación de Pearson para identificar la relación entre las ondas de los diferentes archivos. 

rho(X,Y)=covarianza(X,Y)/sigma_x·sigma_y (sigma=desviación estandar)
'''

# Graficar la matriz de correlación
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=False, cmap="viridis", xticklabels=data_dict.keys(), yticklabels=data_dict.keys())
plt.xticks(rotation=90, fontsize=8)
plt.yticks(fontsize=8)
plt.title("Matriz de Correlación de Archivos Binarios")
plt.show()

