#!/usr/bin/env python3
"""
Solar-Surv: SMS-Based Sensor Node
Simulates Arduino + GSM module sending temperature alerts via SMS
"""

import time
import random
from datetime import datetime
import json

class SMSSensorNode:
    def __init__(self, device_id=1, phone_number="+1234567890"):
        self.device_id = device_id
        self.phone_number = phone_number
        self.temp_min = 2.0
        self.temp_max = 8.0
        self.battery_voltage = 3.8
        self.alert_sent = False
        self.sms_count = 0
        self.sms_cost = 0.02  # $0.02 per SMS
        
    def read_temperature(self):
        """Simulate temperature reading (like potentiometer)"""
        # Simulate different scenarios
        current_time = int(time.time()) % 60
        
        if current_time < 20:
            # Normal temperature
            return round(random.uniform(3.5, 6.5), 1)
        elif current_time < 40:
            # Too hot
            return round(random.uniform(8.5, 12.0), 1)
        else:
            # Too cold
            return round(random.uniform(-2.0, 1.5), 1)
    
    def check_battery(self):
        """Simulate battery voltage reading"""
        # Battery slowly drains over time
        self.battery_voltage = max(3.0, 4.2 - (time.time() / 3600) * 0.1)
        return round(self.battery_voltage, 1)
    
    def send_sms(self, message):
        """Simulate sending SMS via GSM module"""
        self.sms_count += 1
        cost = self.sms_count * self.sms_cost
        
        print(f"\n📱 SMS SENT to {self.phone_number}:")
        print(f"   {message}")
        print(f"   SMS Count: {self.sms_count} | Total Cost: ${cost:.2f}")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 50)
        
        # In real implementation, this would use GSM module:
        # gsm.send_sms(phone_number, message)
    
    def check_thresholds(self, temperature):
        """Check temperature against vaccine storage thresholds"""
        alerts = []
        
        # Check temperature thresholds
        if temperature > self.temp_max:
            alerts.append({
                'type': 'temperature_hot',
                'message': f"🚨 VACCINE ALERT: Temperature {temperature}°C is TOO HOT! Safe range: 2-8°C"
            })
        elif temperature < self.temp_min:
            alerts.append({
                'type': 'temperature_cold', 
                'message': f"�� VACCINE ALERT: Temperature {temperature}°C is TOO COLD! Safe range: 2-8°C"
            })
        
        # Check battery level
        if self.battery_voltage < 3.3:
            alerts.append({
                'type': 'battery_low',
                'message': f"⚠️ BATTERY LOW: {self.battery_voltage}V - Device may shut down soon"
            })
        
        return alerts
    
    def simulate_emergency_button(self):
        """Simulate emergency button press"""
        message = "🚨 EMERGENCY ALERT: Manual emergency button pressed! Immediate attention required!"
        self.send_sms(message)
        self.alert_sent = True
    
    def run_sensor_loop(self):
        """Main sensor loop - simulates Arduino operation"""
        print("=== Solar-Surv SMS Sensor Node ===")
        print(f"Device ID: {self.device_id}")
        print(f"Phone Number: {self.phone_number}")
        print(f"Temperature Range: {self.temp_min}-{self.temp_max}°C")
        print(f"Battery: {self.battery_voltage}V")
        print("Starting temperature monitoring...")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        try:
            while True:
                # Read sensors
                temperature = self.read_temperature()
                battery = self.check_battery()
                
                # Check thresholds
                alerts = self.check_thresholds(temperature)
                
                # Send alerts via SMS
                for alert in alerts:
                    if not self.alert_sent or alert['type'] != 'temperature_hot':
                        self.send_sms(alert['message'])
                        self.alert_sent = True
                
                # Reset alert flag for new temperature readings
                if not alerts:
                    self.alert_sent = False
                
                # Display status
                status = "SAFE" if not alerts else "ALERT"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"Temp: {temperature}°C | Battery: {battery}V | Status: {status}")
                
                # Simulate emergency button (random chance)
                if random.random() < 0.05:  # 5% chance every cycle
                    print("\n🔴 EMERGENCY BUTTON PRESSED!")
                    self.simulate_emergency_button()
                
                time.sleep(5)  # Read every 5 seconds
                
        except KeyboardInterrupt:
            print(f"\n\nSensor node stopped.")
            print(f"Total SMS sent: {self.sms_count}")
            print(f"Total cost: ${self.sms_count * self.sms_cost:.2f}")

def main():
    # Configuration
    DEVICE_ID = 1
    PHONE_NUMBER = "+1234567890"  # Change to your phone number
    
    print("🌡️ Solar-Surv SMS-Based Vaccine Monitor")
    print("Simulating Arduino + GSM module for offline alerts")
    print()
    
    # Create sensor node
    sensor = SMSSensorNode(DEVICE_ID, PHONE_NUMBER)
    
    # Start monitoring
    sensor.run_sensor_loop()

if __name__ == "__main__":
    main()