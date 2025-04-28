#gui_time_analysis.py

import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFileDialog, QTabWidget, QTableWidget,
                             QTableWidgetItem, QMessageBox, QScrollArea)
from PyQt5.QtCore import Qt


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
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        # Tabs para diferentes análisis
        self.tabs = QTabWidget()

        # Tab de resumen
        self.summary_tab = QWidget()
        self.summary_layout = QVBoxLayout(self.summary_tab)
        self.tabs.addTab(self.summary_tab, "Resumen")

        # Tab de análisis por técnico
        self.tech_tab = QScrollArea()
        self.tech_tab.setWidgetResizable(True)
        self.tech_content = QWidget()
        self.tech_layout = QVBoxLayout(self.tech_content)
        self.tech_tab.setWidget(self.tech_content)
        self.tabs.addTab(self.tech_tab, "Por Técnico")

        # Tab de análisis por modelo de terminal
        self.terminal_tab = QScrollArea()
        self.terminal_tab.setWidgetResizable(True)
        self.terminal_content = QWidget()
        self.terminal_layout = QVBoxLayout(self.terminal_content)
        self.terminal_tab.setWidget(self.terminal_content)
        self.tabs.addTab(self.terminal_tab, "Por Modelo de Terminal")

        # Tab de anomalías
        self.anomaly_tab = QScrollArea()
        self.anomaly_tab.setWidgetResizable(True)
        self.anomaly_content = QWidget()
        self.anomaly_layout = QVBoxLayout(self.anomaly_content)
        self.anomaly_tab.setWidget(self.anomaly_content)
        self.tabs.addTab(self.anomaly_tab, "Anomalías")

        main_layout.addWidget(self.tabs)

    def load_excel_file(self):
        """Carga un archivo Excel seleccionado por el usuario"""
        from data_loader import load_excel_file, clean_time_data

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Archivo Excel", "", "Archivos Excel (*.xlsx *.xls)"
        )

        if file_path:
            try:
                # Cargamos el archivo
                self.df = load_excel_file(file_path)

                # Limpiamos los datos de tiempo
                self.df = clean_time_data(self.df)

                # Actualizamos la etiqueta con el nombre del archivo
                self.file_label.setText(f"Archivo cargado: {file_path.split('/')[-1]}")

                # Calculamos la duración y actualizamos las pestañas
                self.analyze_time_data()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar el archivo: {str(e)}")

    def analyze_time_data(self):
        """Realiza el análisis de tiempos y actualiza las pestañas"""
        from time_analyzer import calculate_service_duration

        if self.df is None:
            return

        try:
            # Calculamos la duración de cada servicio
            self.df = calculate_service_duration(self.df)

            # Actualizamos cada pestaña
            self.update_summary_tab()
            self.update_technician_tab()
            self.update_terminal_model_tab()
            self.update_anomalies_tab()

        except Exception as e:
            QMessageBox.warning(self, "Advertencia", f"Error en el análisis: {str(e)}")

    def update_summary_tab(self):
        """Actualiza la pestaña de resumen con estadísticas generales"""
        # Limpiamos el layout
        self.clear_layout(self.summary_layout)

        if self.df is None or 'Duración (minutos)' not in self.df.columns:
            return

        # Calculamos estadísticas básicas
        total_services = len(self.df)
        avg_duration = self.df['Duración (minutos)'].mean()
        min_duration = self.df['Duración (minutos)'].min()
        max_duration = self.df['Duración (minutos)'].max()

        # Creamos un widget para mostrar las estadísticas
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)

        stats_layout.addWidget(QLabel(f"<h2>Estadísticas de Tiempos de Servicio</h2>"))
        stats_layout.addWidget(QLabel(f"<b>Total de servicios:</b> {total_services}"))
        stats_layout.addWidget(QLabel(f"<b>Duración promedio:</b> {avg_duration:.2f} minutos"))
        stats_layout.addWidget(QLabel(f"<b>Duración mínima:</b> {min_duration:.2f} minutos"))
        stats_layout.addWidget(QLabel(f"<b>Duración máxima:</b> {max_duration:.2f} minutos"))

        self.summary_layout.addWidget(stats_widget)

        # Creamos un histograma de duración
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        ax.hist(self.df['Duración (minutos)'].dropna(), bins=20, alpha=0.7, color='blue')
        ax.set_title('Distribución de Tiempos de Servicio')
        ax.set_xlabel('Duración (minutos)')
        ax.set_ylabel('Frecuencia')
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.tight_layout()

        canvas = FigureCanvas(fig)
        self.summary_layout.addWidget(canvas)

        self.summary_layout.addStretch()

    def update_technician_tab(self):
        """Actualiza la pestaña de análisis por técnico"""
        # Limpiamos el layout
        self.clear_layout(self.tech_layout)

        # Cambiamos para usar 'Nombre del oficial técnico que brinda servicio'
        if self.df is None or 'Duración (minutos)' not in self.df.columns or 'Nombre del oficial técnico que brinda servicio' not in self.df.columns:
            self.tech_layout.addWidget(QLabel("No hay datos disponibles o faltan columnas necesarias"))
            return

        from time_analyzer import get_average_duration_by_technician

        try:
            # Obtenemos los datos por técnico
            tech_data = get_average_duration_by_technician(self.df)

            # Creamos la tabla
            table = self.create_table_from_dataframe(tech_data)
            self.tech_layout.addWidget(QLabel("<h2>Duración Promedio por Técnico</h2>"))
            self.tech_layout.addWidget(table)

            # Creamos un gráfico de barras
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            # Ordenamos por promedio para el gráfico
            tech_data_sorted = tech_data.sort_values('Promedio (min)', ascending=False)
            top_n = min(10, len(tech_data_sorted))  # Mostrar top 10 o menos

            bars = ax.bar(tech_data_sorted['Técnico'].head(top_n),
                          tech_data_sorted['Promedio (min)'].head(top_n),
                          alpha=0.7)

            # Añadimos etiquetas
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.,
                        height + 1,
                        f'{height:.1f}',
                        ha='center', va='bottom', rotation=0)

            ax.set_title('Duración Promedio por Técnico (Top 10)')
            ax.set_xlabel('Técnico')
            ax.set_ylabel('Duración Promedio (minutos)')
            ax.grid(True, linestyle='--', alpha=0.7)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            fig.tight_layout()

            canvas = FigureCanvas(fig)
            self.tech_layout.addWidget(canvas)

        except Exception as e:
            self.tech_layout.addWidget(QLabel(f"Error al procesar datos: {str(e)}"))

        self.tech_layout.addStretch()

    def update_terminal_model_tab(self):
        """Actualiza la pestaña de análisis por modelo de terminal"""
        # Limpiamos el layout
        self.clear_layout(self.terminal_layout)

        if self.df is None or 'Duración (minutos)' not in self.df.columns:
            self.terminal_layout.addWidget(QLabel("No hay datos disponibles o faltan columnas necesarias"))
            return

        from time_analyzer import get_average_duration_by_terminal_model

        try:
            # Obtenemos los datos por modelo de terminal
            terminal_data = get_average_duration_by_terminal_model(self.df)

            # Creamos la tabla
            table = self.create_table_from_dataframe(terminal_data)
            self.terminal_layout.addWidget(QLabel("<h2>Duración Promedio por Modelo de Terminal</h2>"))
            self.terminal_layout.addWidget(table)

            # Creamos un gráfico de barras
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            # Ordenamos por promedio para el gráfico
            terminal_data_sorted = terminal_data.sort_values('Promedio (min)', ascending=False)
            top_n = min(10, len(terminal_data_sorted))  # Mostrar top 10 o menos

            bars = ax.bar(terminal_data_sorted['Modelo de Terminal'].head(top_n),
                          terminal_data_sorted['Promedio (min)'].head(top_n),
                          alpha=0.7,
                          color='purple')

            # Añadimos etiquetas
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.,
                        height + 1,
                        f'{height:.1f}',
                        ha='center', va='bottom', rotation=0)

            ax.set_title('Duración Promedio por Modelo de Terminal (Top 10)')
            ax.set_xlabel('Modelo de Terminal')
            ax.set_ylabel('Duración Promedio (minutos)')
            ax.grid(True, linestyle='--', alpha=0.7)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            fig.tight_layout()

            canvas = FigureCanvas(fig)
            self.terminal_layout.addWidget(canvas)

        except Exception as e:
            self.terminal_layout.addWidget(QLabel(f"Error al procesar datos: {str(e)}"))

        self.terminal_layout.addStretch()

    def update_anomalies_tab(self):
        """Actualiza la pestaña de anomalías"""
        # Limpiamos el layout
        self.clear_layout(self.anomaly_layout)

        if self.df is None or 'Duración (minutos)' not in self.df.columns:
            self.anomaly_layout.addWidget(QLabel("No hay datos disponibles o faltan columnas necesarias"))
            return

        from time_analyzer import identify_anomalies

        try:
            # Obtenemos las anomalías
            anomalies_df = identify_anomalies(self.df)

            # Filtramos columnas relevantes para la tabla
            relevant_columns = [
                'Nombre del Afiliado', 'Nombre del oficial técnico que brinda servicio',
                'Hora de llegada', 'Hora de salida', 'Duración (minutos)', 'Tipo de Anomalía'
            ]

            # Filtramos solo las columnas que existen en el DataFrame
            filtered_columns = [col for col in relevant_columns if col in anomalies_df.columns]

            # Si no hay columnas relevantes, usamos todas
            if not filtered_columns:
                filtered_columns = anomalies_df.columns

            anomalies_display = anomalies_df[filtered_columns].copy()

            # Creamos la tabla
            table = self.create_table_from_dataframe(anomalies_display)

            self.anomaly_layout.addWidget(QLabel("<h2>Servicios con Duraciones Anómalas</h2>"))
            self.anomaly_layout.addWidget(QLabel(f"Total de anomalías detectadas: {len(anomalies_df)}"))
            self.anomaly_layout.addWidget(table)

            # Creamos un gráfico de dispersión
            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            # Colores para cada tipo de anomalía
            colors = {'Corta': 'blue', 'Larga': 'red', 'Normal': 'green'}

            # Aplanamos los índices para el gráfico
            x = range(len(anomalies_df))

            for anomaly_type in anomalies_df['Tipo de Anomalía'].unique():
                mask = anomalies_df['Tipo de Anomalía'] == anomaly_type
                filtered_indices = [i for i, m in zip(x, mask) if m]
                filtered_durations = anomalies_df.loc[mask, 'Duración (minutos)'].values

                if len(filtered_indices) > 0:
                    ax.scatter(
                        filtered_indices,
                        filtered_durations,
                        c=colors.get(anomaly_type, 'gray'),
                        label=anomaly_type,
                        alpha=0.7
                    )

            ax.set_title('Distribución de Anomalías')
            ax.set_xlabel('Índice de Servicio')
            ax.set_ylabel('Duración (minutos)')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()
            fig.tight_layout()

            canvas = FigureCanvas(fig)
            self.anomaly_layout.addWidget(canvas)

        except Exception as e:
            self.anomaly_layout.addWidget(QLabel(f"Error al procesar anomalías: {str(e)}"))

        self.anomaly_layout.addStretch()

    def create_table_from_dataframe(self, df):
        """Crea una tabla a partir de un DataFrame"""
        # Crear la tabla
        table = QTableWidget()

        # Configurar el número de filas y columnas
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))

        # Configurar los encabezados
        table.setHorizontalHeaderLabels(df.columns)

        # Llenar la tabla con datos
        for i in range(len(df)):
            for j in range(len(df.columns)):
                value = df.iloc[i, j]

                # Formatear valores numéricos
                if isinstance(value, (int, float)):
                    if j > 0:  # Las columnas después de la primera son numéricas
                        item = QTableWidgetItem(f"{value:.2f}")
                    else:
                        item = QTableWidgetItem(str(value))
                else:
                    item = QTableWidgetItem(str(value))

                # Alineación al centro
                item.setTextAlignment(Qt.AlignCenter)

                table.setItem(i, j, item)

        # Ajustar el tamaño de las columnas al contenido
        table.resizeColumnsToContents()

        return table

    def clear_layout(self, layout):
        """Limpia un layout eliminando todos sus widgets"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())