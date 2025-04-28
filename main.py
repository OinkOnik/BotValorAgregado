# main.py
# Punto de entrada principal de la aplicación
# Inicializa la aplicación y muestra la ventana principal

import sys
import os
from PyQt5.QtWidgets import QApplication
from time_analysis_window import TimeAnalysisWindow


# Aseguramos que las dependencias necesarias estén disponibles
def check_dependencies():
    try:
        import reportlab
    except ImportError:
        print("Instalando dependencia reportlab para generación de PDFs...")
        os.system('pip install reportlab')

    try:
        import pandas
    except ImportError:
        print("Instalando dependencia pandas para análisis de datos...")
        os.system('pip install pandas')

    try:
        import matplotlib
    except ImportError:
        print("Instalando dependencia matplotlib para gráficos...")
        os.system('pip install matplotlib')

    try:
        import numpy
    except ImportError:
        print("Instalando dependencia numpy para cálculos numéricos...")
        os.system('pip install numpy')


def main():
    check_dependencies()
    app = QApplication(sys.argv)
    window = TimeAnalysisWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()