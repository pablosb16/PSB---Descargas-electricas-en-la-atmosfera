##################################################
#                                                #
#        GRABAR EN BUCLE DE DATOS EN BINARIO     #
#                                                #
##################################################
import pyvisa
import numpy as np
import os
import time
from datetime import datetime
tiempoi = time.time()

# Establecer tiempo de ejecución en 1 minuto (60 segundos)
tiempo_inicio = time.time()
tiempo_maximo = 60*24*60  # Segundos

# Configurar conexión con el osciloscopio
rm = pyvisa.ResourceManager()
osc = rm.open_resource("USB0::0x0AAD::0x01D6::106638::0::INSTR")  
osc.timeout = 60000  # 60 segundos


osc.write("*RST")

# Configurar parámetros de adquisición
osc.write("TIM:SCAL 50E-3")  # Base de tiempo 
osc.write("CHAN1:SCAL 1E0")  # Escala de voltaje 1V/div
osc.write("FORM REAL")  # Datos en formato binario
osc.write("CHAN:DATA:POIN MIN")  # Usar 1024 puntos de datos
osc.write("FORM:BORD LSBF")
osc.write("CHAN1: SET IMP 50OH")

print('CAMBIA LA IMPEDANCIA!!!!!!!!!!!!!!')

# Iniciar bucle para adquirir datos durante 1 minuto
while time.time() - tiempo_inicio < tiempo_maximo:
    # Iniciar adquisición
    osc.write("SING")
    osc.query("*OPC?")  # Esperar a que termine la adquisición

    # Obtener datos
    osc.write("CHAN:DATA?")
    datos_bin = osc.read_raw()

    # El encabezado tiene la forma #4 (por ejemplo) y se debe saltar
    encabezado_len = 8  # Asumimos que el encabezado ocupa 4 bytes (ajustar si es necesario)
    datos_bin = datos_bin[encabezado_len:]  # Saltar el encabezado

    # Asegurarnos de que el tamaño de los datos es múltiplo de 4 antes de la conversión
    tamano_datos = len(datos_bin)
    if tamano_datos % 4 != 0:
        tamano_valido = tamano_datos - (tamano_datos % 4)  # Redondear al múltiplo de 4 más cercano
        datos_bin = datos_bin[:tamano_valido]

    # Convertir los datos binarios a un array de numpy (float32)
    try:
        datos = np.frombuffer(datos_bin, dtype=np.float32)
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        datos = np.array([], dtype=np.float32)

    # Generar el nombre del archivo con fecha y hora
    fecha_hora = datetime.now().strftime("%d_%m_%Y__%H-%M-%S")
    carpeta = os.path.join(os.path.expanduser("~"), "Desktop", "Datos_Osciloscopio")
    os.makedirs(carpeta, exist_ok=True)
    nombre_archivo = os.path.join(carpeta, f"{fecha_hora}.bin")

    # Guardar los datos en formato binario
    with open(nombre_archivo, "wb") as f:
        f.write(datos_bin)

    # # Reiniciar el osciloscopio
    # osc.write("*RST")

    # Esperar un poco para evitar sobrecargar el sistema
    # time.sleep(1)
    
    
    if time.time() - tiempo_inicio > 3600:  # Cada hora
        osc.close()
        time.sleep(2)  # Pequeña espera antes de reconectar
        osc = rm.open_resource("USB0::0x0AAD::0x01D6::106638::0::INSTR")
        osc.timeout = 60000


# Fin del bucle, ha pasado 1 minuto
print("Se ha completado el tiempo de adquisición de: " +str(tiempo_maximo/60)+ ' minutos')
tiempof = time.time()
# print(f"Datos guardados en {nombre_archivo}")
print(f'Tardó {tiempof - tiempoi} segundos.')