# core/contact_manager.py
import pandas as pd
import csv

class ContactManager:
    def __init__(self):
        self.contacts = []
        self.columns = ['phone', 'name']  # Default columns
        
    def load_from_csv(self, file_path):
        """Load contacts from CSV file"""
        try:
            df = pd.read_csv(file_path)
            self.contacts = df.to_dict('records')
            self.columns = list(df.columns)
        except Exception as e:
            # Fallback to manual CSV reading
            self.contacts = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.columns = reader.fieldnames or ['phone', 'name']
                for row in reader:
                    # Ensure all columns are present and handle NaN values
                    cleaned_row = {}
                    for col in self.columns:
                        value = row.get(col, '')
                        # Convert pandas NaN or None to empty string
                        if pd.isna(value) or value is None:
                            value = ''
                        cleaned_row[col] = str(value).strip()
                    self.contacts.append(cleaned_row)
                    
    def save_to_csv(self, file_path):
        """Save contacts to CSV file"""
        if self.contacts:
            df = pd.DataFrame(self.contacts)
            # Replace empty strings with NaN to avoid writing empty values
            df = df.replace('', pd.NA)
            df.to_csv(file_path, index=False, encoding='utf-8')
            
    def get_contacts(self):
        """Get all contacts"""
        return self.contacts
        
    def get_columns(self):
        """Get column names"""
        return self.columns
        
    def add_contact(self, phone, name):
        """Add a new contact"""
        contact = {'phone': phone, 'name': name}
        # Add empty values for other columns
        for col in self.columns:
            if col not in contact:
                contact[col] = ""
        self.contacts.append(contact)
        
    def delete_contact(self, index):
        """Delete contact by index"""
        if 0 <= index < len(self.contacts):
            del self.contacts[index]
            
    def add_column(self, column_name):
        """Add a new column to contacts"""
        if column_name not in self.columns:
            self.columns.append(column_name)
            # Add empty values for the new column to all contacts
            for contact in self.contacts:
                contact[column_name] = ""
                
    def update_contact(self, index, column_name, value):
        """Update a specific contact field"""
        if 0 <= index < len(self.contacts) and column_name in self.columns:
            self.contacts[index][column_name] = value
            
    def update_contact_row(self, index, contact_data):
        """Update entire contact row"""
        if 0 <= index < len(self.contacts):
            for col in self.columns:
                if col in contact_data:
                    self.contacts[index][col] = contact_data[col]
                elif col not in self.contacts[index]:
                    self.contacts[index][col] = ""