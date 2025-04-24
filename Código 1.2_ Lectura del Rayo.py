# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 11:36:14 2025

@author: Usuario
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 17:53:10 2025

@author: Usuario
"""
import pyvisa
import numpy as np
import os
import time
from datetime import datetime

# Configurar conexión con el osciloscopio
rm = pyvisa.ResourceManager()
osc = rm.open_resource("USB0::0x0AAD::0x01D6::106638::0::INSTR")  
osc.timeout = 30000  

# Configurar parámetros del osciloscopio
osc.write("*RST")  
osc.write("TIM:SCAL 2E-5")  # 1 µs/div para capturar el pulso del rayo
osc.write("CHAN1:SCAL 70E-3")  # 50 mV/div, ajusta según la señal
osc.write("FORM REAL")  
osc.write("CHAN:DATA:POIN 1024")  
osc.write("FORM:BORD LSBF")
# Configurar trigger para capturar rayos
osc.write("TRIG:SOUR CHAN1")  # Usa el canal 1 como fuente de trigger
osc.write("TRIG:LEV 600E-3")  # Dispara cuando la señal supere
osc.write("TRIG:EDGE:SLOP POS")  # Detectar pulsos positivos (ajustable)
osc.write("TRIG:MODE NORM")  

# Crear carpeta para guardar los datos
carpeta = os.path.join(os.path.expanduser("~"), "Desktop", "Datos_Rayos")
os.makedirs(carpeta, exist_ok=True)

# Monitorear por varias horas
tiempo_inicio = time.time()
tiempo_maximo =60  # 10 horas en segundos

while time.time() - tiempo_inicio < tiempo_maximo:
    print("Esperando un evento de rayo...")
    
    # Iniciar adquisición y esperar el evento
    osc.write("SING")
    osc.query("*OPC?")
    
    # Obtener los datos del canal
    osc.write("CHAN:DATA?")
    datos_bin = osc.read_raw()

    # Procesar el encabezado si existe
    # Muchos osciloscopios envían datos con formato: b'#<n><numero_de_bytes><datos>'
    if datos_bin.startswith(b'#'):
        # El segundo byte indica cuántos dígitos tiene el número de bytes
        num_digits = int(datos_bin[1:2])
        header_len = 2 + num_digits  # '#' + dígito + dígitos que indican el tamaño
    else:
        header_len = 0

    datos_bin = datos_bin[header_len:]  # Eliminamos el encabezado

    # Ajustar el buffer para que sea múltiplo de 4 bytes
    tamano_datos = len(datos_bin)
    if tamano_datos % 4 != 0:
        tamano_valido = tamano_datos - (tamano_datos % 4)
        datos_bin = datos_bin[:tamano_valido]

    # Convertir los datos binarios a un array numpy de float32
    try:
        datos = np.frombuffer(datos_bin, dtype=np.float32)
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        datos = np.array([], dtype=np.float32)
    
    # (Opcional) Puedes representar o procesar 'datos' aquí

    # Guardar los datos en un archivo con marca de tiempo
    fecha_hora = datetime.now().strftime("%d_%m_%Y__%H-%M-%S")
    nombre_archivo = os.path.join(carpeta, f"Rayo_{fecha_hora}.bin")
    with open(nombre_archivo, "wb") as f:
        f.write(datos_bin)

    print(f"⚡ Evento de rayo detectado y guardado en {nombre_archivo}")

print("Finalizó la adquisición de datos.")
