# personalized_sender.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse, time, random, os
import subprocess
import sys

class WhatsAppSender:
    def __init__(self):
        self.driver = None
        self.is_initialized = False
        
    def initialize_driver(self):
        """Initialize the Chrome driver for WhatsApp Web"""
        try:
            # Setup Chrome
            user_data_dir = os.path.join(os.getcwd(), "User_Data")
            if not os.path.exists(user_data_dir):
                os.makedirs(user_data_dir)

            options = webdriver.ChromeOptions()
            options.add_argument(f"--user-data-dir={user_data_dir}")
            options.add_argument("--profile-directory=Default")
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # Try to initialize driver with better error handling
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                print(f"ChromeDriver initialization failed: {e}")
                # Fallback: try without ChromeDriverManager
                try:
                    self.driver = webdriver.Chrome(options=options)
                except Exception as e2:
                    print(f"Fallback Chrome initialization also failed: {e2}")
                    return False

            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.get("https://web.whatsapp.com/")
            
            print("🔒 Please scan the QR code in the browser window...")
            
            # Wait for QR code to be scanned with multiple conditions
            try:
                # Wait for either the side panel (logged in) or QR code element
                WebDriverWait(self.driver, 120).until(
                    lambda driver: driver.find_elements(By.XPATH, "//div[@id='pane-side']") or 
                                 driver.find_elements(By.XPATH, "//canvas[@aria-label='Scan me!']") or
                                 driver.find_elements(By.XPATH, "//div[contains(@class, 'landing-wrapper')]")
                )
                
                # Check if we're actually logged in by looking for the side panel
                if self.driver.find_elements(By.XPATH, "//div[@id='pane-side']"):
                    self.is_initialized = True
                    print("✅ WhatsApp Web is ready!")
                    return True
                else:
                    print("⏳ QR code detected, waiting for scan...")
                    # Wait additional time for login to complete
                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@id='pane-side']"))
                    )
                    self.is_initialized = True
                    print("✅ WhatsApp Web is ready!")
                    return True
                    
            except Exception as e:
                print(f"❌ Failed to detect WhatsApp login: {e}")
                return False
            
        except Exception as e:
            print(f"❌ Failed to initialize driver: {e}")
            return False

    def check_whatsapp_ready(self):
        """Check if WhatsApp Web is ready to send messages"""
        if not self.driver:
            return False
            
        try:
            # Check if we're on WhatsApp and logged in
            current_url = self.driver.current_url
            if "web.whatsapp.com" not in current_url:
                self.driver.get("https://web.whatsapp.com/")
                time.sleep(3)
                
            # Check for login status
            side_panel = self.driver.find_elements(By.XPATH, "//div[@id='pane-side']")
            return len(side_panel) > 0
        except:
            return False

    def send_single_message(self, phone, message):
        """Send a single message to a phone number"""
        if not self.driver:
            print("❌ Driver not initialized.")
            return False

        try:
            # Ensure WhatsApp is ready
            if not self.check_whatsapp_ready():
                print("❌ WhatsApp is not ready. Please ensure you're logged in.")
                return False

            # Clean phone number (remove spaces, dashes, etc.)
            clean_phone = ''.join(filter(str.isdigit, str(phone)))
            if not clean_phone:
                print(f"❌ Invalid phone number: {phone}")
                return False

            encoded = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded}"
            self.driver.get(url)

            # Wait for potential overlay
            time.sleep(3)
            try:
                close_btns = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//button")
                for btn in close_btns:
                    try:
                        btn.click()
                        print(f"ℹ️ Closed a popup before sending to {phone}")
                    except:
                        pass
            except:
                pass

            # Wait until message input box appears
            msg_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//footer//div[@contenteditable='true' and @data-tab]")
                )
            )

            # Focus and send message
            self.driver.execute_script("arguments[0].focus();", msg_box)
            time.sleep(0.5)
            msg_box.send_keys(Keys.ENTER)

            # Wait until message is visible in chat
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'message-out')]"))
            )

            print(f"✅ Message sent to {phone}")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error sending to {phone}: {e}")

    def send_bulk_messages(self, contacts_with_messages, progress_callback=None):
        """Send messages to multiple contacts with progress tracking"""
        if not self.is_initialized:
            if not self.initialize_driver():
                return 0, len(contacts_with_messages)

        success_count = 0
        total_count = len(contacts_with_messages)

        for index, (phone, message, name) in enumerate(contacts_with_messages):
            if progress_callback:
                progress_callback(index, total_count, f"Sending to {name}...")

            if self.send_single_message(phone, message):
                success_count += 1

            if progress_callback:
                progress_callback(index + 1, total_count, f"Sent to {name}")

        return success_count, total_count

    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.is_initialized = False
            self.driver = None
            print("✅ Driver closed")

