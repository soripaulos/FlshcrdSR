#!/usr/bin/env python3
"""
Simple HTTP server for serving Flutter web app
Handles SPA routing by serving index.html for all routes
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import urlparse

class FlutterWebHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="build/web", **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Remove leading slash
        if path.startswith('/'):
            path = path[1:]
        
        # If path is empty, serve index.html
        if not path:
            path = 'index.html'
        
        # Check if file exists
        full_path = os.path.join(self.directory, path)
        
        if os.path.isfile(full_path):
            # File exists, serve it normally
            super().do_GET()
        else:
            # File doesn't exist, serve index.html for SPA routing
            self.path = '/index.html'
            super().do_GET()

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 8080))
    
    # Change to the directory containing build/web
    if not os.path.exists('build/web'):
        print("Error: build/web directory not found. Please run 'flutter build web' first.")
        sys.exit(1)
    
    with socketserver.TCPServer(("", PORT), FlutterWebHandler) as httpd:
        print(f"Serving Flutter web app at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.shutdown()