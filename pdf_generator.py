# pdf_generator.py
"""
Módulo encargado de generar reportes PDF profesionales con diseño técnico avanzado.
Crea documentos estructurados con índice, estadísticas, tablas de datos detallados por oficial técnico
y análisis de respuesta operativa, usando estilos personalizados y elementos gráficos profesionales.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    KeepTogether, ListFlowable, ListItem
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import inch
from datetime import datetime

# Importaciones de los módulos modularizados
from pdf_canvas import NumberedCanvas
from pdf_styles import get_report_styles
from pdf_elements import create_divisor_line, create_statistics_table, create_detail_table, \
    create_operational_data_table


def generate_pdf_report(data, output_path):
    """
    Genera un reporte en PDF con diseño técnico mejorado y profesional

    Args:
        data: Diccionario con datos procesados organizados por oficial técnico
        output_path: Ruta donde se guardará el archivo PDF

    Returns:
        str: Ruta donde se guardó el archivo PDF
    """
    # Crear el documento PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=50,
        bottomMargin=50
    )

    # Contenedor para los elementos del PDF
    elements = []

    # Obtener los estilos para el reporte
    styles = get_report_styles()

    # Añadir título y fecha al reporte
    _add_report_header(elements, styles)

    # Crear el índice de contenidos
    toc = TableOfContents()
    toc.levelStyles = [
        styles['toc1'],
        styles['toc2'],
        styles['toc3']
    ]
    elements.append(Paragraph("Índice de Contenidos", styles['heading1']))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(toc)
    elements.append(PageBreak())

    # Añadir sección de resumen y notas
    _add_summary_section(elements, styles)

    # Añadir sección de análisis de respuesta operativa (NUEVO)
    _add_operational_analysis_section(elements, data, styles)

    # Añadir sección principal de datos
    _add_data_section(elements, data, styles)

    # Generar el PDF con numeración de páginas
    doc.multiBuild(elements, canvasmaker=NumberedCanvas)

    return output_path


def _add_report_header(elements, styles):
    """
    Añade el título y la fecha al reporte

    Args:
        elements: Lista donde se añaden los elementos
        styles: Diccionario con los estilos del reporte
    """
    # Añadir título del reporte
    report_title = Paragraph("Reporte de Tiempos de Estadía", styles['report_title'])
    elements.append(report_title)
    elements.append(Spacer(1, 0.25 * inch))

    # Añadir fecha y hora de generación
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    date_text = Paragraph(f"Generado el: {now}", styles['info'])
    elements.append(date_text)
    elements.append(Spacer(1, 0.25 * inch))


def _add_summary_section(elements, styles):
    """
    Añade la sección de resumen y notas técnicas

    Args:
        elements: Lista donde se añaden los elementos
        styles: Diccionario con los estilos del reporte
    """
    # Usar Paragraph en lugar de ChapterHeader para el título de la sección
    summary_header = Paragraph("Resumen y Notas Técnicas", styles['heading1'])
    elements.append(summary_header)
    elements.append(Spacer(1, 0.2 * inch))

    # Texto de resumen
    summary_text = Paragraph(
        "Este reporte presenta un análisis detallado de los tiempos de estadía registrados para cada oficial técnico, "
        "incluyendo métricas como tiempo total, tiempo promedio y anomalías detectadas en los registros.",
        styles['info']
    )
    elements.append(summary_text)
    elements.append(Spacer(1, 0.15 * inch))

    # Notas técnicas
    notes_title = Paragraph("Notas técnicas:", styles['notes_title'])
    elements.append(notes_title)

    # Lista de notas técnicas
    notes = [
        "Las anomalías (tiempos negativos) se muestran en rojo para identificación rápida.",
        "Los registros con anomalías no se incluyen en los cálculos estadísticos.",
        "El tiempo promedio se calcula utilizando únicamente registros válidos (tiempos positivos)."
    ]

    # Crear lista de notas técnicas
    _add_notes_list(elements, notes, styles)

    elements.append(Spacer(1, 0.3 * inch))

    # Agregar una línea divisoria antes de los datos
    divisor = create_divisor_line()
    elements.append(divisor)
    elements.append(Spacer(1, 0.3 * inch))


def _add_operational_analysis_section(elements, data, styles):
    """
    Añade la sección de análisis de respuesta operativa con todos los afiliados

    Args:
        elements: Lista donde se añaden los elementos
        data: Diccionario con los datos procesados
        styles: Diccionario con los estilos del reporte
    """
    # Usar Paragraph en lugar de ChapterHeader para el título de la sección
    operational_header = Paragraph("Análisis de la Respuesta Operativa", styles['heading1'])
    elements.append(operational_header)
    elements.append(Spacer(1, 0.2 * inch))

    # Texto de introducción para la sección
    intro_text = Paragraph(
        "A continuación se presentan los datos relacionados con los afiliados y sus fechas de reporte "
        "para este análisis de respuesta operativa.",
        styles['info']
    )
    elements.append(intro_text)
    elements.append(Spacer(1, 0.2 * inch))

    # Extraer la lista de afiliados
    operational_data = data.get('operational_data', {})
    affiliates_list = operational_data.get('affiliates', [])

    if not affiliates_list:
        # Si no hay afiliados, agregar un mensaje
        no_data_text = Paragraph("No se encontraron datos de afiliados en el archivo Excel.", styles['info'])
        elements.append(no_data_text)
    else:
        # Crear datos para la tabla
        table_data = [["Nombre del Afiliado", "Fecha de Reporte"]]

        # Agregar cada afiliado a la tabla
        for affiliate in affiliates_list:
            nombre_afiliado = affiliate.get('Nombre del Afiliado', 'No especificado')
            fecha_reporte = affiliate.get('Fecha de Reporte', 'No especificada')
            table_data.append([nombre_afiliado, fecha_reporte])

        # Crear tabla con los datos operativos
        table = create_operational_data_table(table_data)
        elements.append(table)

    elements.append(Spacer(1, 0.3 * inch))

    # Agregar una línea divisoria antes de la siguiente sección
    divisor = create_divisor_line()
    elements.append(divisor)
    elements.append(Spacer(1, 0.3 * inch))


def _add_notes_list(elements, notes, styles):
    """
    Añade una lista de notas al reporte

    Args:
        elements: Lista donde se añaden los elementos
        notes: Lista de notas a añadir
        styles: Diccionario con los estilos del reporte
    """
    notes_items = []
    for note in notes:
        notes_items.append(ListItem(Paragraph(note, styles['note'])))

    notes_list = ListFlowable(
        notes_items,
        bulletType='bullet',
        leftIndent=20,
        bulletFontName='Helvetica',
        bulletFontSize=8
    )
    elements.append(notes_list)


def _add_data_section(elements, data, styles):
    """
    Añade la sección principal de datos con información de cada oficial técnico

    Args:
        elements: Lista donde se añaden los elementos
        data: Diccionario con los datos de los oficiales
        styles: Diccionario con los estilos del reporte
    """
    # Usar Paragraph en lugar de ChapterHeader para el título de la sección
    data_header = Paragraph("Datos de Tiempos por Oficial Técnico", styles['heading1'])
    elements.append(data_header)
    elements.append(Spacer(1, 0.3 * inch))

    # Para cada oficial técnico, generar una sección con sus datos
    for i, (officer, officer_data) in enumerate(data.items()):
        # Saltarse la clave 'operational_data' ya que no es un oficial técnico
        if officer == 'operational_data':
            continue

        _add_officer_section(elements, officer, officer_data, styles)

        # Añadir un salto de página después de cada oficial (excepto el último)
        if i < len(data) - 2:  # Restamos 2 para contar con 'operational_data'
            elements.append(PageBreak())


def _add_officer_section(elements, officer, officer_data, styles):
    """
    Añade una sección con los datos de un oficial técnico

    Args:
        elements: Lista donde se añaden los elementos
        officer: Nombre del oficial técnico
        officer_data: Datos del oficial técnico
        styles: Diccionario con los estilos del reporte
    """
    # Título de la sección (nombre del oficial)
    officer_header = Paragraph(f"Oficial Técnico: {officer}", styles['heading2'])
    elements.append(officer_header)
    elements.append(Spacer(1, 0.2 * inch))

    # Añadir estadísticas del oficial
    _add_officer_statistics(elements, officer_data, styles)

    # Añadir registros detallados del oficial
    _add_officer_records(elements, officer_data, styles)


def _add_officer_statistics(elements, officer_data, styles):
    """
    Añade la tabla de estadísticas de un oficial técnico

    Args:
        elements: Lista donde se añaden los elementos
        officer_data: Datos del oficial técnico
        styles: Diccionario con los estilos del reporte
    """
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

    # Subtítulo para la sección de resumen
    stats_title = Paragraph("Resumen de Estadísticas", styles['section'])
    elements.append(stats_title)
    elements.append(Spacer(1, 0.1 * inch))

    # Tabla de estadísticas con estilo técnico
    stats_table = create_statistics_table(statistics)
    elements.append(stats_table)
    elements.append(Spacer(1, 0.2 * inch))


def _add_officer_records(elements, officer_data, styles):
    """
    Añade la tabla de registros detallados de un oficial técnico

    Args:
        elements: Lista donde se añaden los elementos
        officer_data: Datos del oficial técnico
        styles: Diccionario con los estilos del reporte
    """
    # Datos detallados
    records = officer_data.get('records', [])
    if records:
        # Subtítulo para la sección de registros detallados
        detail_title = Paragraph("Registros Detallados", styles['section'])
        elements.append(detail_title)
        elements.append(Spacer(1, 0.1 * inch))

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

        # Crear tabla de registros detallados
        detail_table = create_detail_table(table_data, records)
        elements.append(detail_table)