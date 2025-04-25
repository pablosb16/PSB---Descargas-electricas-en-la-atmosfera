# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 10:28:27 2025

@author: Usuario
"""

import os
import struct
import numpy as np
import matplotlib.pyplot as plt

# Directorios
fondo_dir = r'C:\Users\Usuario\Desktop\Medidas fondo'
senal_dir = r'C:\Users\Usuario\Desktop\Representación de datos'

# Función para leer un archivo binario como float32
def leer_archivo_binario(file_path):
    data = []
    with open(file_path, 'rb') as file:
        while True:
            byte_data = file.read(4)
            if not byte_data:
                break
            data.append(struct.unpack('f', byte_data)[0])
    return np.array(data)

# Leer todos los archivos de fondo y calcular la media
fondo_files = [os.path.join(fondo_dir, f) for f in os.listdir(fondo_dir) if os.path.isfile(os.path.join(fondo_dir, f))]
fondo_arrays = [leer_archivo_binario(f) for f in fondo_files]

# Asegurar que todos tienen la misma longitud
min_length = min(len(arr) for arr in fondo_arrays)
fondo_arrays = [arr[:min_length] for arr in fondo_arrays]  # Cortar al tamaño mínimo
fondo_medio = np.mean(fondo_arrays, axis=0)  # Media punto por punto

# Leer y procesar los archivos de señal
for filename in os.listdir(senal_dir):
    file_path = os.path.join(senal_dir, filename)
    if os.path.isfile(file_path):
        print(f"Procesando: {filename}")
        
        # Leer señal y asegurarse de que tenga la misma longitud que el fondo
        data = leer_archivo_binario(file_path)[:min_length]
        
        # Restar el fondo medio
        data_sin_fondo = data - fondo_medio
        
        # Parámetros de tiempo
        end_time = 500 * 10**(-3) * 50  
        t = np.linspace(0, end_time, min_length)
        dt = t[1] - t[0]
        
        # Graficar
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle(f"Señal Filtrada - {filename}", fontsize=14, fontweight="bold")
        
        axs[0].plot(t, data_sin_fondo, color='royalblue', label='Señal sin fondo')
        axs[0].set_xlabel("Tiempo (s)")
        axs[0].set_ylabel("Voltaje (V)")
        axs[0].set_title("Señal en el tiempo")
        axs[0].legend()
        axs[0].grid(True)
        
        # FFT
        fft_data = np.fft.fft(data_sin_fondo)
        fft_magnitude = np.abs(fft_data) / min_length
        freqs = np.fft.fftfreq(min_length, d=dt)
        
        half_range = min_length // 2
        axs[1].semilogy(freqs[:half_range], fft_magnitude[:half_range], color='seagreen', label='FFT Filtrada')
        axs[1].set_xlabel("Frecuencia (Hz)")
        axs[1].set_ylabel("Magnitud normalizada")
        axs[1].set_title("Espectro de Frecuencia (FFT)")
        axs[1].legend()
        axs[1].grid(True)
        
        plt.tight_layout()
        plt.show()