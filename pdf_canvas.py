# pdf_canvas.py
# Módulo que contiene clases personalizadas para Canvas de reportlab, específicamente
# para manejar pies de página, numeración y otras características avanzadas del canvas

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
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


class NumberedCanvas(Canvas):
    """
    Canvas con numeración de páginas para usar con SimpleDocTemplate.build()
    """
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