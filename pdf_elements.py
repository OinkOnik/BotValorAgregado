# pdf_elements.py
# Módulo que contiene elementos personalizados para los reportes PDF como
# encabezados de capítulo, elementos de tablas y otros componentes especiales

from reportlab.platypus import Flowable, Table, TableStyle
from reportlab.lib import colors


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


def create_divisor_line():
    """
    Crea un elemento de tabla que sirve como línea divisoria

    Returns:
        Table: Un objeto tabla con líneas horizontales para separar contenido
    """
    divisor_style = TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#CCCCCC')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#CCCCCC')),
    ])
    divisor = Table([['']],
                    colWidths=[450],
                    style=divisor_style)
    return divisor


def create_statistics_table(statistics_data, width_col1=2.5, width_col2=3):
    """
    Crea una tabla de estadísticas con estilo técnico

    Args:
        statistics_data: Lista de filas con datos estadísticos
        width_col1: Ancho de la primera columna en pulgadas
        width_col2: Ancho de la segunda columna en pulgadas

    Returns:
        Table: Un objeto tabla con estadísticas formateado con estilo técnico
    """
    stats_table = Table(statistics_data, colWidths=[width_col1 * 72, width_col2 * 72])  # Convertir a puntos
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
    return stats_table


def create_detail_table(table_data, records, col_widths=None):
    """
    Crea una tabla detallada con datos de registros

    Args:
        table_data: Lista de filas con datos de la tabla
        records: Lista de registros originales para determinar estilos
        col_widths: Lista de anchos de columnas (opcional)

    Returns:
        Table: Un objeto tabla con datos detallados y formato técnico
    """
    if col_widths is None:
        col_widths = [2 * 72, 2 * 72, 2 * 72]  # Convertir a puntos

    detail_table = Table(table_data, colWidths=col_widths)

    # Estilo base de la tabla
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

    # Aplicar colores alternados y resaltar anomalías
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
    return detail_table