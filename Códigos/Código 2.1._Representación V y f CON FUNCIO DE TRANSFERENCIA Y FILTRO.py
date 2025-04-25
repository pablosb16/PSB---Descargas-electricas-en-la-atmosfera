# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 11:34:15 2025

@author: Usuario
"""

##################################################
#                                                #
#   REPRESENTAR VOLTAJE Y FRECUENCIA CON FILTRO  #
#  PASABANDA TANH DIF Y SEÑAL FILTRADA EN TIEMPO #
##################################################

import os
import struct
import matplotlib.pyplot as plt
import numpy as np

end_time = 500  # Tiempo total en microsegundos

# Directorio
directory = r'C:/Users/Usuario/Desktop/analizar fercuencias'

# -----------------------
# Constantes Globales
# -----------------------
c = 3e8  # Velocidad de la luz (m/s)
Z0 = 50  # Impedancia de carga (ohmios)
eta = 1  # Eficiencia 
Q = 1  # Factor de calidad
R_loss = 0  # Pérdidas ohmicas
L = 1  # Longitud (m)

# -----------------------
# Modelo de Impedancia de Entrada de Antena
# -----------------------
def Zin(f, f0):
    R_rad_0 = 73
    X = 50 * (f / f0 - f0 / f)
    R_rad = R_rad_0 * (f / f0)
    return R_rad + R_loss + 1j * X

# -----------------------
# Factor de Resonancia
# -----------------------
def resonance_factor(f, f0, Q):
    return 1 / np.sqrt(1 + Q**2 * (f / f0 - f0 / f)**2)

# -----------------------
# Adaptación de Impedancia
# -----------------------
def impedance_match(Zin_f, Z0):
    return np.abs(Z0 / (Zin_f + Z0))

# -----------------------
# Función de Transferencia Completa
# -----------------------
def H_total(f, f0, Q, Z0, eta):
    Zin_f = Zin(f, f0)
    res = resonance_factor(f, f0, Q)
    match = impedance_match(Zin_f, Z0)
    return eta * res * match

# -----------------------
# Filtro Pasabanda basado en diferencia de tanh
# -----------------------
def filtro_pasabanda_tanh(f, f_low, f_high, a=1e6):  # Suavidad ajustada a MHz
    return np.tanh((f - f_low) / a) - np.tanh((f - f_high) / a)

# -----------------------
# Cálculo y Gráfica
# -----------------------

f0 = c / (2 * L)  # Frecuencia resonante

# Listar todos los archivos
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
    t = np.linspace(0, end_time, num_points)  # Tiempo en microsegundos
    dt = t[1] - t[0]

    # -----------------------
    # FFT de la señal
    # -----------------------
    fft_data = np.fft.fft(data)
    fft_magnitude = np.abs(fft_data) / len(data)
    freqs = np.fft.fftfreq(len(data), d=dt * 1e-6)  # Convertir dt a segundos (porque está en us)
    
    # Frecuencias positivas
    half_range = len(data) // 2
    freqs_positive = freqs[:half_range]
    fft_magnitude_positive = fft_magnitude[:half_range]

    # -----------------------
    # Aplicar filtro pasabanda (1 MHz - 5 MHz)
    # -----------------------
    f_low = 10e6  # 1 MHz
    f_high = 100e6  # 5 MHz
    a = 1e2  # Suavidad del filtro (ajustada para MHz)
    filtro_pb = filtro_pasabanda_tanh(freqs_positive, f_low, f_high, a)

    # Función de transferencia de la antena
    H_f = H_total(freqs_positive, f0, Q, Z0, eta)
    
    H_f=1 #CASO TEÓRICO
    # Aplicar filtro y corregir función de transferencia
    fft_filtrada_magnitude = (fft_magnitude_positive / H_f) * filtro_pb

    # -----------------------
    # Reconstrucción de la señal filtrada en tiempo
    # -----------------------

    # Crear espectro completo con filtro aplicado (considerando simetría hermítica)
    espectro_filtrado_completo = np.zeros(len(data), dtype=complex)
    espectro_filtrado_completo[:half_range] = fft_data[:half_range] * filtro_pb  # Parte positiva con filtro
    
    # Simetría hermítica (reconstrucción parte negativa)
    espectro_filtrado_completo[-(len(data)-half_range):] = np.conj(fft_data[1:half_range+1][::-1]) * filtro_pb[::-1]

    # Transformada Inversa para obtener señal filtrada
    señal_filtrada = np.fft.ifft(espectro_filtrado_completo).real  # Tomar solo la parte real

    # -----------------------
    # Gráficas
    # -----------------------
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"Análisis Señal y Filtro (1-5 MHz) - {filename}", fontsize=14, fontweight="bold")

    # Señal original y filtrada en el dominio del tiempo
    axs[0].plot(t, data, color='steelblue', label='Señal Original')
    # axs[0].plot(t, señal_filtrada, color='coral', label='Señal Filtrada')
    axs[0].set_xlabel("Tiempo (us)")
    axs[0].set_ylabel("Voltaje (V)")
    axs[0].set_title("Señal Original vs Filtrada")
    axs[0].legend()
    axs[0].grid(True)

    # Dominio de la frecuencia - Original vs Filtrada
    axs[1].semilogy(freqs_positive, fft_magnitude_positive / H_f, color='steelblue', label='FFT Original')  # Escala en MHz
    # axs[1].plot(freqs_positive, fft_filtrada_magnitude, color='coral', label='FFT Filtrada')
    axs[1].set_xscale("log")  # Escala logarítmica en el eje X
    axs[1].set_xlabel("Frecuencia (Hz)")
    axs[1].set_ylabel("Magnitud normalizada")
    axs[1].set_title("Espectro de Frecuencia (FFT)")
    axs[1].legend()
    axs[1].grid(True, which="both")  # Cuadrícula en ambas escalas


    # Gráfica del filtro pasabanda
    axs[2].plot(freqs_positive, filtro_pb, color='mediumpurple', label='Filtro Pasabanda')
    axs[2].set_xlabel("Frecuencia (Hz)")
    axs[2].set_ylabel("Ganancia")
    axs[2].set_title("Respuesta del Filtro Pasabanda")
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()
