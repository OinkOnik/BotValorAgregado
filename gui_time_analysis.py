# gui_time_analysis.py
# Punto de entrada principal para la aplicación de análisis de tiempos
# Inicializa la ventana principal de análisis de tiempos de servicio

import sys
from PyQt5.QtWidgets import QApplication
from time_analysis_window import TimeAnalysisWindow

def main():
    app = QApplication(sys.argv)
    window = TimeAnalysisWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()