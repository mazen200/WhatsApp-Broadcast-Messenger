# WhatsApp Broadcast Messenger

A powerful desktop application built with Python and PyQt6 for sending personalized WhatsApp messages to multiple contacts efficiently. This tool is perfect for businesses, organizations, or individuals who need to send bulk personalized messages while maintaining the personal touch of individual communication.

## 🌟 Features

- **Contact Management**: Import, export, and manage contacts via CSV files
- **Personalized Messaging**: Use placeholders like `(name)` to customize messages for each recipient
- **Bulk Messaging**: Send messages to multiple contacts with progress tracking
- **WhatsApp Web Integration**: Automated message sending through WhatsApp Web
- **User-Friendly GUI**: Intuitive tab-based interface built with PyQt6
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- WhatsApp Web account

### Installation

1. **Clone or download the project files**
   ```bash
   # Create project structure
   mkdir whatsapp-broadcast
   cd whatsapp-broadcast
   ```

2. **Create the required directory structure:**
   ```
   whatsapp-broadcast/
   ├── main.py
   ├── core/
   │   ├── contact_manager.py
   │   ├── message_sender.py
   │   └── personalized_sender.py
   ├── gui/
   │   ├── main_window.py
   │   ├── contacts_tab.py
   │   ├── message_tab.py
   │   └── send_tab.py
   └── requirements.txt
   ```

3. **Install dependencies:**
   ```bash
   pip install PyQt6 pandas selenium webdriver-manager
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## 📖 User Guide

### Step 1: Manage Contacts (📞 Contacts Tab)

**Import Contacts:**
- Click "📁 Import CSV" to load contacts from a CSV file
- Your CSV should have at least `phone` and `name` columns
- Additional columns can be added and used as placeholders in messages

**Add Contacts Manually:**
- Click "➕ Add Contact" to add individual contacts
- Use "➕ Add Column" to create custom fields for personalization

**Export Contacts:**
- Click "💾 Export CSV" to save your contact list

### Step 2: Compose Message (💬 Message Tab)

**Create Your Message:**
- Type your message in the text editor
- Use placeholders in parentheses: `(name)`, `(phone)`, or any custom column name
- Example: `Hello (name)! Your order (order_id) is ready for pickup.`

**Message Management:**
- "📁 Load from File" - Import message from text file
- "💾 Save to File" - Save message template for future use
- "🗑️ Clear" - Start with a fresh message

### Step 3: Send Messages (🚀 Send Tab)

**Connect WhatsApp:**
1. Click "Connect WhatsApp"
2. A Chrome browser window will open
3. Scan the QR code with your WhatsApp mobile app
4. Wait for the "🟢 WhatsApp Connected" status

**Select Recipients:**
- Check the boxes next to contacts you want to message
- Use "✓ Select All" or "✗ Deselect All" for bulk selection
- Preview your personalized message in the preview area

**Send Messages:**
- Click "🚀 Send to Selected"
- Confirm the send operation
- Monitor progress in the status bar and status label

## 🛠️ Technical Design

### Architecture Overview

The application follows a **Model-View-Controller (MVC)** pattern with clear separation between data management, business logic, and user interface.

### Core Components

#### 1. **Data Layer** (`contact_manager.py`)
- **Responsibility**: Contact data persistence and management
- **Key Features**:
  - CSV import/export with pandas fallback
  - Dynamic column management
  - Data validation and cleaning
- **Design Pattern**: Repository Pattern

#### 2. **Business Logic Layer** (`message_sender.py`, `personalized_sender.py`)
- **Responsibility**: Message personalization and WhatsApp automation
- **Key Features**:
  - Template-based message personalization
  - Selenium-based WhatsApp Web automation
  - Bulk sending with progress tracking
- **Design Pattern**: Facade Pattern (simplifies complex Selenium operations)

#### 3. **Presentation Layer** (GUI modules)
- **Responsibility**: User interface and interaction
- **Components**:
  - `main_window.py`: Application shell and tab management
  - `contacts_tab.py`: Contact management interface
  - `message_tab.py`: Message composition interface
  - `send_tab.py`: Message sending and progress monitoring

### Key Technical Decisions

#### 1. **PyQt6 for GUI**
- **Why**: Cross-platform compatibility, native look and feel, powerful widget set
- **Benefits**: Signal-slot architecture for decoupled components, excellent documentation

#### 2. **Selenium for WhatsApp Automation**
- **Why**: Most reliable method for WhatsApp Web interaction
- **Benefits**: Handles dynamic content loading, robust element location, cross-browser compatibility

#### 3. **Pandas for Data Handling**
- **Why**: Efficient CSV processing with automatic type inference
- **Benefits**: Handles large contact lists efficiently, built-in data cleaning capabilities

#### 4. **Threading for Responsive UI**
- **Implementation**: Background threads for WhatsApp connection and message sending
- **Benefit**: Prevents UI freezing during long operations

## 🔧 Advanced Usage

### Custom Placeholders

You can create custom placeholders by adding columns to your contacts:

1. In Contacts tab, click "➕ Add Column"
2. Name your column (e.g., "company")
3. Fill in the data for each contact
4. Use `(company)` in your message template

### CSV Format

Your CSV files should follow this structure:
```csv
phone,name,company,order_id
+1234567890,John Doe,ABC Corp,ORD-001
+1234567891,Jane Smith,XYZ Inc,ORD-002
```

### Message Template Examples

**Basic Personalization:**
```
Hello (name), this is a test message.
```

**Advanced Personalization:**
```
Dear (name),

Your order (order_id) from (company) has been shipped.
Tracking number: (tracking_number)

Thank you for your business!
Best regards,
Your Team
```

## ⚠️ Important Notes

### Rate Limiting
- WhatsApp may impose rate limits on message sending
- The application includes random delays to mimic human behavior
- Avoid sending too many messages too quickly

### Privacy & Compliance
- Ensure you have recipients' consent for messaging
- Follow WhatsApp's Terms of Service
- This tool is intended for legitimate business communication

### Browser Requirements
- Google Chrome must be installed
- The application creates a separate Chrome profile in the "User_Data" directory
- First-time setup requires QR code scanning

## 🐛 Troubleshooting

### Common Issues

1. **QR Code Not Scanning**
   - Ensure WhatsApp Web is not already logged in on another device
   - Check internet connection
   - Try refreshing the browser window

2. **Messages Not Sending**
   - Verify phone numbers include country codes
   - Check that contacts exist on WhatsApp
   - Ensure WhatsApp Web is properly connected

3. **Import Errors**
   - Verify CSV format includes 'phone' and 'name' columns
   - Check for special characters in the file
   - Ensure file is not open in another program

### Logs and Debugging
- Check the console output for detailed error messages
- The application creates browser logs in the "User_Data" directory

## 🔮 Future Enhancements

Potential improvements for future versions:
- Image and file attachment support
- Scheduled message sending
- Message templates library
- Advanced contact filtering
- Delivery reports
- Multi-language support


![WhatsApp Image 2025-10-27 at 22 32 28_6204ce81](https://github.com/user-attachments/assets/9207c595-8c4a-4336-8c07-f0fab381ed9b)

![WhatsApp Image 2025-10-27 at 22 33 20_202134eb](https://github.com/user-attachments/assets/315cad0d-6611-4cea-a215-e8682ff3d8e5)

![WhatsApp Image 2025-10-27 at 22 34 04_8573b13f](https://github.com/user-attachments/assets/07225645-6978-4ac0-93a0-47ce240a9860)

