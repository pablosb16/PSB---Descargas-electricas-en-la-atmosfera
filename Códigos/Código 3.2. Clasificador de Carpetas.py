# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:24:23 2025

@author: Usuario
"""

import os
import shutil
import math

# Ruta donde están los archivos originales
ruta_origen = r'C:/Users/Usuario/Desktop/Datos_Osciloscopio'

# Ruta base para las carpetas destino
ruta_destino_base = r'C:/Users/Usuario/Desktop/Datos pre semana santa (muy tormentoso desde cangas al noreste)'

# Número de archivos por carpeta
archivos_por_carpeta = 512

# Prefijo de nombre para las nuevas carpetas
prefijo_carpeta = 'Datos Serie'

# Listar todos los archivos en la carpeta origen
archivos = [f for f in os.listdir(ruta_origen) if os.path.isfile(os.path.join(ruta_origen, f))]

# Ordenar archivos por nombre (opcional, para mantener orden)
archivos.sort()

# Calcular cuántas carpetas se necesitan
num_carpetas = math.ceil(len(archivos) / archivos_por_carpeta)

print(f'Se organizarán {len(archivos)} archivos en {num_carpetas} carpetas de hasta {archivos_por_carpeta} archivos cada una.')

# Crear carpetas y mover archivos
for i in range(num_carpetas):
    # Definir nombre y ruta de la carpeta actual
    nombre_carpeta = f'{prefijo_carpeta} {i + 1}'
    ruta_carpeta = os.path.join(ruta_destino_base, nombre_carpeta)

    # Crear la carpeta si no existe
    os.makedirs(ruta_carpeta, exist_ok=True)
    print(f'Creando carpeta: {ruta_carpeta}')

    # Seleccionar archivos para esta carpeta
    inicio = i * archivos_por_carpeta
    fin = inicio + archivos_por_carpeta
    archivos_grupo = archivos[inicio:fin]

    # Mover archivos
    for archivo in archivos_grupo:
        ruta_archivo_origen = os.path.join(ruta_origen, archivo)
        ruta_archivo_destino = os.path.join(ruta_carpeta, archivo)
        shutil.move(ruta_archivo_origen, ruta_archivo_destino)
        print(f'Movido: {archivo} --> {nombre_carpeta}')

print('¡Archivos organizados correctamente!')
