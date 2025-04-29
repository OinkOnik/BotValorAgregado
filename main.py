# main.py
# Archivo principal que ejecuta la aplicación del Bot para procesar datos Excel y generar informes PDF

import tkinter as tk
from tkinter import messagebox
from gui import create_main_window
from excel_processor import process_excel_file
from pdf_generator import generate_pdf_report


def main():
    """
    Función principal que inicia la aplicación
    """
    root = tk.Tk()
    root.title("Bot Procesador Excel a PDF")

    # Inicializar la interfaz gráfica
    create_main_window(root, process_data)

    root.mainloop()


def process_data(excel_file_path):
    """
    Procesa los datos del archivo Excel seleccionado y genera el informe PDF

    Args:
        excel_file_path: Ruta al archivo Excel seleccionado
    """
    try:
        # Procesar el archivo Excel
        data = process_excel_file(excel_file_path)

        if not data:
            messagebox.showerror("Error", "No se encontraron datos para procesar.")
            return

        # Generar el nombre del archivo PDF basado en el Excel
        pdf_file_path = excel_file_path.replace('.xlsx', '.pdf').replace('.xls', '.pdf')

        # Generar el PDF con los datos procesados
        generate_pdf_report(data, pdf_file_path)

        messagebox.showinfo("Éxito", f"El informe PDF ha sido generado: {pdf_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo: {str(e)}")


if __name__ == "__main__":
    main()