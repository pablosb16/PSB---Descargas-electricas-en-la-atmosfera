# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 21:36:42 2025

@author: pablo
"""

import numpy as np
import matplotlib.pyplot as plt

def rigidez_dielec(P_atm, T, P0=1, T0=298, Eb0=3e6):
    """Calcula la rigidez dieléctrica del aire en función de la presión y temperatura."""
    return Eb0 * (P_atm / P0) * (T0 / T)

def presión(T, h, p0=1, g=9.81, M=0.02896968, R=8.31432):
    """Calcula la presión en función de la temperatura y la altitud."""
    T = T + 273.15  # Convertir temperatura a Kelvin
    return p0 * np.exp(-(g * M * h) / (R * T))  # Fórmula de presión barométrica

# Datos de altura (m) y temperatura (°C)
h = np.array([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 
              15000, 20000, 25000, 30000, 40000, 50000, 60000, 70000, 80000])

T = np.array([15.00, 8.50, 2.00, -4.49, -10.98, -17.47, -23.96, -30.45, -36.94, 
              -43.42, -49.90, -56.50, -56.50, -51.60, -46.64, -22.80, -2.5, -26.13, -53.57, -74.51])

P = presión(T, h)  # Calculamos la presión en función de la altitud

# --- GRÁFICO CON DOS EJES X ---
fig, ax1 = plt.subplots(figsize=(8, 6))

# Primer eje X (Temperatura)
ax1.plot(T+273.15, h/1000, label='Temperatura vs Altitud', color='indianred')
ax1.set_xlabel('Temperatura (K)', color='indianred')
ax1.set_ylabel('Altitud (km)')
ax1.tick_params(axis='x', labelcolor='indianred')

# Segundo eje X (Presión)
ax2 = ax1.twiny()  # Creamos un segundo eje X
ax2.plot(P, h/1000, label='Presión vs Altitud', color='royalblue')
ax2.set_xlabel('Presión (atm)', color='royalblue')
ax2.tick_params(axis='x', labelcolor='royalblue')



# Título y leyendas
ax1.set_title('Temperatura y Presión en función de la Altitud')
ax1.grid()
ax1.legend(loc='upper right', bbox_to_anchor=(1, 1))
ax2.legend(loc='upper left', bbox_to_anchor=(0, 1))

plt.show()


# Rango de presiones y temperaturas
P_values = np.linspace(0.1, 2, 50)  # Presión de 0.5 atm a 2 atm
T_values = np.linspace(200, 350, 50)  # Temperatura de 250 K a 350 K

# Matriz de resultados
Eb_matrix = np.array([[rigidez_dielec(P, T) for P in P_values] for T in T_values])

# Graficamos los resultados
plt.figure(figsize=(8,6))
plt.contourf(P_values, T_values, Eb_matrix, cmap='viridis', levels=20)
plt.plot(P,T+273.15, color="ivory", label="Valor Atmosférico")
plt.colorbar(label='Rigidez dieléctrica (V/m)')
plt.xlabel('Presión (atm)')
plt.ylabel('Temperatura (K)')
plt.title('Rigidez Dieléctrica del Aire vs. Presión y Temperatura')
plt.xlim(0.1, 2)
plt.ylim(200, 350)
plt.legend()
plt.show()


rigatm=rigidez_dielec(P,T+273.15)