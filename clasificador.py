import os
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']

def kmeans(X, n_clusters, max_iters=100):
    # Inicialización aleatoria de centroides
    centroids = X[np.random.choice(range(len(X)), n_clusters, replace=False)]
    
    for _ in range(max_iters):
        # Asignación de puntos a clusters
        labels = np.argmin(np.linalg.norm(X[:, np.newaxis] - centroids, axis=2), axis=1)
        
        # Actualización de centroides
        new_centroids = np.array([X[labels == i].mean(axis=0) if np.sum(labels == i) > 0 else centroids[i] for i in range(n_clusters)])
        
        # Verificar convergencia
        if np.allclose(centroids, new_centroids):
            break
        
        centroids = new_centroids
    
    return labels, centroids

# Función para cargar la imagen desde archivos de canales RGB
def load_image_channels(red_path, green_path, blue_path):
    red_channel = np.load(red_path)
    green_channel = np.load(green_path)
    blue_channel = np.load(blue_path)
    return np.dstack((red_channel, green_channel, blue_channel))

# Obtener la lista de archivos en el directorio './data/'
files_in_directory = sorted(os.listdir('./data/'))
num_files = len([f for f in files_in_directory if f.endswith('_red.npy')])

# Crear una matriz para almacenar los datos de todas las imágenes
all_data = []

# Cargar los datos de imagen desde archivos
for i in range(1, num_files + 1):
    red_channel_path = os.path.join('./data', f'image_{i}_red.npy')
    green_channel_path = os.path.join('./data', f'image_{i}_green.npy')
    blue_channel_path = os.path.join('./data', f'image_{i}_blue.npy')

    # Cargar canales RGB
    X = load_image_channels(red_channel_path, green_channel_path, blue_channel_path)
    
    # Añadir los datos a la matriz
    all_data.append(X.reshape(-1, 3))

# Concatenar los datos de todas las imágenes
all_data = np.concatenate(all_data, axis=0)

# Aplicar el algoritmo K-Means
n_clusters = 3
labels, centroids = kmeans(all_data, n_clusters)

# Visualizar resultados
colors = ["g.", "r.", "b."]
plt.scatter(all_data[:, 0], all_data[:, 1], c=labels, cmap='viridis', s=10)

# Ajustar límites del gráfico
plt.xlim(all_data[:, 0].min(), all_data[:, 0].max())
plt.ylim(all_data[:, 1].min(), all_data[:, 1].max())

# Etiquetas de los ejes x e y
plt.xlabel('Rojo')
plt.ylabel('Verde')

# Mostrar nombres de colores en los ejes x e y
for i, color in enumerate(colors):
    plt.text(centroids[i, 0], centroids[i, 1], color[0], color=color[0], fontsize=12, ha='right', va='bottom')

plt.scatter(centroids[:, 0], centroids[:, 1], marker="x", s=150, linewidths=5, zorder=10, c='red')
plt.show()
