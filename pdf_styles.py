# pdf_styles.py
"""
Módulo que define todos los estilos y la apariencia visual para los reportes PDF generados.

Este módulo centraliza la definición de estilos para textos, párrafos, encabezados y otros
elementos visuales utilizados en los reportes PDF. Mantener los estilos en un módulo
separado facilita la consistencia visual y permite modificar la apariencia de los reportes
sin cambiar la lógica de generación de contenido.
"""

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch


def get_report_styles():
    """
    Crea y retorna un diccionario con todos los estilos necesarios para el reporte

    Returns:
        dict: Diccionario con los estilos para el documento
    """
    # Obtener estilos base
    styles = getSampleStyleSheet()

    # Estilo para el título principal
    # Verificamos si 'title' ya existe para evitar duplicados
    if 'report_title' not in styles:
        styles.add(ParagraphStyle(
            name='report_title',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
        ))

    # Estilos para encabezados (para utilizar con Paragraph en vez de ChapterHeader)
    if 'heading1' not in styles:
        styles.add(ParagraphStyle(
            name='heading1',
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=18,
            spaceAfter=10,
            textColor=colors.darkblue,
        ))

    if 'heading2' not in styles:
        styles.add(ParagraphStyle(
            name='heading2',
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=16,
            leftIndent=10,
            spaceAfter=8,
            textColor=colors.darkblue,
        ))

    if 'heading3' not in styles:
        styles.add(ParagraphStyle(
            name='heading3',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=14,
            leftIndent=20,
            spaceAfter=6,
            textColor=colors.darkblue,
        ))

    # Estilo para texto informativo
    if 'info' not in styles:
        styles.add(ParagraphStyle(
            name='info',
            fontName='Helvetica',
            fontSize=11,
            leading=13,
            alignment=TA_LEFT
        ))

    # Estilo para el título de notas
    if 'notes_title' not in styles:
        styles.add(ParagraphStyle(
            name='notes_title',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=13,
            alignment=TA_LEFT
        ))

    # Estilo para notas
    if 'note' not in styles:
        styles.add(ParagraphStyle(
            name='note',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            leftIndent=10
        ))

    # Estilo para secciones
    if 'section' not in styles:
        styles.add(ParagraphStyle(
            name='section',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=14,
            textColor=colors.darkblue,
            leftIndent=15
        ))

    # Estilos para tabla de contenidos
    if 'toc1' not in styles:
        styles.add(ParagraphStyle(
            name='toc1',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            leftIndent=20,
            firstLineIndent=-20
        ))

    if 'toc2' not in styles:
        styles.add(ParagraphStyle(
            name='toc2',
            fontName='Helvetica',
            fontSize=11,
            leading=14,
            leftIndent=40,
            firstLineIndent=-20
        ))

    if 'toc3' not in styles:
        styles.add(ParagraphStyle(
            name='toc3',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            leftIndent=60,
            firstLineIndent=-20
        ))

    return styles