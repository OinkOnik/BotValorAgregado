# pdf_generator.py
# Módulo para generar reportes PDF con datos procesados de Excel

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
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
    subsubtitle_style = ParagraphStyle(
        'SubSubTitle',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=6
    )
    normal_style = styles['Normal']
    note_style = ParagraphStyle(
        'NoteStyle',
        parent=styles['Italic'],
        fontSize=9,
        textColor=colors.darkblue
    )

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

    # Añadir nota sobre anomalías
    anomaly_note = Paragraph(
        "Nota: Las anomalías (tiempos negativos) se muestran en los registros pero no se incluyen en los cálculos de tiempo total y promedio.",
        note_style
    )
    elements.append(anomaly_note)
    elements.append(Spacer(1, 0.25 * inch))

    # Verificar si existe el análisis de afiliados
    if 'afiliados_analysis' in data:
        # Agregar sección de análisis de afiliados con problemas
        add_affiliates_analysis_section(elements, data['afiliados_analysis'],
                                        subtitle_style, subsubtitle_style,
                                        normal_style, header_style)

        # Eliminar el análisis de afiliados del diccionario para que no interfiera con el bucle de oficiales
        afiliados_data = data.pop('afiliados_analysis')

        # Añadir un salto de página después del análisis de afiliados
        elements.append(Spacer(1, 0.5 * inch))

    # Para cada oficial técnico, generar una sección con sus datos
    for officer, officer_data in data.items():
        # Título de la sección (nombre del oficial)
        section_title = Paragraph(f"Oficial Técnico: {officer}", subtitle_style)
        elements.append(section_title)
        elements.append(Spacer(1, 0.1 * inch))

        # Resumen de estadísticas
        statistics = [
            ["Total de registros:", str(officer_data['total_records'])],
            ["Registros válidos:", str(officer_data['valid_records'])],
            ["Registros con anomalías:", str(officer_data['total_records'] - officer_data['valid_records'])],
            ["Tiempo total (solo válidos):", officer_data['total_time']],
            ["Tiempo promedio (solo válidos):", officer_data['avg_time']]
        ]

        # Tabla de estadísticas
        stats_table = Table(statistics, colWidths=[2.5 * inch, 3 * inch])
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

                # Determinar color de fila según si es válido o no
                row_data = [llegada, salida, estadia]
                table_data.append(row_data)

            # Combinar encabezados y datos
            all_data = table_headers + table_data

            # Crear tabla
            detail_table = Table(all_data, colWidths=[2 * inch, 2 * inch, 2 * inch])

            # Base style
            table_style = [
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

                # Bordes
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]

            # Colores alternados para filas normales, color distinto para anomalías
            for i, record in enumerate(officer_data['records'], 1):
                if not record.get('Es tiempo válido', True):
                    table_style.append(('BACKGROUND', (0, i), (-1, i), colors.mistyrose))
                    table_style.append(('TEXTCOLOR', (2, i), (2, i), colors.red))
                else:
                    if i % 2 == 0:
                        table_style.append(('BACKGROUND', (0, i), (-1, i), colors.lightgrey))
                    else:
                        table_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))

            detail_table.setStyle(TableStyle(table_style))
            elements.append(detail_table)

        # Espaciador entre secciones
        elements.append(Spacer(1, 0.5 * inch))

    # Generar el PDF
    doc.build(elements)

    return output_path


def add_affiliates_analysis_section(elements, afiliados_data, subtitle_style,
                                    subsubtitle_style, normal_style, header_style):
    """
    Agrega la sección de análisis de afiliados al reporte PDF

    Args:
        elements: Lista de elementos del PDF
        afiliados_data: Datos del análisis de afiliados
        subtitle_style, etc.: Estilos para el formato
    """
    if not afiliados_data or 'top_afiliados' not in afiliados_data:
        return

    # Título de la sección
    section_title = Paragraph("Análisis de Afiliados con Problemas", subtitle_style)
    elements.append(section_title)
    elements.append(Spacer(1, 0.2 * inch))

    # Descripción
    description = Paragraph(
        f"Esta sección muestra los afiliados que presentan más casos o problemas. "
        f"Se analizaron un total de {afiliados_data['total_afiliados']} afiliados.",
        normal_style
    )
    elements.append(description)
    elements.append(Spacer(1, 0.2 * inch))

    # Para cada afiliado en el top, crear una subsección
    for i, afiliado in enumerate(afiliados_data['top_afiliados']):
        # Mantener junto todo el contenido de un afiliado
        afiliado_elements = []

        # Subtítulo con el nombre del afiliado y el total de casos
        afiliado_title = Paragraph(
            f"{i + 1}. {afiliado['nombre']} ({afiliado['total_casos']} casos)",
            subsubtitle_style
        )
        afiliado_elements.append(afiliado_title)

        # Crear tabla para las razones principales
        if afiliado['razones']:
            # Encabezados
            headers = [["Razón del problema", "Frecuencia"]]

            # Datos de la tabla
            table_data = []
            for razon_info in afiliado['razones']:
                table_data.append([razon_info['razon'], str(razon_info['frecuencia'])])

            # Combinar encabezados y datos
            all_data = headers + table_data

            # Crear tabla
            razones_table = Table(all_data, colWidths=[4 * inch, 1 * inch])

            # Estilo de la tabla
            table_style = [
                # Encabezados
                ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),

                # Datos
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # Centrar frecuencia

                # Bordes
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]

            # Colores alternados para las filas
            for i in range(1, len(all_data)):
                if i % 2 == 0:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), colors.lightgrey))
                else:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))

            razones_table.setStyle(TableStyle(table_style))
            afiliado_elements.append(razones_table)
        else:
            # Si no hay razones, mostrar un mensaje
            no_reasons = Paragraph("No se encontraron razones específicas registradas.", normal_style)
            afiliado_elements.append(no_reasons)

        # Espaciador
        afiliado_elements.append(Spacer(1, 0.15 * inch))

        # Mantener todos los elementos de este afiliado juntos
        elements.append(KeepTogether(afiliado_elements))

    # Espaciador final
    elements.append(Spacer(1, 0.25 * inch))