# gui/send_tab.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QHeaderView, QCheckBox,
                            QLabel, QProgressBar, QMessageBox, QTextEdit, QSplitter)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtCore import Qt
import threading

class SendTab(QWidget):
    def __init__(self, contact_manager, message_sender):
        super().__init__()
        self.contact_manager = contact_manager
        self.message_sender = message_sender
        self.message_template = ""
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # WhatsApp status
        self.status_layout = QHBoxLayout()
        self.whatsapp_status = QLabel("🔴 WhatsApp Not Connected")
        self.connect_btn = QPushButton("Connect WhatsApp")
        self.connect_btn.clicked.connect(self.connect_whatsapp)
        
        self.status_layout.addWidget(self.whatsapp_status)
        self.status_layout.addStretch()
        self.status_layout.addWidget(self.connect_btn)
        layout.addLayout(self.status_layout)
        
        # Message preview
        self.preview_label = QLabel("Message Preview:")
        layout.addWidget(self.preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(100)
        layout.addWidget(self.preview_text)
        
        # Contacts selection table
        self.contacts_table = QTableWidget()
        self.contacts_table.setAlternatingRowColors(True)
        layout.addWidget(self.contacts_table)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready to send messages")
        layout.addWidget(self.status_label)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.select_all_btn = QPushButton("✓ Select All")
        self.select_all_btn.clicked.connect(self.select_all)
        
        self.deselect_all_btn = QPushButton("✗ Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        
        self.send_btn = QPushButton("🚀 Send to Selected")
        self.send_btn.clicked.connect(self.send_messages)
        
        button_layout.addWidget(self.select_all_btn)
        button_layout.addWidget(self.deselect_all_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.send_btn)
        
        layout.addLayout(button_layout)
        
        self.refresh_contacts()
        
    def connect_whatsapp(self):
        """Connect to WhatsApp Web"""
        self.status_label.setText("🟡 Connecting to WhatsApp Web...")
        self.connect_btn.setEnabled(False)
        
        # Run in thread to avoid freezing GUI
        thread = threading.Thread(target=self.connect_whatsapp_thread)
        thread.daemon = True
        thread.start()
        
    def connect_whatsapp_thread(self):
        """Thread for connecting to WhatsApp"""
        try:
            success = self.message_sender.initialize_whatsapp()
            if success:
                self.whatsapp_status.setText("🟢 WhatsApp Connected")
                self.status_label.setText("✅ WhatsApp is ready! You can now send messages.")
            else:
                self.whatsapp_status.setText("🔴 WhatsApp Connection Failed")
                self.status_label.setText("❌ Failed to connect to WhatsApp. Please try again.")
        except Exception as e:
            self.whatsapp_status.setText("🔴 WhatsApp Connection Error")
            self.status_label.setText(f"❌ Error: {str(e)}")
        finally:
            self.connect_btn.setEnabled(True)
        
    def refresh_contacts(self):
        contacts = self.contact_manager.get_contacts()
        columns = ["Select"] + self.contact_manager.get_columns()
        
        self.contacts_table.setRowCount(len(contacts))
        self.contacts_table.setColumnCount(len(columns))
        self.contacts_table.setHorizontalHeaderLabels(columns)
        
        for row, contact in enumerate(contacts):
            # Checkbox for selection
            checkbox = QCheckBox()
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.contacts_table.setCellWidget(row, 0, checkbox_widget)
            
            # Contact data
            for col, column_name in enumerate(self.contact_manager.get_columns(), 1):
                value = contact.get(column_name, "")
                item = QTableWidgetItem(str(value))
                self.contacts_table.setItem(row, col, item)
        
        self.contacts_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
    def update_message_template(self, message):
        self.message_template = message
        self.message_sender.set_message_template(message)
        # Show preview with sample name
        preview = message.replace("(name)", "Ahmed")
        self.preview_text.setPlainText(preview)
        
    def get_selected_contacts(self):
        selected_contacts = []
        for row in range(self.contacts_table.rowCount()):
            checkbox_widget = self.contacts_table.cellWidget(row, 0)
            checkbox = checkbox_widget.findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                contact_data = {}
                for col, column_name in enumerate(self.contact_manager.get_columns(), 1):
                    item = self.contacts_table.item(row, col)
                    if item:
                        contact_data[column_name] = item.text()
                selected_contacts.append(contact_data)
        return selected_contacts
        
    def select_all(self):
        for row in range(self.contacts_table.rowCount()):
            checkbox_widget = self.contacts_table.cellWidget(row, 0)
            checkbox = checkbox_widget.findChild(QCheckBox)
            if checkbox:
                checkbox.setChecked(True)
                
    def deselect_all(self):
        for row in range(self.contacts_table.rowCount()):
            checkbox_widget = self.contacts_table.cellWidget(row, 0)
            checkbox = checkbox_widget.findChild(QCheckBox)
            if checkbox:
                checkbox.setChecked(False)
                
    def send_messages(self):
        if not self.message_sender.is_whatsapp_ready():
            QMessageBox.warning(self, "WhatsApp Not Connected", 
                              "Please connect to WhatsApp first using the 'Connect WhatsApp' button.")
            return
            
        selected_contacts = self.get_selected_contacts()
        if not selected_contacts:
            QMessageBox.warning(self, "Warning", "Please select at least one contact.")
            return
            
        if not self.message_template:
            QMessageBox.warning(self, "Warning", "Please set a message template first.")
            return
            
        reply = QMessageBox.question(self, "Confirm Send", 
                                   f"Send message to {len(selected_contacts)} contact(s)?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Run sending in a separate thread to avoid freezing the GUI
            thread = threading.Thread(target=self.send_messages_thread, args=(selected_contacts,))
            thread.daemon = True
            thread.start()
            
    def send_messages_thread(self, contacts):
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(contacts))
        self.send_btn.setEnabled(False)
        
        def progress_callback(current, total, status):
            self.progress_bar.setValue(current)
            self.status_label.setText(status)
        
        try:
            success_count, total_count = self.message_sender.send_bulk_messages(
                contacts, 
                progress_callback=progress_callback,
                status_callback=lambda msg: self.status_label.setText(msg)
            )
            
            self.status_label.setText(f"✅ Successfully sent {success_count}/{total_count} messages!")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
            
        finally:
            self.progress_bar.setVisible(False)
            self.send_btn.setEnabled(True)