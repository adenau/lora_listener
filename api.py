from flask import Flask, jsonify, render_template
import threading

class API:
    """Flask API server for accessing LoRa message data."""
    
    def __init__(self, database):
        """Initialize API with a reference to the database."""
        self.database = database
        self.app = Flask(__name__)
        self.thread = None
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up Flask routes."""
        @self.app.route('/', methods=['GET'])
        def index():
            """Serve the main HTML dashboard."""
            return render_template('index.html')
        
        @self.app.route('/api', methods=['GET'])
        def api_index():
            """API index - lists all available endpoints."""
            return jsonify({
                'name': 'LoRa Listener API',
                'version': '1.0',
                'endpoints': [
                    {
                        'path': '/',
                        'method': 'GET',
                        'description': 'Web dashboard for monitoring messages'
                    },
                    {
                        'path': '/api',
                        'method': 'GET',
                        'description': 'API index and available endpoints'
                    },
                    {
                        'path': '/api/messages',
                        'method': 'GET',
                        'description': 'Get the last 100 messages',
                        'example': '/api/messages'
                    },
                    {
                        'path': '/api/messages/<limit>',
                        'method': 'GET',
                        'description': 'Get the last N messages',
                        'example': '/api/messages/50'
                    },
                    {
                        'path': '/api/health',
                        'method': 'GET',
                        'description': 'Health check endpoint'
                    }
                ]
            })
        
        @self.app.route('/api/messages', methods=['GET'])
        @self.app.route('/api/messages/<int:limit>', methods=['GET'])
        def get_messages(limit=100):
            """Get the last N messages from the database."""
            messages = self.database.get_last_messages(limit)
            return jsonify({
                'count': len(messages),
                'messages': messages
            })
        
        @self.app.route('/api/health', methods=['GET'])
        def health():
            """Health check endpoint."""
            return jsonify({'status': 'ok'})
    
    def start(self, host='0.0.0.0', port=5000):
        """Start the Flask server in a background thread."""
        self.thread = threading.Thread(
            target=self._run_server, 
            args=(host, port), 
            daemon=True
        )
        self.thread.start()
        print(f"Flask API server started on http://{host}:{port}")
        return self.thread
    
    def _run_server(self, host, port):
        """Run the Flask server."""
        self.app.run(host=host, port=port, debug=False, use_reloader=False)
    
    def stop(self):
        """Stop the API server (daemon thread will terminate with main program)."""
        print("API server shutting down...")
