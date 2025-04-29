# pdf_generator.py
# Módulo para generar reportes PDF con diseño técnico y profesional mejorado, con índice,
# numeración de páginas, títulos de sección y diseño estructurado

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image,
    PageBreak, KeepTogether, ListFlowable, ListItem, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.tableofcontents import TableOfContents
import os
from datetime import datetime


class FooterCanvas(Canvas):
    """
    Canvas personalizado para añadir pie de página con numeración
    """

    def __init__(self, *args, **kwargs):
        # Extraer el argumento personalizado antes de pasar al constructor padre
        self.footer_info = kwargs.pop('footer_info',
                                      "Reporte generado por Visor Técnico Bot") if 'footer_info' in kwargs else "Reporte generado por Visor Técnico Bot"
        Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        """
        Sobrescribe el método showPage para guardar cada página antes de mostrarla
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """
        Añade el pie de página a cada página antes de guardar el documento
        """
        page_count = len(self.pages)

        # Restaurar el estado de cada página y añadir el footer
        for page_num, page in enumerate(self.pages):
            self.__dict__.update(page)
            self.draw_footer(page_num + 1, page_count)
            Canvas.showPage(self)

        Canvas.save(self)

    def draw_footer(self, page_number, total_pages):
        """
        Dibuja el pie de página con el número de página y el texto de información
        """
        # Configuración del pie de página
        self.saveState()
        self.setFont('Helvetica', 8)

        # Línea horizontal superior del footer
        self.setStrokeColor(colors.HexColor('#CCCCCC'))
        self.line(36, 40, letter[0] - 36, 40)

        # Información de la aplicación (izquierda)
        self.setFillColor(colors.HexColor('#666666'))
        self.drawString(36, 25, self.footer_info)

        # Fecha de generación (centro)
        fecha_generacion = datetime.now().strftime("%d/%m/%Y")
        fecha_texto = f"Fecha: {fecha_generacion}"
        fecha_width = self.stringWidth(fecha_texto, 'Helvetica', 8)
        self.drawString((letter[0] - fecha_width) / 2, 25, fecha_texto)

        # Numeración de página (derecha)
        page_text = f"Página {page_number} de {total_pages}"
        self.drawRightString(letter[0] - 36, 25, page_text)

        self.restoreState()


class ChapterHeader(Flowable):
    """
    Flowable personalizado para crear encabezados de capítulo con diseño técnico
    """

    def __init__(self, text, level=1):
        Flowable.__init__(self)
        self.text = text
        self.level = level  # 1 para título principal, 2 para subtítulo, etc.

    def draw(self):
        # Configuración según el nivel
        if self.level == 1:
            # Título principal
            self.canv.setFillColor(colors.HexColor('#2C3E50'))
            self.canv.setFont('Helvetica-Bold', 16)
            self.canv.drawString(0, 0, self.text)
            # Línea debajo del título principal
            self.canv.setStrokeColor(colors.HexColor('#3498DB'))
            self.canv.setLineWidth(2)
            self.canv.line(0, -6, 450, -6)
        else:
            # Subtítulo
            self.canv.setFillColor(colors.HexColor('#34495E'))
            self.canv.setFont('Helvetica-Bold', 14)
            self.canv.drawString(0, 0, self.text)

    def wrap(self, availWidth, availHeight):
        # Determinar altura basada en el nivel
        if self.level == 1:
            return (availWidth, 30)  # Título principal con espacio para línea
        else:
            return (availWidth, 20)  # Subtítulo


# Define una clase de numeración de páginas que se usará con el método doc.build()
class NumberedCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            Canvas.showPage(self)
        Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#666666'))

        # Dibujar línea divisoria
        self.setStrokeColor(colors.HexColor('#CCCCCC'))
        self.line(36, 40, letter[0] - 36, 40)

        # Información del pie de página
        self.drawString(36, 25, "Reporte generado por Visor Técnico Bot")

        # Fecha de generación (centro)
        fecha_generacion = datetime.now().strftime("%d/%m/%Y")
        fecha_texto = f"Fecha: {fecha_generacion}"
        fecha_width = self.stringWidth(fecha_texto, 'Helvetica', 8)
        self.drawString((letter[0] - fecha_width) / 2, 25, fecha_texto)

        # Número de página (derecha)
        self.drawRightString(letter[0] - 36, 25, f"Página {self._pageNumber} de {page_count}")


def generate_pdf_report(data, output_path):
    """
    Genera un reporte en PDF con diseño técnico mejorado y profesional

    Args:
        data: Diccionario con datos procesados organizados por oficial técnico
        output_path: Ruta donde se guardará el archivo PDF
    """
    # Crear el documento PDF con canvas personalizado para añadir pie de página
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

    # Estilos personalizados
    styles = getSampleStyleSheet()

    # Estilo de título principal con color técnico
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#2C3E50'),  # Azul oscuro profesional
        alignment=TA_CENTER,
        spaceAfter=12
    )

    # Estilo de subtítulo
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor('#34495E'),  # Gris azulado
        alignment=TA_LEFT,
        spaceAfter=6
    )

    # Estilo para secciones
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#2980B9'),  # Azul claro
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

    # Estilo para el índice de contenidos
    toc_style = ParagraphStyle(
        'TOCStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#34495E')
    )

    # Tabla de contenidos
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(name='TOC1', parent=toc_style, fontSize=14, fontName='Helvetica-Bold', leftIndent=0),
        ParagraphStyle(name='TOC2', parent=toc_style, fontSize=12, leftIndent=10),
        ParagraphStyle(name='TOC3', parent=toc_style, fontSize=10, leftIndent=20)
    ]

    # Añadir título del reporte
    report_title = Paragraph("Reporte de Tiempos de Estadía", title_style)
    elements.append(report_title)
    elements.append(Spacer(1, 0.25 * inch))

    # Añadir fecha y hora de generación
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    date_text = Paragraph(f"Generado el: {now}", info_style)
    elements.append(date_text)
    elements.append(Spacer(1, 0.25 * inch))

    # Añadir índice de contenidos
    toc_header = ChapterHeader("Índice de Contenidos", 1)
    elements.append(toc_header)
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(toc)
    elements.append(PageBreak())

    # Añadir sección de resumen y notas
    summary_header = ChapterHeader("Resumen y Notas Técnicas", 1)
    elements.append(summary_header)
    elements.append(Spacer(1, 0.2 * inch))

    # Texto de resumen
    summary_text = Paragraph(
        "Este reporte presenta un análisis detallado de los tiempos de estadía registrados para cada oficial técnico, "
        "incluyendo métricas como tiempo total, tiempo promedio y anomalías detectadas en los registros.",
        info_style
    )
    elements.append(summary_text)
    elements.append(Spacer(1, 0.15 * inch))

    # Notas técnicas
    notes_title = Paragraph("Notas técnicas:", ParagraphStyle(
        'NotesTitle',
        parent=styles['Heading4'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.HexColor('#2C3E50')
    ))
    elements.append(notes_title)

    # Lista de notas técnicas
    notes = [
        "Las anomalías (tiempos negativos) se muestran en rojo para identificación rápida.",
        "Los registros con anomalías no se incluyen en los cálculos estadísticos.",
        "El tiempo promedio se calcula utilizando únicamente registros válidos (tiempos positivos)."
    ]

    notes_items = []
    for note in notes:
        notes_items.append(ListItem(Paragraph(note, note_style)))

    notes_list = ListFlowable(
        notes_items,
        bulletType='bullet',
        leftIndent=20,
        bulletFontName='Helvetica',
        bulletFontSize=8
    )
    elements.append(notes_list)
    elements.append(Spacer(1, 0.3 * inch))

    # Agregar una línea divisoria antes de los datos
    divisor_style = TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#CCCCCC')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#CCCCCC')),
    ])
    divisor = Table([['']],
                    colWidths=[450],
                    style=divisor_style)
    elements.append(divisor)
    elements.append(Spacer(1, 0.3 * inch))

    # Añadir sección principal de datos
    data_header = ChapterHeader("Datos de Tiempos por Oficial Técnico", 1)
    elements.append(data_header)
    elements.append(Spacer(1, 0.3 * inch))

    # Para cada oficial técnico, generar una sección con sus datos
    for officer, officer_data in data.items():
        # Título de la sección (nombre del oficial)
        officer_header = ChapterHeader(f"Oficial Técnico: {officer}", 2)
        elements.append(officer_header)
        elements.append(Spacer(1, 0.2 * inch))

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
        stats_title = Paragraph("Resumen de Estadísticas", section_style)
        elements.append(stats_title)
        elements.append(Spacer(1, 0.1 * inch))

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
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),  # Gris para bordes
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 0.2 * inch))

        # Datos detallados
        records = officer_data.get('records', [])
        if records:
            # Subtítulo para la sección de registros detallados
            detail_title = Paragraph("Registros Detallados", section_style)
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
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#95A5A6')),  # Gris para bordes
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
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

        # Añadir un salto de página después de cada oficial (excepto el último)
        if list(data.keys()).index(officer) < len(data) - 1:
            elements.append(PageBreak())

    # Generar el PDF con numeración de páginas utilizando el NumberedCanvas
    doc.build(elements, canvasmaker=NumberedCanvas)

    return output_path