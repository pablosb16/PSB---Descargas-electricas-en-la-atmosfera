# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 12:54:57 2025

@author: pablo
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Parámetros del pulso ---
E0 = 1.0                  # Amplitud
alpha = 1e6              # Subida (~1 us)
beta = 3.33e6            # Bajada (~30 us)
c = 3e8                  # Velocidad de la luz (m/s)

# Tiempo centrado
t_us = np.linspace(-30, 60, 5000)  # microsegundos
t = t_us * 1e-6                   # segundos
t0 = 10e-6  # Centro del pulso (10 us)

# Campo eléctrico E(t) ideal
E_t = E0 * (np.exp(-alpha * (t - t0)) - np.exp(-beta * (t - t0))) * (t >= t0)

# --- Añadir ruido aleatorio ---
np.random.seed(42)  # Para reproducibilidad
ruido = 0.005 * np.random.normal(0, 1, size=E_t.shape)  # Nivel de ruido (ajustable)
E_t_ruido = E_t + ruido  # Campo con ruido

# Derivada de E(t) (numérica para incluir el ruido)
dE_dt = np.gradient(E_t_ruido, t)

# Campo magnético B(t) y su derivada
B_t = (1 / c) * E_t_ruido
dB_dt = (1 / c) * dE_dt

# --- FFT para espectro ---
N = len(t)
dt = t[1] - t[0]
fs = 1 / dt
f = np.fft.fftshift(np.fft.fftfreq(N, dt))
E_f = np.fft.fftshift(np.fft.fft(E_t_ruido))
mask = f >= 0
f_pos = f[mask]
E_f_pos = E_f[mask]
amplitud = np.abs(E_f_pos)
fase = np.angle(E_f_pos)

# --- Gráfica organizada y bonita ---
fig = plt.figure(figsize=(14, 12))
fig.suptitle('Representación del Pulso Electromagnético con Ruido y su Espectro', fontsize=18, fontweight='bold')

# Primera fila: E(t) y su derivada
ax1 = plt.subplot(3, 2, 1)

ax1.plot(t_us, dE_dt / np.max(np.abs(dE_dt)),  label=r'$\frac{dE}{dt}$ (normalizada)', color='gold',alpha=0.6)
ax1.plot(t_us, E_t_ruido, label=r'$E(t)$ (con ruido)', color='darkorange')

ax1.set_title('Campo Eléctrico $E(t)$ (con ruido) y su Derivada')
ax1.set_xlabel('Tiempo (μs)')
ax1.set_ylabel('Amplitud (u.a.)')
ax1.legend(loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.6)

# Primera fila: B(t) y su derivada
ax2 = plt.subplot(3, 2, 2)

ax2.plot(t_us, dB_dt / np.max(np.abs(dB_dt)), label=r'$\frac{dB}{dt}$ (normalizada)', color='darkgreen', alpha=0.6)
ax2.plot(t_us,0.3* B_t / np.max(np.abs(B_t)), label=r'$B(t)$ (normalizado)', color='darkgreen')

ax2.set_title('Campo Magnético $B(t)$ y su Derivada')
ax2.set_xlabel('Tiempo (μs)')
ax2.set_ylabel('Amplitud (u.a.)')
ax2.legend(loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.6)

# Segunda fila: Espectro de amplitud
ax3 = plt.subplot(3, 1, 2)
ax3.plot(f_pos / 1e6, amplitud / np.max(amplitud), color='purple')
ax3.set_title('Espectro de Amplitud (Frecuencias Positivas)')
ax3.set_xlabel('Frecuencia (MHz)')
ax3.set_ylabel('Amplitud (normalizada)')
ax3.grid(True, linestyle='--', alpha=0.6)

# Tercera fila: Fase del espectro
ax4 = plt.subplot(3, 1, 3)
ax4.plot(f_pos / 1e6, fase, color='brown')
ax4.set_title('Fase del Espectro (Frecuencias Positivas)')
ax4.set_xlabel('Frecuencia (MHz)')
ax4.set_ylabel('Fase (rad)')
ax4.grid(True, linestyle='--', alpha=0.6)

# Ajuste final de espacios
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Espacio para título global
plt.show()
