# pdf_generator.py
# Módulo para generar reportes PDF con diseño técnico y profesional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
import os
from datetime import datetime


def generate_pdf_report(data, output_path):
    """
    Genera un reporte en PDF con diseño técnico mejorado y profesional

    Args:
        data: Diccionario con datos procesados organizados por oficial técnico
        output_path: Ruta donde se guardará el archivo PDF
    """
    # Crear el documento PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    # Contenedor para los elementos del PDF
    elements = []

    # Estilos personalizados
    styles = getSampleStyleSheet()

    # Estilo de título principal con color técnico
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#2C3E50'),  # Azul oscuro profesional
        alignment=TA_CENTER,
        spaceAfter=12
    )

    # Estilo de subtítulo
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#34495E'),  # Gris azulado
        alignment=TA_LEFT,
        spaceAfter=6
    )

    # Estilo para información general
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#2C3E50'),
        alignment=TA_LEFT
    )

    # Estilo para notas
    note_style = ParagraphStyle(
        'NoteStyle',
        parent=styles['Italic'],
        fontSize=9,
        textColor=colors.HexColor('#7F8C8D'),  # Gris más suave
        alignment=TA_LEFT
    )

    # Añadir título del reporte
    report_title = Paragraph("Reporte de Tiempos de Estadía", title_style)
    elements.append(report_title)
    elements.append(Spacer(1, 0.25 * inch))

    # Añadir fecha y hora de generación
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    date_text = Paragraph(f"Generado el: {now}", info_style)
    elements.append(date_text)
    elements.append(Spacer(1, 0.25 * inch))

    # Añadir nota sobre anomalías con estilo técnico
    anomaly_note = Paragraph(
        "Nota: Las anomalías (tiempos negativos) se muestran en rojo para identificación rápida. No se incluyen en cálculos estadísticos.",
        note_style
    )
    elements.append(anomaly_note)
    elements.append(Spacer(1, 0.25 * inch))

    # Para cada oficial técnico, generar una sección con sus datos
    for officer, officer_data in data.items():
        # Título de la sección (nombre del oficial)
        section_title = Paragraph(f"Oficial Técnico: {officer}", subtitle_style)
        elements.append(section_title)
        elements.append(Spacer(1, 0.1 * inch))

        # Resumen de estadísticas con diseño de tabla más técnico
        # Añadimos manejo de errores para cada clave
        statistics = [
            ["Métrica", "Valor"],
            ["Total de registros", str(officer_data.get('total_records', 0))],
            ["Registros válidos", str(officer_data.get('valid_records', 0))],
            ["Registros con anomalías",
             str(officer_data.get('total_records', 0) - officer_data.get('valid_records', 0))],
            ["Tiempo total (solo válidos)", officer_data.get('total_time', 'N/A')],
            ["Tiempo promedio (solo válidos)", officer_data.get('avg_time', 'N/A')]
        ]

        # Tabla de estadísticas con estilo técnico
        stats_table = Table(statistics, colWidths=[2.5 * inch, 3 * inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2980B9')),  # Azul header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ECF0F1')),  # Gris claro para primera columna
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7'))  # Gris para bordes
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 0.2 * inch))

        # Datos detallados
        records = officer_data.get('records', [])
        if records:
            # Encabezados de tabla con estilo técnico
            table_headers = [
                "Hora de llegada", "Hora de salida", "Tiempo de estadía"
            ]

            # Datos de la tabla
            table_data = [table_headers]
            for record in records:
                llegada = record.get('Hora de llegada', 'N/A').strftime("%d/%m/%Y %H:%M:%S") if hasattr(
                    record.get('Hora de llegada'), 'strftime') else str(record.get('Hora de llegada', 'N/A'))
                salida = record.get('Hora de salida', 'N/A').strftime("%d/%m/%Y %H:%M:%S") if hasattr(
                    record.get('Hora de salida'), 'strftime') else str(record.get('Hora de salida', 'N/A'))
                estadia = record.get('Tiempo de estadía', 'N/A')

                table_data.append([llegada, salida, estadia])

            # Crear tabla
            detail_table = Table(table_data, colWidths=[2 * inch, 2 * inch, 2 * inch])

            # Estilo de tabla técnico
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),  # Azul header
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#95A5A6'))  # Gris para bordes
            ]

            # Colores alternados y resaltar anomalías
            for i, record in enumerate(records, 1):
                # Usar .get() con un valor predeterminado para evitar errores
                es_tiempo_valido = record.get('Es tiempo válido', True)

                if not es_tiempo_valido:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F1948A')))  # Rojo suave
                    table_style.append(('TEXTCOLOR', (2, i), (2, i), colors.darkred))
                else:
                    bg_color = colors.HexColor('#F2F4F6') if i % 2 == 0 else colors.white
                    table_style.append(('BACKGROUND', (0, i), (-1, i), bg_color))

            detail_table.setStyle(TableStyle(table_style))
            elements.append(detail_table)

        # Espaciador entre secciones
        elements.append(Spacer(1, 0.5 * inch))

    # Generar el PDF
    doc.build(elements)

    return output_path