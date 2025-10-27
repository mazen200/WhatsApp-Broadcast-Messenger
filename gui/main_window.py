from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QPushButton, QTableWidget, QTableWidgetItem,
                            QTextEdit, QLineEdit, QLabel, QHeaderView, QMessageBox,
                            QCheckBox, QFileDialog, QSplitter, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import pandas as pd
from core.contact_manager import ContactManager
from core.message_sender import MessageSender
from gui.contacts_tab import ContactsTab
from gui.message_tab import MessageTab
from gui.send_tab import SendTab

class WhatsAppBroadcastApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.contact_manager = ContactManager()
        self.message_sender = MessageSender()
        self.init_ui()
        self.load_initial_data()
        
    def init_ui(self):
        self.setWindowTitle("WhatsApp Broadcast Messenger")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.contacts_tab = ContactsTab(self.contact_manager)
        self.message_tab = MessageTab()
        self.send_tab = SendTab(self.contact_manager, self.message_sender)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.contacts_tab, "📞 Contacts")
        self.tab_widget.addTab(self.message_tab, "💬 Message")
        self.tab_widget.addTab(self.send_tab, "🚀 Send")
        
        # Connect signals
        self.connect_signals()
        
    def connect_signals(self):
        # When contacts are updated in contacts tab, update send tab
        self.contacts_tab.contacts_updated.connect(self.send_tab.refresh_contacts)
        # When message is updated in message tab, update send tab
        self.message_tab.message_updated.connect(self.send_tab.update_message_template)
        
    def load_initial_data(self):
        # Try to load existing data
        try:
            self.contact_manager.load_from_csv('contacts.csv')
            self.contacts_tab.refresh_table()
        except FileNotFoundError:
            pass  # No existing contacts file
            
        try:
            with open('message.txt', 'r', encoding='utf-8') as f:
                message = f.read()
                self.message_tab.set_message(message)
        except FileNotFoundError:
            pass  # No existing message file