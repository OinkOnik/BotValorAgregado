# pdf_styles.py
# Módulo que define los estilos de texto y párrafos para ser utilizados en los reportes PDF

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


def get_report_styles():
    """
    Crea y devuelve un diccionario con estilos personalizados para el reporte PDF

    Returns:
        dict: Diccionario con estilos para distintos elementos del PDF
    """
    # Obtener los estilos base
    styles = getSampleStyleSheet()

    # Diccionario para almacenar todos los estilos
    report_styles = {}

    # Estilo de título principal con color técnico
    report_styles['title'] = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#2C3E50'),  # Azul oscuro profesional
        alignment=TA_CENTER,
        spaceAfter=12
    )

    # Estilo de subtítulo
    report_styles['subtitle'] = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor('#34495E'),  # Gris azulado
        alignment=TA_LEFT,
        spaceAfter=6
    )

    # Estilo para secciones
    report_styles['section'] = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#2980B9'),  # Azul claro
        alignment=TA_LEFT,
        spaceAfter=6
    )

    # Estilo para información general
    report_styles['info'] = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#2C3E50'),
        alignment=TA_LEFT
    )

    # Estilo para notas
    report_styles['note'] = ParagraphStyle(
        'NoteStyle',
        parent=styles['Italic'],
        fontSize=9,
        textColor=colors.HexColor('#7F8C8D'),  # Gris más suave
        alignment=TA_LEFT
    )

    # Estilo para el título de notas
    report_styles['notes_title'] = ParagraphStyle(
        'NotesTitle',
        parent=styles['Heading4'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.HexColor('#2C3E50')
    )

    # Estilo para el índice de contenidos
    report_styles['toc'] = ParagraphStyle(
        'TOCStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#34495E')
    )

    # Estilos para los niveles del índice
    report_styles['toc1'] = ParagraphStyle(
        name='TOC1',
        parent=report_styles['toc'],
        fontSize=14,
        fontName='Helvetica-Bold',
        leftIndent=0
    )

    report_styles['toc2'] = ParagraphStyle(
        name='TOC2',
        parent=report_styles['toc'],
        fontSize=12,
        leftIndent=10
    )

    report_styles['toc3'] = ParagraphStyle(
        name='TOC3',
        parent=report_styles['toc'],
        fontSize=10,
        leftIndent=20
    )

    return report_styles