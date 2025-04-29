# main.py
# Archivo principal que ejecuta la aplicación del Bot para procesar datos Excel y generar informes PDF

from ttkthemes import ThemedTk
from tkinter import messagebox, filedialog
from gui import create_main_window
from excel_processor import process_excel_file
from pdf_generator import generate_pdf_report
import os


def main():
    """
    Función principal que inicia la aplicación
    """
    root = ThemedTk(theme="arc")  # Usamos el tema 'arc' para un aspecto moderno
    root.title("Visor Técnico Bot")

    # Inicializar la interfaz gráfica
    create_main_window(root, process_data)

    root.mainloop()


def process_data(excel_file_path, output_pdf_path=None):
    """
    Procesa los datos del archivo Excel seleccionado y genera el informe PDF

    Args:
        excel_file_path: Ruta al archivo Excel seleccionado
        output_pdf_path: Ruta donde se guardará el archivo PDF (opcional)
    """
    try:
        # Procesar el archivo Excel
        data = process_excel_file(excel_file_path)

        if not data:
            messagebox.showerror("Error", "No se encontraron datos para procesar.")
            return

        # Si no se proporcionó una ruta de salida, solicitar al usuario que elija dónde guardar
        if not output_pdf_path:
            # Generar un nombre predeterminado basado en el archivo Excel
            default_filename = os.path.splitext(os.path.basename(excel_file_path))[0] + ".pdf"

            # Abrir diálogo para seleccionar dónde guardar
            output_pdf_path = filedialog.asksaveasfilename(
                title="Guardar Reporte PDF",
                defaultextension=".pdf",
                initialfile=default_filename,
                filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
            )

            # Si el usuario cancela, salir
            if not output_pdf_path:
                return

        # Generar el PDF con los datos procesados
        generate_pdf_report(data, output_pdf_path)

        messagebox.showinfo("Éxito", f"El informe PDF ha sido generado: {output_pdf_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo: {str(e)}")


if __name__ == "__main__":
    main()