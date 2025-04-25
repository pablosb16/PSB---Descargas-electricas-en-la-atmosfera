import os
import struct
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# Directorio base con los archivos
directory = r'C:/Users/Usuario/Desktop/Datos 20 03 (tormenta cerca)/Datos Serie 58'

def read_binary_file(file_path):
    """Lee un archivo binario y devuelve los valores en una lista."""
    data = []
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"Advertencia: El archivo {file_path} está vacío.")
            return None
        
        with open(file_path, 'rb') as file:
            while True:
                byte_data = file.read(4)
                if not byte_data:
                    break
                if len(byte_data) != 4:
                    print(f"Error: Archivo {file_path} tiene datos incompletos.")
                    return None
                try:
                    float_value = struct.unpack('f', byte_data)[0]
                    data.append(float_value)
                except struct.error:
                    print(f"Error al leer datos en {file_path}, posible archivo corrupto.")
                    return None
    except Exception as e:
        print(f"No se pudo leer {file_path}: {e}")
        return None
    return np.array(data) if data else None

# Leer todos los archivos en la carpeta
data_dict = {}
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        print(f"Leyendo archivo: {filename}, tamaño: {os.path.getsize(file_path)} bytes")
        data = read_binary_file(file_path)
        if data is not None:
            data_dict[filename] = data

if not data_dict:
    print("No se encontraron datos válidos para procesar.")
    sys.exit(1)

# Asegurar que todos los arrays tengan la misma longitud recortándolos al mínimo común
def equalize_lengths(data_dict):
    min_length = min(len(arr) for arr in data_dict.values())
    return {key: arr[:min_length] for key, arr in data_dict.items()}

data_dict = equalize_lengths(data_dict)

# Aplicar Transformada de Fourier y extraer las magnitudes de las frecuencias
fft_dict = {key: np.abs(np.fft.fft(arr))[:len(arr)//2] for key, arr in data_dict.items()}

# Asegurar que todas las FFT tengan la misma longitud
min_fft_length = min(len(arr) for arr in fft_dict.values())
fft_dict = {key: arr[:min_fft_length] for key, arr in fft_dict.items()}

# Convertir los datos a una matriz
matrix = np.array(list(fft_dict.values()))
print(f"Dimensión de la matriz de datos FFT: {matrix.shape}, Memoria utilizada: {matrix.nbytes / 1e6:.2f} MB")

# Verificar si la matriz tiene suficientes datos para la correlación
if matrix.shape[0] < 2:
    print("No hay suficientes archivos con datos válidos para calcular la correlación.")
    sys.exit(1)

# Calcular la matriz de correlación sobre las frecuencias
corr_matrix = np.corrcoef(matrix)

# Obtener nombres de archivos para etiquetas
titles = list(fft_dict.keys())

# Graficar la matriz de correlación con etiquetas
plt.figure(figsize=(10, 8))
sns.heatmap(
    corr_matrix,
    annot=False,
    cmap="Spectral",
    xticklabels=titles,
    yticklabels=titles
)

plt.xticks(rotation=90, fontsize=8)
plt.yticks(fontsize=8)
plt.title("Matriz de Correlación de Frecuencias")

# Mostrar el gráfico
plt.show()

print("✅ Gráfico de correlación generado correctamente")

