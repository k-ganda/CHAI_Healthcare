#!/usr/bin/env python3
"""
Solar-Surv: LoRa Receiver for Vaccine Cold Chain Monitoring
"""

import json
import time
import threading
from datetime import datetime

class LoRaReceiver:
    def __init__(self):
        self.devices = {}
        self.alerts = []
        self.running = True
        
    def simulate_lora_reception(self):
        """Simulate LoRa message reception for demo purposes"""
        print("Starting LoRa receiver simulation...")
        
        while self.running:
            current_time = int(time.time() * 1000)
            
            # Scenario 1: Normal temperature
            if int(time.time()) % 30 < 10:
                device_data = {
                    'deviceId': 1,
                    'timestamp': current_time,
                    'temperature': 4.2,
                    'batteryVoltage': 3.8,
                    'emergencyPressed': False,
                    'alertActive': False,
                    'alertType': 0
                }
                self.process_message(device_data)
            
            # Scenario 2: Temperature too hot
            elif int(time.time()) % 30 < 20:
                device_data = {
                    'deviceId': 1,
                    'timestamp': current_time,
                    'temperature': 9.1,
                    'batteryVoltage': 3.7,
                    'emergencyPressed': False,
                    'alertActive': True,
                    'alertType': 1
                }
                self.process_message(device_data)
            
            # Scenario 3: Temperature too cold
            else:
                device_data = {
                    'deviceId': 1,
                    'timestamp': current_time,
                    'temperature': 1.5,
                    'batteryVoltage': 3.6,
                    'emergencyPressed': False,
                    'alertActive': True,
                    'alertType': 2
                }
                self.process_message(device_data)
            
            time.sleep(5)
    
    def process_message(self, data):
        """Process received LoRa message"""
        device_id = data['deviceId']
        self.devices[device_id] = data
        
        timestamp = datetime.fromtimestamp(data['timestamp'] / 1000).strftime('%H:%M:%S')
        print(f"[{timestamp}] Device {device_id}: {data['temperature']:.1f}°C, "
              f"Battery: {data['batteryVoltage']:.1f}V, "
              f"Alert: {'Yes' if data['alertActive'] else 'No'}")
        
        if data['alertActive']:
            self.handle_alert(data)
    
    def handle_alert(self, data):
        """Handle temperature alerts"""
        alert_messages = {
            1: f"🚨 VACCINE ALERT: Temperature too hot! {data['temperature']:.1f}°C",
            2: f"🚨 VACCINE ALERT: Temperature too cold! {data['temperature']:.1f}°C",
            3: "🚨 EMERGENCY: Manual alert triggered!",
            4: f"⚠️ Battery low: {data['batteryVoltage']:.1f}V"
        }
        
        alert_message = alert_messages.get(data['alertType'], "Unknown alert")
        print(f"ALERT: {alert_message}")
    
    def start(self):
        """Start the LoRa receiver"""
        print("=== Solar-Surv LoRa Receiver ===")
        print("Vaccine Cold Chain Monitoring System")
        print("Listening for temperature alerts...")
        print()
        
        try:
            self.simulate_lora_reception()
        except KeyboardInterrupt:
            print("\nShutting down receiver...")
            self.running = False

def main():
    receiver = LoRaReceiver()
    receiver.start()

if __name__ == "__main__":
    main()
