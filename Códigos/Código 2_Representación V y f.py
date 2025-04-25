##################################################
#                                                #
#         REPRESENTAR VOLTAJE Y FRECUENCIA       #
#                                                #
##################################################
import os
import struct
import matplotlib.pyplot as plt
import numpy as np

end_time = 500  # Tiempo total en microsegundos

# Directorio
directory = r'C:/Users/Usuario/Desktop/Representación de datos'

# Listar todos los archivos en el directorio
for filename in os.listdir(directory):
    data = []

    # Crear la ruta completa del archivo
    file_path = os.path.join(directory, filename)

    # Asegurarnos de que estamos procesando archivos y no directorios
    if os.path.isfile(file_path):
        print(f"Reading file: {filename}")

        # Abrir el archivo binario en modo lectura
        with open(file_path, 'rb') as file:
            while True:
                # Leer 4 bytes a la vez (32 bits)
                byte_data = file.read(4)
                if not byte_data:
                    break  # Fin del archivo

                # Desempaquetar los bytes como un float de 32 bits (IEEE 754)
                float_value = struct.unpack('f', byte_data)[0]

                # Añadir el valor a la lista de datos
                data.append(float_value)
    
    # Convertir los datos a un array de numpy
    data = np.array(data)
    
    num_points = len(data)
    t = np.linspace(0, end_time, num_points)  # Array de tiempo en microsegundos

    # Calcular el intervalo de muestreo (dt)
    dt = t[1] - t[0]

    # Generar una señal seno teórica de 1 kHz
    f_teo = 1  # Frecuencia en kHz
    seno_teo = np.sin(2 * np.pi * f_teo * t)
    
    # Pulso teórico basado en una ecuación exponencial
    Vo = 2
    alfa = 10.043
    beta = 353.793
    pulsoWF4 = Vo * (np.exp(-alfa * t) - np.exp(-beta * t))

    # Graficar en subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(f"Análisis de Señal - {filename}", fontsize=14, fontweight="bold")

    # Señal en el dominio del tiempo
    axs[0].plot(t, data, color='royalblue', label='Señal Real')
    axs[0].set_xlabel("Tiempo (ms)")  # Cambiado de 'us' a 'mus'
    axs[0].set_ylabel("Voltaje (V)")
    axs[0].set_title("Señal en el tiempo")
    axs[0].legend()
    axs[0].grid(True)  # Se mantiene el grid activado
    
    # Calcular la FFT de los datos
    fft_data = np.fft.fft(data)
    fft_magnitude = np.abs(fft_data) / len(data)  # Normalización

    # Obtener las frecuencias correspondientes a la FFT
    freqs = np.fft.fftfreq(len(data), d=dt)

    # Solo tomamos la mitad positiva de la frecuencia y la magnitud
    half_range = len(data) // 2
    freqs_positive = freqs[:half_range]
    fft_magnitude_positive = fft_magnitude[:half_range]

    # Espectro de Frecuencia (FFT) - solo frecuencias positivas
    axs[1].semilogy(freqs_positive, fft_magnitude_positive, color='rosybrown', label='FFT Real')
    
    # Calcular y graficar la FFT de la señal teórica (seno de 1 kHz)
    fft_teo = np.fft.fft(seno_teo)
    fft_magnitude_teo = np.abs(fft_teo) / len(seno_teo)
    
    axs[1].set_xlabel("Frecuencia (Hz)")
    axs[1].set_ylabel("Magnitud normalizada")
    axs[1].set_title("Espectro de Frecuencia (FFT)")
    axs[1].legend()
    axs[1].grid(True)  # Grid activado en la FFT
    
    plt.tight_layout()
    plt.show()
