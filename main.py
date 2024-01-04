import os
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from threading import Thread
import requests
from ttkthemes import ThemedTk

class AplicacionDescargador:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x300")
        self.root.title("Descargador de Videos de YouTube")
        # Configurar el tema "clam" de ttkthemes
        self.root.set_theme("clam")
        # Crear una fuente personalizada para un aspecto más moderno
        self.custom_font = tkfont.Font(family="Arial", size=12)
        self.crear_widgets()

    def crear_widgets(self):
        self.progress_var = tk.DoubleVar()
        self.success_label = tk.Label(self.root, text="", font=("Arial", 12))
        # Crear una barra de progreso
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, length=400, mode='determinate')
        self.progress_bar.pack(pady=10)
        # Widget de entrada para la URL con fuente más grande y estilo de fuente personalizado
        self.url_label = ttk.Label(self.root, text="URL", font=self.custom_font)
        self.url_label.pack(pady=5)
        self.url_entry = ttk.Entry(self.root, font=self.custom_font, width=50)
        self.url_entry.pack(pady=5)
        # Botón para iniciar la descarga
        boton_descargar = ttk.Button(self.root, text="Descargar", command=self.iniciar_descarga)
        boton_descargar.pack(pady=10)
        # Etiqueta para mostrar el mensaje de éxito y la ruta del archivo
        self.success_label.pack(pady=10)

    def iniciar_descarga(self):
        url = self.url_entry.get()
        hilo_descarga = Thread(target=self.descargar_video, args=(url,))
        hilo_descarga.start()

    def descargar_video(self, url):
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        total_size = video.filesize

        def en_progreso():
            descargado = 0
            tamano_chunk = 1024
            respuesta = requests.get(video.url, stream=True)
            ruta_archivo = os.path.join(os.getcwd(), video.title + ".mp4")
            with open(ruta_archivo, 'wb') as f:
                for chunk in respuesta.iter_content(chunk_size=tamano_chunk):
                    if chunk:
                        f.write(chunk)
                        descargado += len(chunk)
                        progreso = (descargado / total_size) * 100
                        self.progress_var.set(progreso)
            # Actualizar la interfaz con el mensaje de éxito y la ruta del archivo
            self.success_label.config(text=f"Descarga exitosa!\nArchivo guardado en:\n{ruta_archivo}")
        # Ejecutar la descarga en un hilo para no bloquear la interfaz de usuario
        hilo_descarga = Thread(target=en_progreso)
        hilo_descarga.start()

def main():
    root = ThemedTk(theme="clam")  # Usar el tema "clam" de ttkthemes
    app = AplicacionDescargador(root)
    root.mainloop()

if __name__ == "__main__":
    main()
