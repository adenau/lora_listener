import sys
from datetime import datetime
from config import DATABASE_FILE, API_HOST, API_PORT
from database import Database
from lora import LoRaReader
from api import API

def write_line(f, s: str):
    f.write(s + "\n")
    f.flush()

# Initialize the database
db = Database(DATABASE_FILE)

# Start the Flask API server with database reference
api = API(db)
api.start(API_HOST, API_PORT)

# Initialize LoRa reader
lora = LoRaReader()

try:
    while True:
        chunk = lora.read_chunk()
        
        for text in lora.parse_messages(chunk):
            timestamp = datetime.now().isoformat()
            write_line(sys.stdout, text)
            db.log_message(text, timestamp)

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    lora.close()
    api.stop()

