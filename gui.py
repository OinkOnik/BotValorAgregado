# gui.py
# Módulo que contiene la interfaz gráfica para seleccionar archivos Excel y mostrar información

import tkinter as tk
from tkinter import filedialog, ttk
import os
from ttkthemes import ThemedTk


def create_main_window(root, process_callback):
    """
    Crea la ventana principal de la interfaz gráfica

    Args:
        root: Ventana principal de Tkinter
        process_callback: Función a llamar cuando se procesa un archivo
    """
    # Convertir root a un ThemedTk si no lo es ya
    if not isinstance(root, ThemedTk):
        # Guardar la posición original
        if hasattr(root, 'geometry'):
            geometry = root.geometry()
        else:
            geometry = "650x480"

        # Destruir la ventana original
        root.destroy()

        # Crear una nueva con tema
        root = ThemedTk(theme="arc")  # Usamos el tema 'arc' que es moderno y minimalista
        root.geometry(geometry)
        root.title("Visor Técnico Bot")

    # Configurar la ventana principal
    root.configure(bg="#f0f0f0")

    # Estilo personalizado sobre el tema
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0")
    style.configure("Header.TLabel", font=("Helvetica", 22, "bold"), foreground="#2c3e50")
    style.configure("Subheader.TLabel", font=("Helvetica", 11), foreground="#34495e")
    style.configure("TLabelframe", background="#f0f0f0")
    style.configure("TLabelframe.Label", font=("Helvetica", 11), foreground="#2c3e50")
    style.configure("AccentButton.TButton", font=("Helvetica", 11, "bold"))
    style.configure("Status.TLabel", background="#f5f5f5", foreground="#555555", font=("Helvetica", 9))

    # Crear un frame principal con padding
    main_frame = ttk.Frame(root, padding="40", style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Logo o icono (opcional - aquí usamos un texto con estilo)
    logo_frame = ttk.Frame(main_frame, style="TFrame")
    logo_frame.pack(pady=(0, 10))

    # Título de la aplicación
    title_label = ttk.Label(
        main_frame,
        text="Visor Técnico Bot",
        style="Header.TLabel"
    )
    title_label.pack(pady=(0, 10))

    # Línea divisoria
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill=tk.X, pady=15)

    # Descripción
    description = "Aplicación de escritorio que analiza datos técnicos desde archivos Excel y genera reportes automatizados en PDF."
    desc_label = ttk.Label(main_frame, text=description, wraplength=550, style="Subheader.TLabel")
    desc_label.pack(pady=(0, 25))

    # Frame para selección de archivo con esquinas redondeadas
    file_frame = ttk.LabelFrame(main_frame, text="Selección de Archivo", padding="20")
    file_frame.pack(fill=tk.X, pady=15)

    # Variables para almacenar la ruta del archivo
    file_path_var = tk.StringVar()

    # Entrada para mostrar la ruta del archivo
    file_entry = ttk.Entry(file_frame, textvariable=file_path_var, width=50, font=("Helvetica", 10))
    file_entry.pack(side=tk.LEFT, padx=(5, 10), pady=10, fill=tk.X, expand=True)

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

    select_button = ttk.Button(file_frame, text="Examinar", command=select_file)
    select_button.pack(side=tk.LEFT, padx=(5, 5), pady=10)

    # Frame para botones
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=25)

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
        button_frame,
        text="Generar Reporte PDF",
        command=process_file,
        style="AccentButton.TButton"
    )
    process_button.pack(pady=5, ipadx=20, ipady=10)

    # Etiqueta de estado
    status_var = tk.StringVar()
    status_var.set("Listo para procesar")
    status_label = ttk.Label(
        root,
        textvariable=status_var,
        style="Status.TLabel",
        padding=(15, 8)
    )
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    return root