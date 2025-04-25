# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 10:43:34 2025

@author: Usuario
"""
# -*- coding: utf-8 -*- 
"""
Created on Wed Mar 12 13:02:17 2025
Modificado para guardar figuras automáticamente en subcarpeta
"""

import os
import struct
import matplotlib.pyplot as plt
import numpy as np

end_time = 500  # Tiempo total en microsegundos

# Directorio de entrada
directory = r'C:/Users/Usuario/Desktop/Datos 20 03 (tormenta cerca)/Datos Serie 15'

# Crear carpeta de salida para figuras
parent_dir = os.path.abspath(directory)
figures_dir_name = os.path.basename(directory) + "_figuras"
figures_path = os.path.join(parent_dir, figures_dir_name)

if not os.path.exists(figures_path):
    os.makedirs(figures_path)

# Constantes
c = 3e8  # Velocidad de la luz (m/s)
Z0 = 50  # Impedancia de carga (ohmios)
eta = 1  # Eficiencia 
Q = 1  # Factor de calidad
R_loss = 0
L = 1  # Longitud (m)

# Modelo de impedancia de antena
def Zin(f, f0):
    R_rad_0 = 73
    X = 50 * (f / f0 - f0 / f)
    R_rad = R_rad_0 * (f / f0)
    return R_rad + R_loss + 1j * X

def resonance_factor(f, f0, Q):
    return 1 / np.sqrt(1 + Q**2 * (f / f0 - f0 / f)**2)

def impedance_match(Zin_f, Z0):
    return np.abs(Z0 / (Zin_f + Z0))

def H_total(f, f0, Q, Z0, eta):
    Zin_f = Zin(f, f0)
    res = resonance_factor(f, f0, Q)
    match = impedance_match(Zin_f, Z0)
    return eta * res * match

# Calcular frecuencia resonante
f0 = c / (2 * L)

# Procesar cada archivo binario
for filename in os.listdir(directory):
    data = []
    file_path = os.path.join(directory, filename)

    if os.path.isfile(file_path):
        print(f"Reading file: {filename}")

        with open(file_path, 'rb') as file:
            while True:
                byte_data = file.read(4)
                if not byte_data:
                    break
                float_value = struct.unpack('f', byte_data)[0]
                data.append(float_value)

    data = np.array(data)
    num_points = len(data)
    t = np.linspace(0, end_time, num_points)
    dt = t[1] - t[0]

    f_teo = 1  # kHz
    seno_teo = np.sin(2 * np.pi * f_teo * t)
    Vo = 2
    alfa = 10.043
    beta = 353.793
    pulsoWF4 = Vo * (np.exp(-alfa * t) - np.exp(-beta * t))

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(f"Análisis de Señal - {filename}", fontsize=14, fontweight="bold")

    axs[0].plot(t, data, color='royalblue', label='Señal Real')
    axs[0].set_xlabel("Tiempo (ms)")
    axs[0].set_ylabel("Voltaje (V)")
    axs[0].set_title("Señal en el tiempo")
    axs[0].legend()
    axs[0].grid(True)

    fft_data = np.fft.fft(data)
    fft_magnitude = np.abs(fft_data) / len(data)
    freqs = np.fft.fftfreq(len(data), d=dt)
    half_range = len(data) // 2
    freqs_positive = freqs[:half_range]
    fft_magnitude_positive = fft_magnitude[:half_range]
    H_f = H_total(freqs_positive, f0, Q, Z0, eta)

    axs[1].semilogy(freqs_positive, fft_magnitude_positive / H_f, color='rosybrown', label='FFT Real')
    axs[1].set_xlabel("Frecuencia (Hz)")
    axs[1].set_ylabel("Magnitud normalizada")
    axs[1].set_title("Espectro de Frecuencia (FFT)")
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    
    # Guardar figura
    filename_clean = os.path.splitext(filename)[0]
    fig_save_path = os.path.join(figures_path, f"{filename_clean}.png")
    fig.savefig(fig_save_path)
    plt.close(fig)  # Cerrar figura para liberar memoria
