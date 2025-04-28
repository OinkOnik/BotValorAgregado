#main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui_time_analysis import TimeAnalysisWindow

def main():
    app = QApplication(sys.argv)
    window = TimeAnalysisWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()