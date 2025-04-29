# gui.py
# Módulo que contiene la interfaz gráfica para seleccionar archivos Excel y mostrar información

import tkinter as tk
from tkinter import filedialog, ttk
import os


def create_main_window(root, process_callback):
    """
    Crea la ventana principal de la interfaz gráfica

    Args:
        root: Ventana principal de Tkinter
        process_callback: Función a llamar cuando se procesa un archivo
    """
    # Configurar la ventana principal
    root.geometry("600x400")
    root.resizable(True, True)

    # Crear un frame principal con padding
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Título de la aplicación
    title_label = ttk.Label(
        main_frame,
        text="Bot Procesador Excel a PDF",
        font=("Arial", 16, "bold")
    )
    title_label.pack(pady=(0, 20))

    # Descripción
    description = "Esta aplicación procesa datos de Excel para calcular tiempos basados en horas de llegada y salida, y genera un reporte en PDF."
    desc_label = ttk.Label(main_frame, text=description, wraplength=500)
    desc_label.pack(pady=(0, 20))

    # Frame para selección de archivo
    file_frame = ttk.LabelFrame(main_frame, text="Selección de Archivo Excel")
    file_frame.pack(fill=tk.X, pady=10)

    # Variables para almacenar la ruta del archivo
    file_path_var = tk.StringVar()

    # Entrada para mostrar la ruta del archivo
    file_entry = ttk.Entry(file_frame, textvariable=file_path_var, width=50)
    file_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10, fill=tk.X, expand=True)

    # Botón para seleccionar archivo
    def select_file():
        file_types = [
            ('Archivos Excel', '*.xlsx;*.xls'),
            ('Todos los archivos', '*.*')
        ]
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=file_types
        )
        if file_path:
            file_path_var.set(file_path)

    select_button = ttk.Button(file_frame, text="Examinar...", command=select_file)
    select_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

    # Botón para procesar el archivo
    def process_file():
        file_path = file_path_var.get()
        if not file_path:
            tk.messagebox.showwarning("Advertencia", "Por favor seleccione un archivo Excel primero.")
            return

        if not os.path.exists(file_path):
            tk.messagebox.showerror("Error", "El archivo seleccionado no existe.")
            return

        process_callback(file_path)

    process_button = ttk.Button(
        main_frame,
        text="Procesar archivo y generar PDF",
        command=process_file
    )
    process_button.pack(pady=20)

    # Etiqueta de estado
    status_var = tk.StringVar()
    status_var.set("Listo para procesar.")
    status_label = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    return root