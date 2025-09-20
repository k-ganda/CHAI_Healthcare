#!/usr/bin/env python3
"""
Solar-Surv: Web Dashboard Server
Serves the SMS monitoring dashboard with real-time updates
"""

import http.server
import socketserver
import webbrowser
import threading
import time
from datetime import datetime

class DashboardServer:
    def __init__(self, port=8080):
        self.port = port
        self.running = False
        
    def start_server(self):
        """Start the web server"""
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"🌐 Dashboard server started on http://localhost:{self.port}")
            print(f"�� Open http://localhost:{self.port}/sms_dashboard.html in your browser")
            print("Press Ctrl+C to stop")
            self.running = True
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Server stopped")
                self.running = False

def main():
    print("��️ Solar-Surv SMS Dashboard Server")
    print("=" * 50)
    
    # Create and start server
    server = DashboardServer(8080)
    
    # Open browser automatically
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:8080/sms_dashboard.html')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start server
    server.start_server()

if __name__ == "__main__":
    main()