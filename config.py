"""
Configuration file for LoRa Listener application.
Modify these settings according to your setup.
"""

# Serial Port Configuration
SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_BAUDRATE = 9600

# Database Configuration
DATABASE_FILE = "messages.db"

# API Server Configuration
API_HOST = "0.0.0.0"  # Use 0.0.0.0 to accept connections from any network interface
API_PORT = 5000

# Auto-refresh interval for web dashboard (seconds)
DASHBOARD_REFRESH_INTERVAL = 30
