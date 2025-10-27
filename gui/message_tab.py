from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                            QPushButton, QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal

class MessageTab(QWidget):
    message_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel("Use (name) as placeholder for contact name. Example: Hello (name)!")
        layout.addWidget(instructions)
        
        # Message editor
        self.message_edit = QTextEdit()
        self.message_edit.setPlaceholderText("Enter your message here...\nUse (name) as placeholder for contact name.")
        self.message_edit.textChanged.connect(self.on_message_changed)
        layout.addWidget(self.message_edit)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("📁 Load from File")
        self.load_btn.clicked.connect(self.load_from_file)
        
        self.save_btn = QPushButton("💾 Save to File")
        self.save_btn.clicked.connect(self.save_to_file)
        
        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.clicked.connect(self.clear_message)
        
        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
    def on_message_changed(self):
        self.message_updated.emit(self.message_edit.toPlainText())
        
    def set_message(self, message):
        self.message_edit.setPlainText(message)
        
    def get_message(self):
        return self.message_edit.toPlainText()
        
    def load_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Message", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    message = f.read()
                    self.set_message(message)
                QMessageBox.information(self, "Success", "Message loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load message: {str(e)}")
                
    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Message", "message.txt", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.get_message())
                QMessageBox.information(self, "Success", "Message saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save message: {str(e)}")
                
    def clear_message(self):
        self.message_edit.clear()