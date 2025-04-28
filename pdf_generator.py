# pdf_generator.py
# Generador de informes PDF a partir de análisis de datos
# Crea un informe PDF completo con todas las secciones de análisis

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import tempfile
import os
import pandas as pd
from pdf_charts import (add_duration_histogram, add_technician_chart,
                       add_terminal_model_chart, add_anomalies_chart)
from time_analyzer import (calculate_service_duration,
                          get_average_duration_by_technician,
                          get_average_duration_by_terminal_model,
                          identify_anomalies)

class PDFGenerator:
    """
    Clase para generar informes PDF a partir de análisis de datos.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Crear un estilo personalizado para títulos
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            alignment=TA_CENTER,
            fontSize=16,
            spaceAfter=12
        )
        # Estilo para subtítulos
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10
        )
        # Estilo para texto normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )

    def create_pdf_report(self, df, output_path=None):
        """
        Crea un informe PDF completo con todos los análisis.

        Args:
            df: DataFrame con los datos analizados
            output_path: Ruta donde guardar el PDF, si es None se usa un diálogo

        Returns:
            str: Ruta del archivo PDF generado
        """
        if output_path is None:
            # Crear un nombre de archivo temporal con fecha y hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(tempfile.gettempdir(), f"analisis_tiempos_{timestamp}.pdf")

        # Crear el documento
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=72
        )

        # Lista de elementos que van en el PDF
        elements = []

        # Título principal del informe
        elements.append(Paragraph("Informe de Análisis de Tiempos de Servicio", self.title_style))
        elements.append(Spacer(1, 0.25 * inch))

        # Fecha del informe
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Generado el: {fecha_actual}", self.normal_style))
        elements.append(Spacer(1, 0.25 * inch))

        # Agregar las secciones del informe
        self._add_summary_section(elements, df)
        self._add_technician_section(elements, df)
        self._add_terminal_model_section(elements, df)
        self._add_anomalies_section(elements, df)

        # Generar el PDF
        doc.build(elements)

        return output_path

    def _add_summary_section(self, elements, df):
        """Agrega la sección de resumen al informe"""
        # Asegurarse de que el DataFrame tenga calculada la duración
        if 'Duración (minutos)' not in df.columns:
            try:
                df = calculate_service_duration(df)
            except:
                elements.append(
                    Paragraph("Error: No se pudo calcular la duración de los servicios.", self.normal_style))
                return

        # Título de la sección
        elements.append(Paragraph("1. Resumen General", self.subtitle_style))
        elements.append(Spacer(1, 0.1 * inch))

        # Estadísticas básicas
        total_services = len(df)
        avg_duration = df['Duración (minutos)'].mean()
        min_duration = df['Duración (minutos)'].min()
        max_duration = df['Duración (minutos)'].max()
        std_duration = df['Duración (minutos)'].std()

        # Texto del resumen
        elements.append(Paragraph(f"Total de servicios analizados: {total_services}", self.normal_style))
        elements.append(Paragraph(f"Duración promedio: {avg_duration:.2f} minutos", self.normal_style))
        elements.append(Paragraph(f"Duración mínima: {min_duration:.2f} minutos", self.normal_style))
        elements.append(Paragraph(f"Duración máxima: {max_duration:.2f} minutos", self.normal_style))
        elements.append(Paragraph(f"Desviación estándar: {std_duration:.2f} minutos", self.normal_style))
        elements.append(Spacer(1, 0.15 * inch))

        # Crear un histograma de duración
        add_duration_histogram(elements, df)

        elements.append(Spacer(1, 0.25 * inch))

    def _add_technician_section(self, elements, df):
        """Agrega la sección de análisis por técnico al informe"""
        if 'Duración (minutos)' not in df.columns or 'Nombre del oficial técnico que brinda servicio' not in df.columns:
            elements.append(
                Paragraph("Error: Faltan columnas necesarias para el análisis por técnico.", self.normal_style))
            return

        # Título de la sección
        elements.append(Paragraph("2. Análisis por Técnico", self.subtitle_style))
        elements.append(Spacer(1, 0.1 * inch))

        try:
            # Obtener los datos por técnico
            tech_data = get_average_duration_by_technician(df)

            # Crear una tabla con los datos (top 10)
            tech_data_sorted = tech_data.sort_values('Promedio (min)', ascending=True)
            top_n = min(10, len(tech_data_sorted))

            data = [["Técnico", "Promedio (min)", "Cantidad", "Mínimo (min)", "Máximo (min)"]]

            for _, row in tech_data_sorted.head(top_n).iterrows():
                data.append([
                    row['Técnico'],
                    f"{row['Promedio (min)']:.2f}",
                    str(row['Cantidad']),
                    f"{row['Mínimo (min)']:.2f}",
                    f"{row['Máximo (min)']:.2f}"
                ])

            table = Table(data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(Paragraph("Top 10 técnicos por duración promedio:", self.normal_style))
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(table)
            elements.append(Spacer(1, 0.2 * inch))

            # Crear un gráfico de barras
            add_technician_chart(elements, tech_data_sorted)

        except Exception as e:
            elements.append(Paragraph(f"Error al procesar datos: {str(e)}", self.normal_style))

        elements.append(Spacer(1, 0.25 * inch))

    def _add_terminal_model_section(self, elements, df):
        """Agrega la sección de análisis por modelo de terminal al informe"""
        if 'Duración (minutos)' not in df.columns:
            elements.append(
                Paragraph("Error: Faltan columnas necesarias para el análisis por modelo.", self.normal_style))
            return

        # Título de la sección
        elements.append(Paragraph("3. Análisis por Modelo de Terminal", self.subtitle_style))
        elements.append(Spacer(1, 0.1 * inch))

        try:
            # Obtener los datos por modelo de terminal
            terminal_data = get_average_duration_by_terminal_model(df)

            # Crear una tabla con los datos (top 10)
            terminal_data_sorted = terminal_data.sort_values('Promedio (min)', ascending=True)
            top_n = min(10, len(terminal_data_sorted))

            data = [["Modelo de Terminal", "Promedio (min)", "Cantidad", "Mínimo (min)", "Máximo (min)"]]

            for _, row in terminal_data_sorted.head(top_n).iterrows():
                data.append([
                    row['Modelo de Terminal'],
                    f"{row['Promedio (min)']:.2f}",
                    str(row['Cantidad']),
                    f"{row['Mínimo (min)']:.2f}",
                    f"{row['Máximo (min)']:.2f}"
                ])

            table = Table(data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(Paragraph("Top 10 modelos de terminal por duración promedio:", self.normal_style))
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(table)
            elements.append(Spacer(1, 0.2 * inch))

            # Crear un gráfico de barras
            add_terminal_model_chart(elements, terminal_data_sorted)

        except Exception as e:
            elements.append(Paragraph(f"Error al procesar datos: {str(e)}", self.normal_style))

        elements.append(Spacer(1, 0.25 * inch))

    def _add_anomalies_section(self, elements, df):
        """Agrega la sección de anomalías al informe"""
        if 'Duración (minutos)' not in df.columns:
            elements.append(
                Paragraph("Error: Faltan columnas necesarias para el análisis de anomalías.", self.normal_style))
            return

        # Título de la sección
        elements.append(Paragraph("4. Análisis de Anomalías", self.subtitle_style))
        elements.append(Spacer(1, 0.1 * inch))

        try:
            # Obtener las anomalías
            anomalies_df = identify_anomalies(df)

            # Información básica sobre anomalías
            total_anomalies = len(anomalies_df)
            anomaly_percent = (total_anomalies / len(df)) * 100 if len(df) > 0 else 0

            elements.append(
                Paragraph(f"Total de anomalías detectadas: {total_anomalies} ({anomaly_percent:.2f}% del total)",
                          self.normal_style))

            # Conteo por tipo de anomalía
            counts = anomalies_df['Tipo de Anomalía'].value_counts()

            for anomaly_type, count in counts.items():
                elements.append(Paragraph(f"- {anomaly_type}: {count} servicios", self.normal_style))

            elements.append(Spacer(1, 0.15 * inch))

            # Mostrar algunas anomalías (límite a 10 para no hacer el PDF muy largo)
            if total_anomalies > 0:
                elements.append(Paragraph("Muestra de servicios anómalos:", self.normal_style))
                elements.append(Spacer(1, 0.1 * inch))

                # Filtrar columnas relevantes
                relevant_columns = [
                    'Nombre del Afiliado', 'Nombre del oficial técnico que brinda servicio',
                    'Hora de llegada', 'Hora de salida', 'Duración (minutos)', 'Tipo de Anomalía'
                ]

                # Seleccionar columnas que existen en el DataFrame
                available_columns = [col for col in relevant_columns if col in anomalies_df.columns]

                # Si no hay suficientes columnas, usar las primeras 5
                if len(available_columns) < 3:
                    available_columns = list(anomalies_df.columns[:min(5, len(anomalies_df.columns))])

                # Crear la tabla de anomalías
                anomalies_sample = anomalies_df[available_columns].head(10)

                # Preparar los datos para la tabla
                table_data = [available_columns]  # Encabezados

                for _, row in anomalies_sample.iterrows():
                    table_row = []
                    for col in available_columns:
                        value = row[col]
                        # Formatear fechas y números
                        if pd.api.types.is_datetime64_dtype(anomalies_sample[col]):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        elif pd.api.types.is_numeric_dtype(anomalies_sample[col]):
                            value = f"{value:.2f}" if isinstance(value, float) else str(value)
                        else:
                            value = str(value)
                        table_row.append(value)
                    table_data.append(table_row)

                # Crear la tabla
                anomaly_table = Table(table_data, repeatRows=1)
                anomaly_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))

                elements.append(anomaly_table)
                elements.append(Spacer(1, 0.2 * inch))

                # Gráfico de anomalías
                add_anomalies_chart(elements, anomalies_df)

        except Exception as e:
            elements.append(Paragraph(f"Error al procesar anomalías: {str(e)}", self.normal_style))