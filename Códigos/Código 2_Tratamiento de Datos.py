# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:46:00 2025

@author: Usuario
"""

import os
import struct
import matplotlib.pyplot as plt
import numpy as np

# Directory path
directory = r'C:\Users\Usuario\Desktop\Datos_Osciloscopio'

# Array to store the float data from all files
data = []

# List all files in the directory
for filename in os.listdir(directory):
    # Create full file path
    file_path = os.path.join(directory, filename)

    # Ensure we only process files (not directories)
    if os.path.isfile(file_path):
        print(f"Reading file: {filename}")

        # Open the binary file in read mode
        with open(file_path, 'rb') as file:
            while True:
                # Read 4 bytes at a time (32 bits)
                byte_data = file.read(4)
                if not byte_data:
                    break  # End of file

                # Unpack the bytes as a 32-bit signed float (IEEE 754)
                float_value = struct.unpack('f', byte_data)[0]

                # Append the value to the data list
                data.append(float_value)
                
    
    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(data)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (V)")
    plt.title("Representación de: " + str(filename))
    # plt.legend()
    plt.grid(True)
    plt.show()
    
    dt = 0.0001  # Período de muestreo
    sample_rate = 1 / dt  # Frecuencia de muestreo
    # t = np.arange(0, 131000 * dt, dt)  # Eje de tiempo
    
    # Graficar en subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(f"Análisis de Señal - {filename}", fontsize=14, fontweight="bold")
    # Señal en el dominio del tiempo
    axs[0].plot( data, color='royalblue')
    axs[0].set_xlabel("Tiempo (s)")
    axs[0].set_ylabel("Voltaje (V)")
    axs[0].set_title("Señal en el tiempo")
    axs[0].grid(True)
    
    
    
    # # Calcular la FFT
    fft_data = np.fft.fft(data)
    fft_magnitude = np.abs(fft_data) / len(data)  # Normalización
    freqs = np.fft.fftfreq(len(data), d=dt)


    # # Espectro de Frecuencia (FFT)
    axs[1].plot(freqs, fft_magnitude, color='seagreen')
    axs[1].set_xlabel("Frecuencia (Hz)")
    axs[1].set_ylabel("Magnitud normalizada")
    axs[1].set_title("Espectro de Frecuencia (FFT)")
    axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()
    