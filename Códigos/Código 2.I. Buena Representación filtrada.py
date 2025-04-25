# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 10:58:11 2025

@author: Usuario
"""

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
    freqs = np.fft.fftfreq(len(data), d=dt * 1e-6)  # Convertir dt a segundos
    half_range = len(data) // 2
    freqs_positive = freqs[:half_range]
    fft_magnitude_positive = fft_magnitude[:half_range]

    # -----------------------
    # Aplicar filtro pasabanda (1 MHz - 5 MHz)
    # -----------------------
    f_low = 0  # 10 MHz
    f_high = 100e6  # 100 MHz
    a = 1e2  # Suavidad del filtro
    filtro_pb = filtro_pasabanda_tanh(freqs_positive, f_low, f_high, a)/2

    # Función de transferencia de la antena
    H_f = H_total(freqs_positive, f0, Q, Z0, eta)
    H_f = 1  # CASO TEÓRICO

    # Aplicar filtro
    fft_filtrada_magnitude = (fft_magnitude_positive / H_f) * filtro_pb

    # Reconstrucción de señal en dominio del tiempo
    espectro_filtrado_completo = np.zeros(len(data), dtype=complex)
    espectro_filtrado_completo[:half_range] = fft_data[:half_range] * filtro_pb
    espectro_filtrado_completo[-(len(data)-half_range):] = np.conj(fft_data[1:half_range+1][::-1]) * filtro_pb[::-1]
    señal_filtrada = np.fft.ifft(espectro_filtrado_completo).real

    # -----------------------
    # Gráficas en 2x2
    # -----------------------
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Análisis Señal y Filtro - {filename}", fontsize=14, fontweight="bold")

    # (1,1) Voltaje vs Tiempo
    axs[0, 0].plot(t, data, color='steelblue', label='Señal Original')
    axs[0, 0].set_xlabel("Tiempo (us)")
    axs[0, 0].set_ylabel("Voltaje (V)")
    axs[0, 0].set_title("Señal Original vs Tiempo")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # (1,2) FFT
    axs[0, 1].plot(freqs_positive, fft_magnitude_positive / H_f, color='mediumpurple', label='FFT Original')
    axs[0, 1].set_xlabel("Frecuencia (Hz)")
    axs[0, 1].set_ylabel("Magnitud normalizada")
    axs[0, 1].set_title("Espectro de Frecuencia (FFT)")
    axs[0, 1].legend()
    axs[0, 1].grid(True, which="both")

    # (2,1) IFFT de señal filtrada
    axs[1, 0].plot(t, señal_filtrada, color='steelblue', label='Señal Filtrada')
    axs[1, 0].set_xlabel("Tiempo (us)")
    axs[1, 0].set_ylabel("Voltaje (V)")
    axs[1, 0].set_title("IFFT de Señal Filtrada")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # (2,2) Filtro pasabanda
    axs[1, 1].plot(freqs_positive, filtro_pb, color='darkred', label='Filtro Pasabanda')
    axs[1, 1].set_xlabel("Frecuencia (MHz)")
    axs[1, 1].set_ylabel("Ganancia")
    axs[1, 1].set_title("Respuesta del Filtro Pasabanda")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()
