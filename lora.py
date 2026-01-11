import serial

PORT = "/dev/ttyUSB0"
BAUD = 9600

class LoRaReader:
    """Handles LoRa serial communication and message parsing."""
    
    def __init__(self, port=PORT, baudrate=BAUD):
        """Initialize serial connection."""
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,         # 8
            parity=serial.PARITY_NONE,         # N
            stopbits=serial.STOPBITS_ONE,      # 1
            xonxoff=False,                     # software flow control off
            rtscts=False,                      # hardware flow control off
            dsrdtr=False,                      # DSR/DTR flow control off
            timeout=1,                         # non-blocking-ish read
            inter_byte_timeout=0.2,
        )
        
        # Some devices need these lines asserted; Minicom often does this by default.
        self.ser.setDTR(True)
        self.ser.setRTS(True)
        
        # Clear any stale bytes so you start clean
        self.ser.reset_input_buffer()
        
        self.buffer = bytearray()
        print(f"Listening on {port} @ {baudrate} (8N1)…")
    
    def read_chunk(self):
        """Read available data from serial port."""
        return self.ser.read(1024)
    
    def parse_messages(self, chunk):
        """Parse chunk into complete messages. Yields decoded text messages."""
        if not chunk:
            return
        
        self.buffer.extend(chunk)
        
        # Split on either LF or CR (Minicom copes with both)
        while True:
            # find first CR or LF
            ix = -1
            for sep in (b"\n", b"\r"):
                j = self.buffer.find(sep)
                if j != -1 and (ix == -1 or j < ix):
                    ix = j
            if ix == -1:
                break
            
            raw = self.buffer[:ix]
            # drop the separator (and any paired CR/LF)
            drop = 1
            if ix + 1 < len(self.buffer) and self.buffer[ix:ix+2] in (b"\r\n", b"\n\r"):
                drop = 2
            del self.buffer[:ix+drop]
            
            # decode safely
            text = raw.decode("utf-8", errors="replace")
            yield text
    
    def close(self):
        """Close the serial connection."""
        self.ser.close()
        print("Serial port closed.")
