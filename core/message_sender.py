# core/message_sender.py
from core.personalized_sender import WhatsAppSender
import threading
import time

class MessageSender:
    def __init__(self):
        self.whatsapp_sender = WhatsAppSender()
        self.is_sending = False
        
    def personalize_message(self, template, contact_data):
        """Personalize message template with contact data"""
        message = template
        for key, value in contact_data.items():
            placeholder = f"({key})"
            message = message.replace(placeholder, str(value))
        return message
        
    def initialize_whatsapp(self):
        """Initialize WhatsApp Web connection"""
        print("Initializing WhatsApp Web...")
        success = self.whatsapp_sender.initialize_driver()
        if success:
            print("WhatsApp Web initialized successfully")
        else:
            print("Failed to initialize WhatsApp Web")
        return success
        
    def send_message(self, phone, message):
        """Send message to phone number using Selenium"""
        return self.whatsapp_sender.send_single_message(phone, message)
        
    def send_bulk_messages(self, contacts_data, progress_callback=None, status_callback=None):
        """Send messages to multiple contacts"""
        if not self.whatsapp_sender.is_initialized:
            if status_callback:
                status_callback("🟡 Connecting to WhatsApp Web...")
            if not self.initialize_whatsapp():
                if status_callback:
                    status_callback("❌ Failed to initialize WhatsApp Web")
                return 0, len(contacts_data)
        
        # Prepare data for bulk sending
        contacts_with_messages = []
        for contact in contacts_data:
            phone = contact.get('phone', '')
            name = contact.get('name', '')
            personalized_message = self.personalize_message(self.current_template, contact)
            contacts_with_messages.append((phone, personalized_message, name))
        
        if status_callback:
            status_callback(f"🟡 Sending to {len(contacts_with_messages)} contacts...")
        
        # Send messages
        success_count, total_count = self.whatsapp_sender.send_bulk_messages(
            contacts_with_messages, 
            progress_callback
        )
        
        if status_callback:
            status_callback(f"✅ Sent {success_count}/{total_count} messages successfully")
        
        return success_count, total_count
        
    def set_message_template(self, template):
        """Set the current message template"""
        self.current_template = template
        
    def close_whatsapp(self):
        """Close WhatsApp connection"""
        self.whatsapp_sender.close_driver()
        
    def is_whatsapp_ready(self):
        """Check if WhatsApp is initialized and ready"""
        return self.whatsapp_sender.is_initialized and self.whatsapp_sender.check_whatsapp_ready()