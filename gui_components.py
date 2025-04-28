# gui_components.py
# Componentes reutilizables para la interfaz gráfica
# Contiene funciones para crear tablas y limpiar layouts

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def clear_layout(layout):
    """Limpia un layout eliminando todos sus widgets"""
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clear_layout(item.layout())

def create_table_from_dataframe(df):
    """Crea una tabla a partir de un DataFrame"""
    # Crear la tabla
    table = QTableWidget()

    # Configurar el número de filas y columnas
    table.setRowCount(len(df))
    table.setColumnCount(len(df.columns))

    # Configurar los encabezados
    table.setHorizontalHeaderLabels(df.columns)

    # Llenar la tabla con datos
    for i in range(len(df)):
        for j in range(len(df.columns)):
            value = df.iloc[i, j]

            # Formatear valores numéricos
            if isinstance(value, (int, float)):
                if j > 0:  # Las columnas después de la primera son numéricas
                    item = QTableWidgetItem(f"{value:.2f}")
                else:
                    item = QTableWidgetItem(str(value))
            else:
                item = QTableWidgetItem(str(value))

            # Alineación al centro
            item.setTextAlignment(Qt.AlignCenter)

            table.setItem(i, j, item)

    # Ajustar el tamaño de las columnas al contenido
    table.resizeColumnsToContents()

    return table

def create_figure(figsize=(10, 6)):
    """Crea una figura de matplotlib con canvas"""
    fig = Figure(figsize=figsize)
    canvas = FigureCanvas(fig)
    return fig, canvas