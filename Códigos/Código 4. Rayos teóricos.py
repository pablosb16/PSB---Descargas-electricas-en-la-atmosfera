# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 10:47:10 2025

@author: Usuario
"""

import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

def rayo(t, A, alfa, beta):
    R = A * (np.exp(-alfa * t) - np.exp(-beta * t))
    return R / max(R)

# Parámetros
t_max = 50e-6  # 50 µs
n_puntos = 1000
t = np.linspace(0, t_max, n_puntos)  # Vector de tiempo en segundos

A = 8  
alfa = 1 / (10e-6)  # Decaimiento
beta = 1 / (2.5e-6)  # Subida

# Pulso limpio
raayo = rayo(t, A, alfa, beta)

# Añadir ruido aleatorio uniforme de ±500 mV
ruido = np.random.uniform(-0.01, 0.1, size=n_puntos)  # Rango de -0.5 V a 0.5 V
raayo_con_ruido = raayo + ruido

# Transformada de Fourier de la señal con ruido
fft_raayo = np.fft.fft(raayo_con_ruido)
freqs = np.fft.fftfreq(n_puntos, d=t[1] - t[0])  # Vector de frecuencias
fft_raayo_magnitude = np.abs(fft_raayo) / max(np.abs(fft_raayo))  # Normalizado

# Solo parte positiva de la frecuencia
pos_mask = freqs >= 0
freqs_pos = freqs[pos_mask] / 1e6  # Convertir a MHz
fft_raayo_magnitude_pos = fft_raayo_magnitude[pos_mask]

# Crear subplots
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Pulso en el tiempo (con ruido)
axs[0].plot(t * 1e6, raayo_con_ruido, color="b", linewidth=1.5, label="Pulso WF4 con ruido")
axs[0].set_xlabel("Tiempo (µs)")
axs[0].set_ylabel("Amplitud (V)")
axs[0].set_title("Pulso de tipo WF4 + Ruido (±100 mV)")
axs[0].grid(True, linestyle="--", alpha=0.6)
axs[0].legend()

# Transformada de Fourier (Espectro)
axs[1].plot(freqs_pos, fft_raayo_magnitude_pos, color="r", linewidth=2, label="FFT del pulso con ruido")
axs[1].set_xlabel("Frecuencia (MHz)")
axs[1].set_ylabel("Magnitud normalizada")
axs[1].set_title("Transformada de Fourier (con ruido)")
axs[1].grid(True, linestyle="--", alpha=0.6)
axs[1].legend()

plt.tight_layout()
plt.show()







