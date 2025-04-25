# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:39:47 2025

@author: Usuario
"""

import os
import struct
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# Ruta base donde están las carpetas de las series
base_directory = r'C:/Users/Usuario/Desktop/Datos pre semana santa (muy tormentoso desde cangas al noreste)'
# Carpeta donde se guardarán las figuras de correlación
output_directory = os.path.join(base_directory, 'Correlaciones')

# Crear carpeta de salida si no existe
os.makedirs(output_directory, exist_ok=True)

def read_binary_file(file_path):
    """Lee un archivo binario y devuelve los valores en una lista."""
    data = []
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"Advertencia: El archivo {file_path} está vacío.")
            return None

        with open(file_path, 'rb') as file:
            while True:
                byte_data = file.read(4)
                if not byte_data:
                    break
                if len(byte_data) != 4:
                    print(f"Error: Archivo {file_path} tiene datos incompletos.")
                    return None
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

def equalize_lengths(data_dict):
    """Recorta todos los arrays al tamaño del menor."""
    min_length = min(len(arr) for arr in data_dict.values())
    return {key: arr[:min_length] for key, arr in data_dict.items()}

# Buscar todas las carpetas que empiecen con "Datos13.03 Serie"
series_folders = [f for f in os.listdir(base_directory) if f.startswith("Datos Serie") and os.path.isdir(os.path.join(base_directory, f))]

if not series_folders:
    print("No se encontraron carpetas de series para procesar.")
    sys.exit(1)

print(f"Se encontraron las siguientes series: {series_folders}")

# Procesar cada carpeta de serie
for serie_folder in series_folders:
    serie_path = os.path.join(base_directory, serie_folder)
    print(f"\nProcesando: {serie_folder}")

    # Leer todos los archivos en la carpeta de la serie
    data_dict = {}
    for filename in os.listdir(serie_path):
        file_path = os.path.join(serie_path, filename)
        if os.path.isfile(file_path):
            print(f"  Leyendo archivo: {filename}, tamaño: {os.path.getsize(file_path)} bytes")
            data = read_binary_file(file_path)
            if data is not None:
                data_dict[filename] = data

    if not data_dict:
        print(f"No se encontraron datos válidos en {serie_folder}, se omite esta serie.")
        continue

    # Igualar las longitudes de los datos
    data_dict = equalize_lengths(data_dict)

    # Aplicar Transformada de Fourier
    fft_dict = {key: np.abs(np.fft.fft(arr))[:len(arr)//2] for key, arr in data_dict.items()}

    # Igualar las longitudes de las FFT
    min_fft_length = min(len(arr) for arr in fft_dict.values())
    fft_dict = {key: arr[:min_fft_length] for key, arr in fft_dict.items()}

    # Convertir a matriz
    matrix = np.array(list(fft_dict.values()))
    print(f"  Dimensión de la matriz FFT: {matrix.shape}, Memoria: {matrix.nbytes / 1e6:.2f} MB")

    if matrix.shape[0] < 2:
        print(f"No hay suficientes archivos en {serie_folder} para calcular la correlación, se omite.")
        continue

    # Calcular la matriz de correlación
    corr_matrix = np.corrcoef(matrix)

    # Preparar las etiquetas de los archivos
    archivos_lista = list(fft_dict.keys())

    # Definir posiciones específicas (ajustadas al número real de archivos)
    posiciones = [0, 127, 255, 383, 511]  # Equivalen a 1, 128, 256, 384, 512 (índices desde 0)
    posiciones_validas = [p for p in posiciones if p < len(archivos_lista)]  # Solo las que existan

    # Generar etiquetas solo en esas posiciones
    etiquetas = [archivos_lista[p] for p in posiciones_validas]

    # -----------------------------
    # Graficar la matriz de correlación con escala absoluta
    # -----------------------------
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=False,
        cmap="Spectral",  # Puedes cambiarlo por "coolwarm", "viridis", etc.

        xticklabels=False,
        yticklabels=False
    )

    # Poner solo las etiquetas deseadas en los ejes
    plt.xticks(
        ticks=posiciones_validas,
        labels=etiquetas,
        rotation=90,
        fontsize=8
    )
    plt.yticks(
        ticks=posiciones_validas,
        labels=etiquetas,
        fontsize=8
    )

    plt.title(f"Matriz de Correlación de Frecuencias\n{serie_folder}")

    # Guardar figura
    output_path = os.path.join(output_directory, f'correlacion_{serie_folder}.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Gráfico guardado en: {output_path}")

print("\n✅ Procesamiento completado de todas las series.")

