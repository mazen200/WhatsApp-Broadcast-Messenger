# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import WhatsAppBroadcastApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhatsAppBroadcastApp()
    window.show()
    sys.exit(app.exec())