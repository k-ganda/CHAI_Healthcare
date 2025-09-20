#!/usr/bin/env python3
import json
import time
import threading
from datetime import datetime
import asyncio
import websockets

class LoRaReceiver:
    def __init__(self):
        self.devices = {}
        self.running = True
        self.connected_clients = set()
        
    async def handle_client(self, websocket, path):
        print(f"Dashboard connected: {websocket.remote_address}")
        self.connected_clients.add(websocket)
        try:
            while True:
                if self.devices:
                    for device_id, device_data in self.devices.items():
                        await websocket.send(json.dumps(device_data))
                await asyncio.sleep(1)
        except websockets.exceptions.ConnectionClosed:
            print("Dashboard disconnected")
            self.connected_clients.discard(websocket)
    
    async def start_websocket_server(self):
        server = await websockets.serve(self.handle_client, "localhost", 8765)
        print("WebSocket server started on ws://localhost:8765")
        await server.wait_closed()
    
    def simulate_lora_reception(self):
        print("Starting LoRa receiver simulation...")
        while self.running:
            current_time = int(time.time() * 1000)
            if int(time.time()) % 30 < 10:
                device_data = {
                    "deviceId": 1,
                    "timestamp": current_time,
                    "temperature": 4.2,
                    "batteryVoltage": 3.8,
                    "emergencyPressed": False,
                    "alertActive": False,
                    "alertType": 0
                }
            elif int(time.time()) % 30 < 20:
                device_data = {
                    "deviceId": 1,
                    "timestamp": current_time,
                    "temperature": 9.1,
                    "batteryVoltage": 3.7,
                    "emergencyPressed": False,
                    "alertActive": True,
                    "alertType": 1
                }
            else:
                device_data = {
                    "deviceId": 1,
                    "timestamp": current_time,
                    "temperature": 1.5,
                    "batteryVoltage": 3.6,
                    "emergencyPressed": False,
                    "alertActive": True,
                    "alertType": 2
                }
            
            self.devices[1] = device_data
            timestamp = datetime.fromtimestamp(device_data["timestamp"] / 1000).strftime("%H:%M:%S")
            print(f"[{timestamp}] Device 1: {device_data['temperature']:.1f}°C, "
                  f"Battery: {device_data['batteryVoltage']:.1f}V, "
                  f"Alert: {'Yes' if device_data['alertActive'] else 'No'}")
            time.sleep(5)
    
    def start(self):
        print("=== Solar-Surv LoRa Receiver ===")
        print("WebSocket server: ws://localhost:8765")
        print()
        
        def run_websocket():
            asyncio.run(self.start_websocket_server())
        
        ws_thread = threading.Thread(target=run_webs