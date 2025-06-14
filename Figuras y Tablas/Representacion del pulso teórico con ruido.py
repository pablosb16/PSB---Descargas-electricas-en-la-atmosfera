# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 12:54:57 2025

@author: pablo
"""

import os
import struct
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# -----------------------
# PARÁMETROS
# -----------------------
end_time = 500  # Tiempo total en microsegundos
directory = r'C:/Users/Usuario/Desktop/Datos/Datos 20 03 (Tormenta Peña Ubiña)/Arch bin de los rayos'

# -----------------------
# CONSTANTES
# -----------------------
c = 3e8
Z0 = 50
eta = 1
Q = 1
R_loss = 0
L = 1

# -----------------------
# FUNCIONES AUXILIARES
# -----------------------

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

def exp_decay(f, a, b):
    return a * np.exp(-b * f)

# -----------------------
# CARGAR DATOS
# -----------------------

all_data = []
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path) and filename.endswith('.bin'):
        print(f"Leyendo archivo: {filename}")
        data = []
        with open(file_path, 'rb') as file:
            while True:
                byte_data = file.read(4)
                if not byte_data:
                    break
                float_value = struct.unpack('f', byte_data)[0]
                data.append(float_value)
        all_data.append(np.array(data))

if not all_data:
    raise ValueError("No se encontraron archivos de datos.")
min_length = min(len(d) for d in all_data)
all_data = [d[:min_length] for d in all_data]
all_data_array = np.vstack(all_data)
mean_signal = np.mean(all_data_array, axis=0)

# -----------------------
# CARGAR REFERENCIA
# -----------------------

all_data2 = []
directory2 = r'C:/Users/Usuario/Desktop/Datos/Archivo datos referencia'
for filename in os.listdir(directory2):
    file_path = os.path.join(directory2, filename)
    if os.path.isfile(file_path) and filename.endswith('.bin'):
        print(f"Leyendo archivo de referencia: {filename}")
        data = []
        with open(file_path, 'rb') as file:
            while True:
                byte_data = file.read(4)
                if not byte_data:
                    break
                float_value = struct.unpack('f', byte_data)[0]
                data.append(float_value)
        all_data2.append(np.array(data))

if not all_data2:
    raise ValueError("No se encontraron archivos de datos de referencia.")
min_length2 = min(len(d) for d in all_data2)
all_data2 = [d[:min_length2] for d in all_data2]
all_data_array2 = np.vstack(all_data2)
mean_signal_ref = np.mean(all_data_array2, axis=0)

# -----------------------
# FFT
# -----------------------

num_points = len(mean_signal)
t = np.linspace(0, end_time, num_points)
dt = t[1] - t[0]
fft_data = np.fft.fft(mean_signal)
fft_magnitude = np.abs(fft_data) / num_points
freqs = np.fft.fftfreq(num_points, d=dt)
half = num_points // 2
freqs_positive = freqs[:half]
fft_magnitude_positive = fft_magnitude[:half]
f0 = c / (2 * L)
H_f = H_total(freqs_positive, f0, Q, Z0, eta)
fft_corrected = fft_magnitude_positive / H_f

# FFT referencia
num_points2 = len(mean_signal_ref)
t2 = np.linspace(0, end_time, num_points2)
dt2 = t2[1] - t2[0]
fft_data2 = np.fft.fft(mean_signal_ref)
fft_magnitude2 = np.abs(fft_data2) / num_points2
freqs2 = np.fft.fftfreq(num_points2, d=dt2)
half2 = num_points2 // 2
freqs_positive2 = freqs2[:half2]
fft_magnitude_positive2 = fft_magnitude2[:half2]
H_f2 = H_total(freqs_positive2, f0, Q, Z0, eta)
fft_corrected2 = fft_magnitude_positive2 / H_f2

# Ajuste exponencial
mask = (freqs_positive > 0) & (fft_corrected > 0)
popt, pcov = curve_fit(exp_decay, freqs_positive[mask], fft_corrected[mask], p0=(1e17, 0.2))
a_fit, b_fit = popt
print(f"Ajuste exponencial: a = {a_fit:.3e}, b = {b_fit:.3e}")

# -----------------------
# FIGURA 1: Señal y FFT
# -----------------------

plt.figure(figsize=(12, 6),  facecolor='#d7d8ff')
plt.suptitle('Análisis de la FFT en Eventos con Rayos y Resonancia Schumann', fontsize=20, fontweight='bold')

plt.subplot(1, 2, 1)
plt.plot(t, mean_signal, color='royalblue', label='Media de eventos')
plt.xlabel('Tiempo (μs)', fontsize=14)
plt.ylabel('Voltaje (V)', fontsize=14)
plt.title('Señal Media en el Tiempo', fontsize=16)
plt.grid()
plt.legend(fontsize=12)

plt.subplot(1, 2, 2)
frequencies_schumann = np.array([7.83, 14.3, 20.8, 27.3, 33.8, 40.3, 46.3, 52.8, 59.3, 65.8])
colors = plt.cm.tab10(np.linspace(0, 1, len(frequencies_schumann)))
for i, freq in enumerate(frequencies_schumann):
    plt.axvline(freq, ymin=0, ymax=1e17, color=colors[i], linestyle='--', alpha=0.7, label=f'Resonancia {i+1}: {freq:.1f} Hz')
plt.semilogy(freqs_positive, fft_corrected, label='FFT corregida', color='rosybrown')
plt.xlabel('Frecuencia (Hz)', fontsize=14)
plt.ylabel('Magnitud', fontsize=14)
plt.title('FFT de la Señal Media', fontsize=16)
plt.grid()
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()


# -----------------------
# FIGURA 1: Señal y FFT
# -----------------------

plt.figure(figsize=(12, 6),  facecolor='#d7d8ff')
plt.suptitle('Análisis de la FFT en Eventos sin Rayos', fontsize=20, fontweight='bold')

plt.subplot(1, 2, 1)
plt.plot(t, mean_signal, color='royalblue', label='Media de eventos sin rayos')
plt.xlabel('Tiempo (μs)', fontsize=14)
plt.ylabel('Voltaje (V)', fontsize=14)
plt.title('Señal Media en el Tiempo', fontsize=16)
plt.grid()
plt.legend(fontsize=12)

plt.subplot(1, 2, 2)
frequencies_schumann = np.array([7.83, 14.3, 20.8, 27.3, 33.8, 40.3, 46.3, 52.8, 59.3, 65.8])
colors = plt.cm.tab10(np.linspace(0, 1, len(frequencies_schumann)))

plt.semilogy(freqs_positive2, fft_corrected2, label='FFT corregida', color='rosybrown')
plt.xlabel('Frecuencia (Hz)', fontsize=14)
plt.ylabel('Magnitud', fontsize=14)
plt.title('FFT de la Señal Media', fontsize=16)
plt.grid()
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()

# -----------------------
# FIGURA 2: Diferencia
# -----------------------

min_len = min(len(freqs_positive), len(freqs_positive2))
freqs_common = freqs_positive[:min_len]
fft_diff = fft_corrected[:min_len] / fft_corrected2[:min_len]

plt.figure(figsize=(12, 6),  facecolor='#d7d8ff')
plt.suptitle('Diferencia entre Tormenta y Referencia', fontsize=20, fontweight='bold')
plt.title('FFT: Diferencia entre Tormenta y Referencia', fontsize=16)
plt.plot(freqs_common, np.abs(fft_diff), label='Diferencia FFT', color='rosybrown')

frequencies_schumann = np.array([
    7.83, 14.3, 20.8, 27.3, 33.8, 40.3, 46.7, 53.2,
    59.7, 66.2, 72.7, 79.2, 85.7, 92.2, 98.7, 105.2,
    111.7, 118.2
])
colors = plt.cm.tab20(np.linspace(0, 1, len(frequencies_schumann)))
for i, freq in enumerate(frequencies_schumann):
    plt.axvline(x=freq, color=colors[i], linestyle='--', alpha=0.8)


plt.xlabel('Frecuencia (Hz)', fontsize=14)
plt.ylabel('Magnitud (u.a.)', fontsize=14)
plt.grid()
plt.legend(ncol=2, fontsize=10)
plt.tight_layout()
plt.show()
