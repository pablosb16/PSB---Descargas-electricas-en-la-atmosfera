# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:50:12 2025

@author: Usuario
"""

import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# Constantes Globales
# -----------------------
c = 3e8  # Velocidad de la luz (m/s)
Z0 = 50  # Impedancia de carga (ohmios)
eta = 1  # Eficiencia 
Q = 1  # Factor de calidad (relacionado con ancho de banda)
R_loss = 0  # Pérdidas ohmicas (ohmios), típicas

# -----------------------
# Modelo de Impedancia de Entrada de Antena
# -----------------------
def Zin(f, f0):
    R_rad_0 = 73  # Resistencia de radiación típica para dipolo resonante (ohmios)
    X = 50 * (f / f0 - f0 / f)  # Reactancia aproximada
    R_rad = R_rad_0 * (f / f0)  # Resistencia de radiación dependiente de f
    return R_rad + R_loss + 1j * X  # Impedancia total (compleja)

# -----------------------
# Factor de Resonancia (tipo RLC)
# -----------------------
def resonance_factor(f, f0, Q):
    return 1 / np.sqrt(1 + Q**2 * (f / f0 - f0 / f)**2)

# -----------------------
# Factor de Adaptación de Impedancia
# -----------------------
def impedance_match(Zin_f, Z0):
    return np.abs(Z0 / (Zin_f + Z0))  # Relación de acoplamiento

# -----------------------
# Función de Transferencia Completa
# -----------------------
def H_total(f, f0, Q, Z0, eta):
    Zin_f = Zin(f, f0)
    res = resonance_factor(f, f0, Q)
    match = impedance_match(Zin_f, Z0)
    return eta * res * match

# -----------------------
# Cálculo y Gráfica para varias longitudes
# -----------------------

# Rango de frecuencias
f = np.linspace(1e6, 1.5e9, 20000)  # 1 MHz a 1 GHz, alta resolución

# Longitudes a evaluar
longitudes = [0.5, 1.0, 2.0]  # En metros

# Colores para el gráfico
colores = ['teal', 'dodgerblue', 'mediumslateblue']  

# Crear la figura
plt.figure(figsize=(12, 7))

# Bucle para cada longitud
for idx, L in enumerate(longitudes):
    f0 = c / (2 * L)  # Frecuencia resonante
    H_f = H_total(f, f0, Q, Z0, eta)  # Función de transferencia
    plt.plot(f / 1e6, H_f, label=f'L = {L} m (f₀ ≈ {f0/1e6:.1f} MHz)', linewidth=2, color=colores[idx])


fmaxosci=1.2*10**9
# -----------------------
# Formato bonito de la gráfica
# -----------------------
plt.xlabel('Frecuencia (MHz)', fontsize=14)
plt.ylabel('Amplitud de Transferencia (normalizada)', fontsize=14)
plt.axvline(x=fmaxosci / 1e6, color='darkred', linestyle='--', linewidth=2, label=f'Frecuencia límite del Osciloscopio: {fmaxosci/1e6:.0f} MHz')
plt.title('Comparación de Función de Transferencia para Diferentes Longitudes de Antena', fontsize=16, pad=15)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
