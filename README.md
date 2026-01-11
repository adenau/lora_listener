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

By default, the application uses the following settings:

- **Serial Port**: `/dev/ttyUSB0`
- **Baud Rate**: `9600`
- **Database File**: `messages.db`
- **API Server**: `http://0.0.0.0:5000`

To change these settings, edit the respective files:
- LoRa settings: `lora.py`
- Database file: `database.py`
- API settings: `api.py`

## Running the Application

1. **Ensure your virtual environment is activated**:
   ```bash
   source .venv/bin/activate
   ```

2. **Run the main application**:
   ```bash
   python main.py
   ```

The application will:
- Initialize the SQLite database
- Start the Flask API server on port 5000
- Begin listening for LoRa messages on the configured serial port

3. **Stop the application**:
   - Press `Ctrl+C` to gracefully shut down

## API Endpoints

Once running, the following endpoints are available:

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
├── lora.py          # LoRa serial communication module
├── database.py      # SQLite database operations
├── api.py           # Flask REST API server
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
