# gui.py
# Módulo que contiene la interfaz gráfica para seleccionar archivos Excel y mostrar información
# con un diseño moderno y profesional

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os


def create_main_window(root, process_callback):
    """
    Crea la ventana principal de la interfaz gráfica con un diseño moderno y profesional

    Args:
        root: Ventana principal de Tkinter
        process_callback: Función a llamar cuando se procesa un archivo
    """
    # Configuración básica de la ventana
    root.title("Visor Técnico Bot")
    root.geometry("800x700")
    root.resizable(False, False)

    # Configurar colores
    bg_color = '#F5F7FA'
    card_color = '#FFFFFF'
    primary_color = '#0052CC'
    secondary_color = '#42526E'
    border_color = '#DFE1E6'
    hover_color = '#0065FF'

    # Configurar la ventana principal
    root.configure(bg=bg_color)

    # Configurar estilos
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')

    # Estilos para componentes
    style.configure('Main.TFrame', background=bg_color)
    style.configure('Card.TFrame', background=card_color, relief='flat')
    style.configure('Title.TLabel', background=bg_color, foreground=primary_color,
                    font=('Segoe UI', 24, 'bold'))
    style.configure('Subtitle.TLabel', background=bg_color, foreground=secondary_color,
                    font=('Segoe UI', 12))
    style.configure('CardTitle.TLabel', background=card_color, foreground=primary_color,
                    font=('Segoe UI', 12, 'bold'))
    style.configure('CardDesc.TLabel', background=card_color, foreground=secondary_color,
                    font=('Segoe UI', 10))
    style.configure('Status.TLabel', background=bg_color, foreground=secondary_color,
                    font=('Segoe UI', 11))
    style.configure('Custom.TEntry',
                    fieldbackground='#F4F5F7',
                    bordercolor=border_color,
                    lightcolor=border_color,
                    darkcolor=border_color)
    style.configure("Custom.Horizontal.TProgressbar",
                    troughcolor='#F4F5F7',
                    background=primary_color,
                    bordercolor=border_color,
                    lightcolor=primary_color,
                    darkcolor=primary_color)

    # Frame principal con padding
    main_frame = ttk.Frame(root, style='Main.TFrame', padding="35")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Logo y título
    title_frame = ttk.Frame(main_frame, style='Main.TFrame')
    title_frame.pack(fill=tk.X, pady=(0, 30))

    # Icono simple usando texto
    icon_label = ttk.Label(title_frame, text="📊", font=('Segoe UI', 36),
                           background=bg_color, foreground=primary_color)
    icon_label.pack()

    title_label = ttk.Label(title_frame, text="Visor Técnico Bot", style='Title.TLabel')
    title_label.pack(pady=(10, 0))

    subtitle_label = ttk.Label(title_frame,
                               text="Analiza datos técnicos y genera reportes profesionales en PDF",
                               style='Subtitle.TLabel')
    subtitle_label.pack(pady=(8, 0))

    # Contenedor para la selección de archivo
    file_container = ttk.Frame(main_frame, style='Main.TFrame')
    file_container.pack(fill=tk.X, pady=15)

    # Variable para almacenar la ruta del archivo
    file_path_var = tk.StringVar()

    # Tarjeta para selección de archivo Excel
    card_frame = ttk.Frame(file_container, style='Main.TFrame')
    card_frame.pack(fill=tk.X, pady=8)

    card = ttk.Frame(card_frame, style='Card.TFrame', padding=20)
    card.pack(fill=tk.X, padx=10)
    card.configure(relief='solid', borderwidth=1)

    # Frame para título y descripción
    header_frame = ttk.Frame(card, style='Card.TFrame')
    header_frame.pack(fill=tk.X, pady=(0, 12))

    # Título
    title_label = ttk.Label(header_frame, text="📁 Archivo Excel de Datos", style='CardTitle.TLabel')
    title_label.pack(anchor='w')

    # Descripción
    desc_label = ttk.Label(header_frame,
                           text="Seleccione el archivo Excel con los datos de tiempos de estadía",
                           style='CardDesc.TLabel', wraplength=550)
    desc_label.pack(anchor='w', pady=(4, 0))

    # Frame para entrada y botón
    input_frame = ttk.Frame(card, style='Card.TFrame')
    input_frame.pack(fill=tk.X)

    # Frame interior para el entry con padding y borde
    entry_frame = ttk.Frame(input_frame, style='Card.TFrame')
    entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12))

    # Entry mejorado
    entry = ttk.Entry(entry_frame,
                      textvariable=file_path_var,
                      width=50,
                      style='Custom.TEntry',
                      font=('Segoe UI', 10))
    entry.pack(fill=tk.X, ipady=8)
    entry.configure(state='readonly')

    # Botón de selección
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

    select_button = ttk.Button(input_frame,
                               text="Examinar",
                               command=select_file,
                               padding=(15, 8),
                               cursor='hand2')
    select_button.pack(side=tk.LEFT)

    # Contenedor para el botón de procesamiento
    action_container = ttk.Frame(main_frame, style='Main.TFrame')
    action_container.pack(fill=tk.X, pady=25)

    # Botón de procesamiento
    button_frame = ttk.Frame(action_container, style='Main.TFrame')
    button_frame.pack(pady=(0, 25))

    # Definimos la función para procesar el archivo
    def process_file():
        file_path = file_path_var.get()
        if not file_path:
            tk.messagebox.showwarning("Advertencia", "Por favor seleccione un archivo Excel primero.")
            return

        if not os.path.exists(file_path):
            tk.messagebox.showerror("Error", "El archivo seleccionado no existe.")
            return

        # Llamar a la función de procesamiento proporcionada
        status_var.set("⏳ Procesando archivo...")
        progress_var.set(20)
        root.update()

        try:
            # Mostrar progreso simulado
            progress_var.set(50)
            root.update()

            # Llamar al callback de procesamiento
            process_callback(file_path)

            # Actualizar estado
            progress_var.set(100)
            status_var.set("✅ Archivo procesado con éxito")

            # Resetear después de 3 segundos
            root.after(3000, lambda: [progress_var.set(0), status_var.set("✓ Listo para procesar")])

        except Exception as e:
            # Manejar errores
            status_var.set("❌ Error durante el procesamiento")
            progress_var.set(0)
            messagebox.showerror("Error", f"No se pudo procesar el archivo: {str(e)}")

    # Crear el botón con un estilo moderno
    process_button = tk.Button(
        button_frame,
        text="Generar Reporte PDF",
        command=process_file,
        bg=primary_color,
        fg='white',
        font=('Segoe UI', 13, 'bold'),
        relief='flat',
        width=22,
        height=2,
        cursor='hand2',
        activebackground=hover_color,
        activeforeground='white',
        bd=0,
        highlightthickness=0
    )
    process_button.pack(expand=True)

    # Efectos visuales para el botón
    def on_enter(e):
        process_button['background'] = hover_color

    def on_leave(e):
        process_button['background'] = primary_color

    process_button.bind('<Enter>', on_enter)
    process_button.bind('<Leave>', on_leave)

    # Barra de progreso
    progress_frame = ttk.Frame(action_container, style='Main.TFrame')
    progress_frame.pack(fill=tk.X, pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_frame,
                                   style="Custom.Horizontal.TProgressbar",
                                   variable=progress_var,
                                   maximum=100,
                                   length=450,
                                   mode='determinate')
    progress_bar.pack(fill=tk.X, padx=50)

    # Label de estado
    status_var = tk.StringVar()
    status_var.set("✓ Listo para procesar")
    status_label = ttk.Label(action_container,
                             textvariable=status_var,
                             style='Status.TLabel')
    status_label.pack(pady=10)

    return root