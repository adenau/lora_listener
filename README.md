# LoRa Listener

A Python-based listener application for receiving and logging messages from a **SX1262 LoRa HAT** via serial communication. The application stores messages in an SQLite database and provides a REST API for querying received messages.

## Features

- **Serial Communication**: Listens to LoRa messages from SX1262 LoRa HAT via serial port
- **SQLite Database**: Automatically logs all received messages with timestamps
- **REST API**: Flask-based API server for querying message history
- **Modular Design**: Clean separation of concerns with dedicated modules for LoRa, Database, and API functionality

## Hardware Requirements

- SX1262 LoRa HAT
- Compatible device with serial port (default: `/dev/ttyUSB0`)

## Software Requirements

- Python 3.7 or higher
- Virtual environment (recommended)

## Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd /path/to/lora_listener
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

All application settings are centralized in `config.py`. Edit this file to customize your setup:

```python
# Serial Port Configuration
SERIAL_PORT = "/dev/ttyUSB0"      # Your LoRa device serial port
SERIAL_BAUDRATE = 9600             # Communication baud rate

# Database Configuration
DATABASE_FILE = "messages.db"      # SQLite database file path

# API Server Configuration
API_HOST = "0.0.0.0"              # Server host (0.0.0.0 = all interfaces)
API_PORT = 5000                    # Server port

# Dashboard Configuration
DASHBOARD_REFRESH_INTERVAL = 30    # Auto-refresh interval (seconds)
```

### Common Configuration Changes

**Change serial port:**
```python
SERIAL_PORT = "/dev/ttyUSB1"  # or "/dev/ttyAMA0" for Raspberry Pi GPIO
```

**Change API port:**
```python
API_PORT = 8080
```

**Use different database location:**
```python
DATABASE_FILE = "/var/lib/lora/messages.db"
```

## Running the Application

1. **Ensure your virtual environment is activated**:
   ```bash
   source .venv/bin/activate
   ```

2. **Configure your settings** (if needed):
   ```bash
   # Edit config.py to match your setup
   nano config.py
   ```

3. **Run the main application**:
   ```bash
   python main.py
   ```

The application will:
- Initialize the SQLite database
- Start the Flask API server (default: http://0.0.0.0:5000)
- Start the web dashboard at http://localhost:5000
- Begin listening for LoRa messages on the configured serial port

4. **Stop the application**:
   - Press `Ctrl+C` to gracefully shut down

## Web Dashboard

Access the live message monitoring dashboard by visiting `http://localhost:5000` in your web browser.

Features:
- Real-time message display
- Auto-refresh every 30 seconds (configurable in `config.py`)
- Message count and timestamp statistics
- Direct link to API documentation

## API Endpoints

Once running, the following endpoints are available:

### Web Dashboard
```bash
GET http://localhost:5000/
```
Interactive web interface for monitoring messages.

### API Documentation
```bash
GET http://localhost:5000/api
```
Lists all available API endpoints.

### Get Last 100 Messages
```bash
GET http://localhost:5000/api/messages
```

### Get Last N Messages
```bash
GET http://localhost:5000/api/messages/{limit}
```
Example: `http://localhost:5000/api/messages/50` retrieves the last 50 messages.

### Health Check
```bash
GET http://localhost:5000/api/health
```

### Example API Response
```json
{
  "count": 2,
  "messages": [
    {
      "id": 2,
      "timestamp": "2026-01-10T14:30:45.123456",
      "message": "Hello from LoRa"
    },
    {
      "id": 1,
      "timestamp": "2026-01-10T14:30:12.654321",
      "message": "Test message"
    }
  ]
}
```

## Project Structure

```
lora_listener/
├── main.py          # Main application entry point
├── config.py        # Centralized configuration file
├── lora.py          # LoRa serial communication module
├── database.py      # SQLite database operations
├── api.py           # Flask REST API server
├── templates/       # HTML templates
│   └── index.html   # Web dashboard
├── requirements.txt # Python dependencies
├── messages.db      # SQLite database (created automatically)
└── README.md        # This file
```

## Troubleshooting

### Serial Port Permission Issues
If you encounter permission errors accessing `/dev/ttyUSB0`:
```bash
sudo usermod -a -G dialout $USER
```
Log out and log back in for changes to take effect.

### Change Serial Port
If your device uses a different serial port, modify the `PORT` variable in `lora.py`.

### View Database Contents
To manually inspect the database:
```bash
sqlite3 messages.db "SELECT * FROM messages ORDER BY id DESC LIMIT 10;"
```

## License

This project is provided as-is for use with SX1262 LoRa HAT devices.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
