# pdf_elements.py
# Módulo que contiene elementos específicos para la generación de PDF como encabezados, tablas y líneas divisorias

from reportlab.platypus import Paragraph, Table, TableStyle, Flowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch


class ChapterHeader(Flowable):
    """
    Clase personalizada para crear encabezados de capítulos con niveles
    """

    def __init__(self, text, level=1):
        Flowable.__init__(self)
        self.text = text
        self.level = level
        self.paragraph = None  # Inicializamos el párrafo como None
        # Definimos los estilos según el nivel
        self.styles = {
            1: ParagraphStyle(
                name='Heading1',
                fontName='Helvetica-Bold',
                fontSize=16,
                leading=18,
                spaceAfter=10
            ),
            2: ParagraphStyle(
                name='Heading2',
                fontName='Helvetica-Bold',
                fontSize=14,
                leading=16,
                spaceAfter=8,
                leftIndent=10
            ),
            3: ParagraphStyle(
                name='Heading3',
                fontName='Helvetica-Bold',
                fontSize=12,
                leading=14,
                spaceAfter=6,
                leftIndent=20
            )
        }

    def wrap(self, availWidth, availHeight):
        """
        Determina las dimensiones requeridas para el flowable

        Args:
            availWidth: Ancho disponible
            availHeight: Alto disponible

        Returns:
            Tupla (ancho, alto) requerido
        """
        # Creamos el párrafo aquí para asegurarnos de que esté inicializado
        self.paragraph = Paragraph(self.text, self.styles[self.level])
        self.width, self.height = self.paragraph.wrap(availWidth, availHeight)
        return (self.width, self.height)

    def draw(self):
        """
        Dibuja el flowable en el canvas
        """
        # Comprobamos que el párrafo esté inicializado
        if self.paragraph is None:
            self.paragraph = Paragraph(self.text, self.styles[self.level])
            # Aseguramos que el párrafo ha sido dimensionado correctamente
            self.paragraph.wrap(self.width, self.height)

        # Dibujamos el párrafo
        self.paragraph.drawOn(self.canv, 0, 0)

        # Generar un ID único para este encabezado
        key = f'h{self.level}-{hash(self.text)}'

        # Crear el bookmark para la tabla de contenidos
        # Esto solo marca la posición actual en el documento
        self.canv.bookmarkPage(key)

        # Añadir una entrada al esquema del documento
        # Utilizamos 0 como nivel base y sumamos el nivel real
        # para evitar saltos no permitidos
        self.canv.addOutlineEntry(self.text, key, 0 + self.level)


def create_divisor_line():
    """
    Crea una línea divisoria para separar secciones

    Returns:
        Table: Un elemento de tabla con una línea divisoria
    """
    line_table = Table([['']], colWidths=[7.5 * inch], rowHeights=[1])
    line_table.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (0, 0), 1, colors.grey),
        ('BOTTOMPADDING', (0, 0), (0, 0), 0),
        ('TOPPADDING', (0, 0), (0, 0), 0),
    ]))
    return line_table


def create_statistics_table(data):
    """
    Crea una tabla de estadísticas con diseño técnico

    Args:
        data: Lista de listas con datos para la tabla

    Returns:
        Table: Tabla formatada con los datos
    """
    # Crear tabla con ancho específico
    table = Table(data, colWidths=[2.5 * inch, 4.0 * inch])

    # Estilo técnico para la tabla
    table.setStyle(TableStyle([
        # Encabezados
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        # Contenido
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (0, -1), colors.grey),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        # Bordes
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    return table


def create_detail_table(data, records):
    """
    Crea una tabla de registros detallados con formato técnico

    Args:
        data: Lista de listas con datos para la tabla
        records: Datos originales de registros para personalización

    Returns:
        Table: Tabla formatada con los datos
    """
    # Crear tabla con ancho específico
    table = Table(data, colWidths=[2.3 * inch, 2.3 * inch, 2.3 * inch])

    # Estilo base para la tabla
    style = [
        # Encabezados
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        # Contenido
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        # Bordes
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]

    # Personalización para registros con anomalías
    for i, record in enumerate(records, 1):
        if 'anomalía' in str(record.get('Tiempo de estadía', '')):
            style.append(('TEXTCOLOR', (2, i), (2, i), colors.red))
            style.append(('FONTNAME', (2, i), (2, i), 'Helvetica-Bold'))

    table.setStyle(TableStyle(style))
    return table


def create_operational_data_table(data):
    """
    Crea una tabla para mostrar los datos de análisis de respuesta operativa

    Args:
        data: Lista de listas con datos para la tabla

    Returns:
        Table: Tabla formateada con los datos operativos
    """
    # Determinar ancho de columnas basado en la cantidad de datos
    if len(data) > 0 and len(data[0]) == 2:  # Para tabla de afiliados (2 columnas)
        col_widths = [3.5 * inch, 3.5 * inch]
    else:  # Para otros casos (por ejemplo, formato original)
        col_widths = [2.5 * inch, 4.0 * inch]

    # Crear tabla con ancho específico para datos operativos
    table = Table(data, colWidths=col_widths)

    # Estilo técnico para la tabla de datos operativos
    table.setStyle(TableStyle([
        # Encabezados
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Diferente color para distinguir
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        # Contenido
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (0, -1), colors.grey),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        # Bordes
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    return table