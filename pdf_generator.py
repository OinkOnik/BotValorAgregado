# pdf_generator.py
# Módulo para generar reportes PDF con datos procesados de Excel

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from datetime import datetime


def generate_pdf_report(data, output_path):
    """
    Genera un reporte en PDF con los datos procesados

    Args:
        data: Diccionario con datos procesados organizados por oficial técnico
        output_path: Ruta donde se guardará el archivo PDF
    """
    # Crear el documento PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Contenedor para los elementos del PDF
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']

    # Crear estilo para encabezados de tabla
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        alignment=1,  # Centrado
        spaceAfter=10
    )

    # Añadir título del reporte
    report_title = Paragraph("Reporte de Tiempos de Estadía", title_style)
    elements.append(report_title)
    elements.append(Spacer(1, 0.25 * inch))

    # Añadir fecha y hora de generación
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    date_text = Paragraph(f"Generado el: {now}", normal_style)
    elements.append(date_text)
    elements.append(Spacer(1, 0.25 * inch))

    # Para cada oficial técnico, generar una sección con sus datos
    for officer, officer_data in data.items():
        # Título de la sección (nombre del oficial)
        section_title = Paragraph(f"Oficial Técnico: {officer}", subtitle_style)
        elements.append(section_title)
        elements.append(Spacer(1, 0.1 * inch))

        # Resumen de estadísticas
        statistics = [
            ["Total de registros:", str(officer_data['total_records'])],
            ["Tiempo total:", officer_data['total_time']],
            ["Tiempo promedio:", officer_data['avg_time']]
        ]

        # Tabla de estadísticas
        stats_table = Table(statistics, colWidths=[2 * inch, 3 * inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 0.2 * inch))

        # Datos detallados
        if officer_data['records']:
            # Encabezados de tabla
            table_headers = [
                [
                    Paragraph("Hora de llegada", header_style),
                    Paragraph("Hora de salida", header_style),
                    Paragraph("Tiempo de estadía", header_style)
                ]
            ]

            # Datos de la tabla
            table_data = []
            for record in officer_data['records']:
                llegada = record['Hora de llegada'].strftime("%d/%m/%Y %H:%M:%S")
                salida = record['Hora de salida'].strftime("%d/%m/%Y %H:%M:%S")
                estadia = record['Tiempo de estadía']

                table_data.append([llegada, salida, estadia])

            # Combinar encabezados y datos
            all_data = table_headers + table_data

            # Crear tabla
            detail_table = Table(all_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
            detail_table.setStyle(TableStyle([
                # Estilo para los encabezados
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),

                # Estilo para los datos
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                # Bordes y colores alternados en filas
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            elements.append(detail_table)

        # Espaciador entre secciones
        elements.append(Spacer(1, 0.5 * inch))

    # Generar el PDF
    doc.build(elements)

    return output_path