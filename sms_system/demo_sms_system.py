#!/usr/bin/env python3
"""
Solar-Surv: SMS System Demo
Demonstrates offline vaccine monitoring with SMS alerts
"""

import time
import threading
from datetime import datetime

class SMSDemo:
    def __init__(self):
        self.sensor_running = False
        self.receiver_running = False
        
    def simulate_sensor_node(self):
        """Simulate Arduino + GSM sensor node"""
        print("��️ SENSOR NODE (Arduino + GSM Module)")
        print("=" * 50)
        print("Device: Solar-Surv Vaccine Monitor")
        print("Location: Rural Clinic, Kenya")
        print("Power: Solar Panel + Battery")
        print("Communication: GSM 2G Network")
        print("=" * 50)
        
        temperatures = [4.2, 5.1, 6.3, 8.9, 9.5, 1.2, 2.1, 4.8]
        battery_levels = [3.8, 3.7, 3.6, 3.5, 3.4, 3.3, 3.2, 3.1]
        
        for i, temp in enumerate(temperatures):
            battery = battery_levels[i]
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Reading sensors...")
            print(f"Temperature: {temp}°C")
            print(f"Battery: {battery}V")
            
            # Check thresholds
            if temp > 8.0:
                print("🚨 ALERT: Temperature too hot!")
                print(f"📱 Sending SMS: VACCINE ALERT: Temperature {temp}°C is TOO HOT!")
                print("   SMS sent via GSM module to clinic phone")
            elif temp < 2.0:
                print("🚨 ALERT: Temperature too cold!")
                print(f"�� Sending SMS: VACCINE ALERT: Temperature {temp}°C is TOO COLD!")
                print("   SMS sent via GSM module to clinic phone")
            else:
                print("✅ Status: Normal temperature")
            
            if battery < 3.3:
                print("⚠️ ALERT: Battery low!")
                print(f"📱 Sending SMS: BATTERY LOW: {battery}V - Device may shut down")
                print("   SMS sent via GSM module to clinic phone")
            
            time.sleep(3)
        
        print("\n🔴 EMERGENCY BUTTON PRESSED!")
        print("📱 Sending SMS: EMERGENCY ALERT: Manual emergency button pressed!")
        print("   SMS sent via GSM module to clinic phone")
        
        self.sensor_running = False
    
    def simulate_receiver_phone(self):
        """Simulate button phone receiving SMS"""
        print("\n📱 RECEIVER PHONE (Button Phone)")
        print("=" * 50)
        print("Phone: Basic Nokia/Button Phone")
        print("Location: Clinic Office")
        print("Network: 2G GSM")
        print("Internet: Not required")
        print("=" * 50)
        
        time.sleep(2)
        
        # Simulate receiving SMS alerts
        sms_messages = [
            "�� VACCINE ALERT: Temperature 8.9°C is TOO HOT! Safe range: 2-8°C",
            "⚠️ BATTERY LOW: 3.6V - Device may shut down soon",
            "�� VACCINE ALERT: Temperature 1.2°C is TOO COLD! Safe range: 2-8°C",
            "🚨 EMERGENCY ALERT: Manual emergency button pressed!"
        ]
        
        for i, message in enumerate(sms_messages, 1):
            print(f"\n📱 NEW SMS #{i}")
            print(f"From: Solar-Surv Device")
            print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
            print(f"Message: {message}")
            print("🔔 Phone vibrating...")
            print("📞 Ring ring...")
            print("�� LED flashing...")
            time.sleep(2)
        
        print("\n📱 SMS INBOX:")
        print("1. NEW | 14:32 | Solar-Surv | VACCINE ALERT: Temperature 8.9°C...")
        print("2. NEW | 14:35 | Solar-Surv | BATTERY LOW: 3.6V...")
        print("3. NEW | 14:38 | Solar-Surv | VACCINE ALERT: Temperature 1.2°C...")
        print("4. NEW | 14:41 | Solar-Surv | EMERGENCY ALERT: Manual emergency...")
        
        self.receiver_running = False
    
    def run_demo(self):
        """Run the complete SMS system demo"""
        print("🌡️ Solar-Surv SMS-Based Offline Health Alert System")
        print("=" * 60)
        print("Demonstrating offline vaccine monitoring with SMS alerts")
        print("=" * 60)
        
        # Start sensor node
        self.sensor_running = True
        sensor_thread = threading.Thread(target=self.simulate_sensor_node)
        sensor_thread.start()
        
        # Wait a bit, then start receiver
        time.sleep(5)
        self.receiver_running = True
        receiver_thread = threading.Thread(target=self.simulate_receiver_phone)
        receiver_thread.start()
        
        # Wait for both to complete
        sensor_thread.join()
        receiver_thread.join()
        
        print("\n" + "=" * 60)
        print("🎯 DEMO COMPLETE - Key Points:")
        print("=" * 60)
        print("✅ Completely offline (no internet required)")
        print("✅ Works with basic button phones")
        print("✅ Real-time temperature monitoring")
        print("✅ Immediate SMS alerts")
        print("✅ Solar powered for remote areas")
        print("✅ Cost effective (~$0.02 per SMS)")
        print("✅ Scalable to multiple clinics")
        print("=" * 60)

def main():
    demo = SMSDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()