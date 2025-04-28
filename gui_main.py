# gui_main.py
# Contiene la clase principal de la ventana de análisis de tiempos
# Maneja la ventana principal y la carga de archivos

import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFileDialog, QTabWidget, QMessageBox,
                             QStatusBar)
from PyQt5.QtCore import QThread, pyqtSignal
from gui_tabs import (update_summary_tab, update_technician_tab,
                     update_terminal_model_tab, update_anomalies_tab)
from gui_components import clear_layout
from data_loader import load_excel_file, clean_time_data, validate_required_columns
from time_analyzer import calculate_service_duration

class PDFExportThread(QThread):
    """
    Thread para exportar PDF en segundo plano para no bloquear la interfaz.
    """
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, df, output_path):
        super().__init__()
        self.df = df
        self.output_path = output_path

    def run(self):
        try:
            from pdf_generator import PDFGenerator
            pdf_gen = PDFGenerator()
            result_path = pdf_gen.create_pdf_report(self.df, self.output_path)
            self.finished.emit(result_path)
        except Exception as e:
            self.error.emit(str(e))


class TimeAnalysisWindow(QMainWindow):
    """
    Ventana principal para el análisis de tiempos de servicio.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análisis de Tiempos de Servicio")
        self.setGeometry(100, 100, 1200, 800)

        # Variable para almacenar el DataFrame
        self.df = None

        # Variable para el thread de exportación PDF
        self.pdf_thread = None

        # Configurar la interfaz
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)

        # Area superior para cargar archivo
        top_layout = QHBoxLayout()

        self.load_button = QPushButton("Cargar Archivo Excel")
        self.load_button.clicked.connect(self.load_excel_file)
        self.file_label = QLabel("Ningún archivo cargado")

        top_layout.addWidget(self.load_button)
        top_layout.addWidget(self.file_label)

        # Botón para exportar a PDF
        self.export_pdf_button = QPushButton("Exportar a PDF")
        self.export_pdf_button.clicked.connect(self.export_to_pdf)
        self.export_pdf_button.setEnabled(False)  # Desactivado hasta que se cargue un archivo

        top_layout.addWidget(self.export_pdf_button)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        # Tabs para diferentes análisis
        self.tabs = QTabWidget()

        # Tab de resumen
        self.summary_tab = QWidget()
        self.summary_layout = QVBoxLayout(self.summary_tab)
        self.tabs.addTab(self.summary_tab, "Resumen")

        # Tab de análisis por técnico
        self.tech_tab = QWidget()
        self.tech_layout = QVBoxLayout(self.tech_tab)
        self.tabs.addTab(self.tech_tab, "Por Técnico")

        # Tab de análisis por modelo de terminal
        self.terminal_tab = QWidget()
        self.terminal_layout = QVBoxLayout(self.terminal_tab)
        self.tabs.addTab(self.terminal_tab, "Por Modelo de Terminal")

        # Tab de anomalías
        self.anomaly_tab = QWidget()
        self.anomaly_layout = QVBoxLayout(self.anomaly_tab)
        self.tabs.addTab(self.anomaly_tab, "Anomalías")

        main_layout.addWidget(self.tabs)

        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def load_excel_file(self):
        """Carga un archivo Excel seleccionado por el usuario"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Archivo Excel", "", "Archivos Excel (*.xlsx *.xls)"
        )

        if file_path:
            try:
                # Actualizamos el status bar
                self.status_bar.showMessage("Cargando archivo Excel...")

                # Cargamos el archivo
                self.df = load_excel_file(file_path)

                # Verificamos columnas requeridas
                required_columns = ['Hora de llegada', 'Hora de salida']
                try:
                    validate_required_columns(self.df, required_columns)
                except ValueError as e:
                    QMessageBox.warning(self, "Advertencia", str(e))
                    return

                # Limpiamos los datos de tiempo
                self.df = clean_time_data(self.df)

                # Actualizamos la etiqueta con el nombre del archivo
                self.file_label.setText(f"Archivo cargado: {file_path.split('/')[-1]}")

                # Habilitamos el botón de exportación
                self.export_pdf_button.setEnabled(True)

                # Calculamos la duración y actualizamos las pestañas
                self.analyze_time_data()
                self.status_bar.showMessage("Archivo cargado exitosamente", 3000)

            except Exception as e:
                self.status_bar.clearMessage()
                QMessageBox.critical(self, "Error", f"Error al cargar el archivo: {str(e)}")

    def analyze_time_data(self):
        """Realiza el análisis de tiempos y actualiza las pestañas"""
        if self.df is None:
            return

        try:
            # Actualizamos el status bar
            self.status_bar.showMessage("Analizando datos...")

            # Calculamos la duración de cada servicio
            self.df = calculate_service_duration(self.df)

            # Actualizamos cada pestaña
            update_summary_tab(self.summary_layout, self.df)
            update_technician_tab(self.tech_layout, self.df)
            update_terminal_model_tab(self.terminal_layout, self.df)
            update_anomalies_tab(self.anomaly_layout, self.df)

            self.status_bar.showMessage("Análisis completado", 3000)

        except Exception as e:
            self.status_bar.clearMessage()
            QMessageBox.warning(self, "Advertencia", f"Error en el análisis: {str(e)}")

    def export_to_pdf(self):
        """Exporta los análisis a un archivo PDF"""
        if self.df is None or 'Duración (minutos)' not in self.df.columns:
            QMessageBox.warning(self, "Advertencia", "No hay datos para exportar")
            return

        # Seleccionar ubicación para guardar el PDF
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Informe PDF", "", "Archivos PDF (*.pdf)"
        )

        if output_path:
            # Si no tiene extensión .pdf, la añadimos
            if not output_path.lower().endswith('.pdf'):
                output_path += '.pdf'

            # Actualizamos el status bar
            self.status_bar.showMessage("Generando informe PDF...")

            # Deshabilitamos los botones durante la exportación
            self.export_pdf_button.setEnabled(False)
            self.load_button.setEnabled(False)

            # Creamos un thread para la exportación
            self.pdf_thread = PDFExportThread(self.df, output_path)
            self.pdf_thread.finished.connect(self.pdf_export_finished)
            self.pdf_thread.error.connect(self.pdf_export_error)
            self.pdf_thread.start()

    def pdf_export_finished(self, output_path):
        """Callback cuando la exportación PDF ha terminado"""
        # Habilitamos los botones nuevamente
        self.export_pdf_button.setEnabled(True)
        self.load_button.setEnabled(True)

        # Actualizamos el status bar
        self.status_bar.showMessage(f"PDF guardado en {output_path}", 5000)

        # Mostramos un mensaje de éxito
        QMessageBox.information(self, "Exportación Exitosa",
                                f"El informe PDF ha sido generado exitosamente y guardado en:\n{output_path}")

    def pdf_export_error(self, error_msg):
        """Callback cuando hay un error en la exportación PDF"""
        # Habilitamos los botones nuevamente
        self.export_pdf_button.setEnabled(True)
        self.load_button.setEnabled(True)

        # Limpiamos el status bar
        self.status_bar.clearMessage()

        # Mostramos un mensaje de error
        QMessageBox.critical(self, "Error de Exportación",
                             f"Ocurrió un error al generar el PDF:\n{error_msg}")