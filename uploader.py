import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageManipulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Manipulator")
        self.root.geometry("800x700")

        self.load_button = tk.Button(root, text="Cargar Imagen", command=self.load_image)
        self.load_button.grid(row=0, column=0, pady=10)

        self.image_label = tk.Label(root)
        self.image_label.grid(row=1, column=0, pady=10)

        # Labels para los canales
        self.label_red = tk.Label(root, text="Canal Rojo")
        self.label_red.grid(row=2, column=0, pady=20)

        self.label_green = tk.Label(root, text="Canal Verde")
        self.label_green.grid(row=2, column=1, pady=20)

        self.label_blue = tk.Label(root, text="Canal Azul")
        self.label_blue.grid(row=2, column=2, pady=20)

        self.process_button = tk.Button(root, text="Procesar", command=self.process_channels)
        self.process_button.grid(row=5, column=0, pady=10)

        # Variable para almacenar las imágenes procesadas
        self.processed_images = []

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            original_image = Image.open(file_path)

            # Redimensionar la imagen a 200x400
            resized_image = original_image.resize((250, 100))

            self.original_image = resized_image
            self.display_image(self.original_image, self.image_label)

    def display_image(self, image, label):
        tk_image = ImageTk.PhotoImage(image)
        label.config(image=tk_image)
        label.image = tk_image

    def display_images(self, original, red, green, blue):
        tk_original = ImageTk.PhotoImage(original)
        tk_red = ImageTk.PhotoImage(red)
        tk_green = ImageTk.PhotoImage(green)
        tk_blue = ImageTk.PhotoImage(blue)

        self.image_label.config(image=tk_original)
        self.image_label.image = tk_original

        self.label_red.config(image=tk_red)
        self.label_red.image = tk_red

        self.label_green.config(image=tk_green)
        self.label_green.image = tk_green

        self.label_blue.config(image=tk_blue)
        self.label_blue.image = tk_blue

    def process_channels(self):
        if hasattr(self, 'original_image'):
            # Convertir la imagen original a un arreglo NumPy
            original_image_array = np.array(self.original_image)

            # Separar los canales RGB
            red_channel_array = original_image_array.copy()
            red_channel_array[:, :, (1, 2)] = 0

            green_channel_array = original_image_array.copy()
            green_channel_array[:, :, (0, 2)] = 0

            blue_channel_array = original_image_array.copy()
            blue_channel_array[:, :, (0, 1)] = 0

            # Crear imágenes con cada canal
            red_channel_image = Image.fromarray(red_channel_array)
            green_channel_image = Image.fromarray(green_channel_array)
            blue_channel_image = Image.fromarray(blue_channel_array)

            # Obtener el índice para el nombre del archivo
            files_in_directory = os.listdir('./data/')
            num_files = len([f for f in files_in_directory if f.endswith('.npy')]) // 3 + 1
            filename_base = './data/image_{}'.format(num_files)

            np.save(filename_base + '_red.npy', red_channel_array)
            np.save(filename_base + '_green.npy', green_channel_array)
            np.save(filename_base + '_blue.npy', blue_channel_array)

            # Mostrar todas las imágenes
            self.display_images(self.original_image, red_channel_image, green_channel_image, blue_channel_image)

            # Almacenar las matrices de canales
            self.red_channel_array = red_channel_array
            self.green_channel_array = green_channel_array
            self.blue_channel_array = blue_channel_array

            # Almacenar las imágenes procesadas
            self.processed_images = [red_channel_image, green_channel_image, blue_channel_image]

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageManipulator(root)
    root.mainloop()
