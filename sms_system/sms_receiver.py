#!/usr/bin/env python3
"""
Solar-Surv: SMS Receiver Simulation
Simulates receiving SMS alerts on a button phone
"""

import time
import random
from datetime import datetime

class SMSReceiver:
    def __init__(self, phone_number="+1234567890"):
        self.phone_number = phone_number
        self.received_sms = []
        self.alert_count = 0
        
    def receive_sms(self, message, sender="Solar-Surv"):
        """Simulate receiving SMS on button phone"""
        timestamp = datetime.now()
        sms = {
            'timestamp': timestamp,
            'sender': sender,
            'message': message,
            'read': False
        }
        
        self.received_sms.append(sms)
        self.alert_count += 1
        
        # Simulate phone notification
        print(f"\n�� NEW SMS RECEIVED on {self.phone_number}")
        print(f"   From: {sender}")
        print(f"   Time: {timestamp.strftime('%H:%M:%S')}")
        print(f"   Message: {message}")
        print(f"   Total Alerts: {self.alert_count}")
        print("=" * 60)
        
        # Simulate phone vibration/ring
        self.simulate_phone_notification()
    
    def simulate_phone_notification(self):
        """Simulate phone vibration and ring"""
        print("🔔 Phone vibrating...")
        print("📞 Ring ring...")
        print("💡 LED flashing...")
        time.sleep(1)
    
    def show_sms_inbox(self):
        """Show SMS inbox (like on button phone)"""
        print(f"\n📱 SMS INBOX - {self.phone_number}")
        print("=" * 40)
        
        if not self.received_sms:
            print("No messages")
            return
        
        for i, sms in enumerate(self.received_sms[-10:], 1):  # Show last 10
            status = "NEW" if not sms['read'] else "READ"
            print(f"{i}. {status} | {sms['timestamp'].strftime('%H:%M')} | {sms['sender']}")
            print(f"   {sms['message'][:50]}...")
            print()
    
    def mark_as_read(self, index):
        """Mark SMS as read"""
        if 0 <= index < len(self.received_sms):
            self.received_sms[index]['read'] = True
            print(f"✅ SMS {index + 1} marked as read")
    
    def simulate_button_phone_interface(self):
        """Simulate button phone SMS interface"""
        print("�� Button Phone SMS Interface")
        print("=" * 30)
        print("1. View Inbox")
        print("2. Read Message")
        print("3. Delete Message")
        print("4. Exit")
        
        while True:
            try:
                choice = input("\nSelect option (1-4): ").strip()
                
                if choice == "1":
                    self.show_sms_inbox()
                elif choice == "2":
                    self.show_sms_inbox()
                    if self.received_sms:
                        msg_num = int(input("Enter message number to read: ")) - 1
                        if 0 <= msg_num < len(self.received_sms):
                            sms = self.received_sms[msg_num]
                            print(f"\n�� MESSAGE {msg_num + 1}:")
                            print(f"From: {sms['sender']}")
                            print(f"Time: {sms['timestamp'].strftime('%H:%M:%S')}")
                            print(f"Message: {sms['message']}")
                            self.mark_as_read(msg_num)
                elif choice == "3":
                    self.show_sms_inbox()
                    if self.received_sms:
                        msg_num = int(input("Enter message number to delete: ")) - 1
                        if 0 <= msg_num < len(self.received_sms):
                            del self.received_sms[msg_num]
                            print(f"✅ SMS {msg_num + 1} deleted")
                elif choice == "4":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option")
                    
            except (ValueError, IndexError):
                print("Invalid input")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

def main():
    print("📱 Solar-Surv SMS Receiver Simulation")
    print("Simulating button phone receiving vaccine alerts")
    print()
    
    # Create receiver
    receiver = SMSReceiver("+1234567890")
    
    # Simulate receiving some alerts
    print("Simulating incoming SMS alerts...")
    time.sleep(2)
    
    receiver.receive_sms("�� VACCINE ALERT: Temperature 9.1°C is TOO HOT! Safe range: 2-8°C")
    time.sleep(3)
    
    receiver.receive_sms("⚠️ BATTERY LOW: 3.2V - Device may shut down soon")
    time.sleep(3)
    
    receiver.receive_sms("�� EMERGENCY ALERT: Manual emergency button pressed!")
    
    print("\n" + "="*60)
    print("Now simulating button phone interface...")
    print("="*60)
    
    # Show button phone interface
    receiver.simulate_button_phone_interface()

if __name__ == "__main__":
    main()