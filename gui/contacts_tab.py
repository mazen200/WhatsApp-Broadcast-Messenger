# gui/contacts_tab.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QHeaderView, QMessageBox,
                            QInputDialog, QLineEdit, QFileDialog, QCheckBox)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHeaderView

class ContactsTab(QWidget):
    contacts_updated = pyqtSignal()
    
    def __init__(self, contact_manager):
        super().__init__()
        self.contact_manager = contact_manager
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("➕ Add Contact")
        self.add_btn.clicked.connect(self.add_contact)
        
        self.import_btn = QPushButton("📁 Import CSV")
        self.import_btn.clicked.connect(self.import_csv)
        
        self.export_btn = QPushButton("💾 Export CSV")
        self.export_btn.clicked.connect(self.export_csv)
        
        self.delete_btn = QPushButton("🗑️ Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected)
        
        self.add_column_btn = QPushButton("➕ Add Column")
        self.add_column_btn.clicked.connect(self.add_column)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.add_column_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Contacts table
        self.contacts_table = QTableWidget()
        self.contacts_table.setAlternatingRowColors(True)
        self.contacts_table.horizontalHeader().setStretchLastSection(True)
        
        # Connect cell changed signal to handle edits
        self.contacts_table.cellChanged.connect(self.on_cell_changed)
        
        layout.addWidget(self.contacts_table)
        
        self.refresh_table()
        
    def refresh_table(self):
        # Disconnect cellChanged signal temporarily to avoid triggering during refresh
        self.contacts_table.cellChanged.disconnect()
        
        contacts = self.contact_manager.get_contacts()
        columns = self.contact_manager.get_columns()
        
        self.contacts_table.setRowCount(len(contacts))
        self.contacts_table.setColumnCount(len(columns))
        self.contacts_table.setHorizontalHeaderLabels(columns)
        
        for row, contact in enumerate(contacts):
            for col, column_name in enumerate(columns):
                value = contact.get(column_name, "")
                item = QTableWidgetItem(str(value))
                self.contacts_table.setItem(row, col, item)
        
        self.contacts_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Reconnect cellChanged signal
        self.contacts_table.cellChanged.connect(self.on_cell_changed)
        
        self.contacts_updated.emit()
        
    def on_cell_changed(self, row, column):
        """Handle when a cell is edited in the table"""
        if row < self.contacts_table.rowCount() and column < self.contacts_table.columnCount():
            item = self.contacts_table.item(row, column)
            if item:
                column_name = self.contact_manager.get_columns()[column]
                new_value = item.text()
                
                # Update the contact manager with the new value
                self.contact_manager.update_contact(row, column_name, new_value)
        
    def add_contact(self):
        phone, ok = QInputDialog.getText(self, "Add Contact", "Phone Number:")
        if ok and phone:
            name, ok = QInputDialog.getText(self, "Add Contact", "Name:")
            if ok:
                self.contact_manager.add_contact(phone.strip(), name.strip())
                self.refresh_table()
                
    def delete_selected(self):
        selected_rows = set(index.row() for index in self.contacts_table.selectedIndexes())
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select contacts to delete.")
            return
            
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Delete {len(selected_rows)} contact(s)?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Delete in reverse order to maintain correct indices
            for row in sorted(selected_rows, reverse=True):
                self.contact_manager.delete_contact(row)
            self.refresh_table()
            
    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.contact_manager.load_from_csv(file_path)
                self.refresh_table()
                QMessageBox.information(self, "Success", "Contacts imported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import contacts: {str(e)}")
                
    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "contacts.csv", "CSV Files (*.csv)")
        if file_path:
            try:
                # Ensure all table edits are saved before exporting
                self.save_table_edits()
                self.contact_manager.save_to_csv(file_path)
                QMessageBox.information(self, "Success", "Contacts exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export contacts: {str(e)}")
                
    def add_column(self):
        column_name, ok = QInputDialog.getText(self, "Add Column", "Column Name:")
        if ok and column_name:
            self.contact_manager.add_column(column_name.strip())
            self.refresh_table()
            
    def save_table_edits(self):
        """Ensure all pending edits in the table are saved to the contact manager"""
        for row in range(self.contacts_table.rowCount()):
            for col in range(self.contacts_table.columnCount()):
                item = self.contacts_table.item(row, col)
                if item:
                    column_name = self.contact_manager.get_columns()[col]
                    value = item.text()
                    self.contact_manager.update_contact(row, column_name, value)