// Solar-Surv: Vaccine Cold Chain Monitor
// Offline Temperature Alert System for Vaccine Storage
// Monitors fridge temperature and sends alerts via LoRa when outside 2-8°C range

#include <SPI.h>
#include <LoRa.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <EEPROM.h>

// Pin definitions
#define TEMP_SENSOR_PIN 2        // DS18B20 temperature sensor
#define EMERGENCY_BUTTON_PIN 3   // Manual alert button
#define LED_PIN 4                // Status LED
#define BUZZER_PIN 5             // Alert buzzer
#define BATTERY_PIN A1           // Battery voltage monitoring
#define POTENTIOMETER_PIN A0     // For temperature simulation

// Temperature thresholds (Vaccine storage requirements)
#define TEMP_MIN 2.0             // Minimum safe temperature (°C)
#define TEMP_MAX 8.0             // Maximum safe temperature (°C)
#define BATTERY_LOW 3.3          // Low battery threshold (V)

// Device configuration
#define DEVICE_ID_ADDR 0
#define DEVICE_ID_DEFAULT 0x01
#define SENSOR_INTERVAL 5000     // Read temperature every 5 seconds
#define HEARTBEAT_INTERVAL 30000 // Send status every 30 seconds
#define ALERT_TIMEOUT 10000      // Alert timeout (10 seconds)

// Data structures
struct VaccineMonitorData {
  uint8_t deviceId;
  uint32_t timestamp;
  float temperature;
  float batteryVoltage;
  bool emergencyPressed;
  bool alertActive;
  uint8_t alertType;  // 0=none, 1=too hot, 2=too cold, 3=emergency, 4=battery
};

struct AlertMessage {
  uint8_t deviceId;
  uint8_t alertType;
  uint32_t timestamp;
  float temperature;
  char message[40];
};

// Global variables
OneWire oneWire(TEMP_SENSOR_PIN);
DallasTemperature tempSensor(&oneWire);
VaccineMonitorData currentData;
AlertMessage alertMsg;
unsigned long lastSensorRead = 0;
unsigned long lastHeartbeat = 0;
bool alertActive = false;
uint8_t deviceId;
bool useSimulation = true;  // Set to false when real sensor is connected

void setup() {
  Serial.begin(9600);
  
  // Initialize pins
  pinMode(EMERGENCY_BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Initialize LoRa
  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa init failed!");
    while (1);
  }
  LoRa.setTxPower(20);
  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(125E3);
  
  // Initialize temperature sensor
  tempSensor.begin();
  
  // Get or set device ID
  deviceId = EEPROM.read(DEVICE_ID_ADDR);
  if (deviceId == 0xFF) {
    deviceId = DEVICE_ID_DEFAULT;
    EEPROM.write(DEVICE_ID_ADDR, deviceId);
  }
  
  // Initialize data structure
  currentData.deviceId = deviceId;
  currentData.alertActive = false;
  currentData.alertType = 0;
  
  Serial.println("=== Solar-Surv Vaccine Cold Chain Monitor ===");
  Serial.print("Device ID: ");
  Serial.println(deviceId);
  Serial.println("Monitoring temperature range: 2-8°C");
  Serial.println("Press emergency button for manual alert");
  
  // Startup sequence
  startupSequence();
}

void loop() {
  unsigned long currentTime = millis();
  
  // Read temperature every SENSOR_INTERVAL
  if (currentTime - lastSensorRead >= SENSOR_INTERVAL) {
    readTemperature();
    checkTemperatureThresholds();
    lastSensorRead = currentTime;
  }
  
  // Send heartbeat every HEARTBEAT_INTERVAL
  if (currentTime - lastHeartbeat >= HEARTBEAT_INTERVAL) {
    sendHeartbeat();
    lastHeartbeat = currentTime;
  }
  
  // Check emergency button
  if (digitalRead(EMERGENCY_BUTTON_PIN) == LOW) {
    triggerEmergencyAlert();
    delay(1000);  // Debounce
  }
  
  // Handle alert timeout
  if (alertActive && (currentTime - lastSensorRead >= ALERT_TIMEOUT)) {
    clearAlert();
  }
  
  delay(100);
}

void readTemperature() {
  if (useSimulation) {
    // Simulate temperature using potentiometer (0-1023 maps to -5 to 15°C)
    int tempRaw = analogRead(POTENTIOMETER_PIN);
    currentData.temperature = map(tempRaw, 0, 1023, -50, 150) / 10.0;  // -5.0 to 15.0°C
  } else {
    // Read real temperature sensor
    tempSensor.requestTemperatures();
    currentData.temperature = tempSensor.getTempCByIndex(0);
  }
  
  // Read battery voltage
  int batteryRaw = analogRead(BATTERY_PIN);
  currentData.batteryVoltage = (batteryRaw * 5.0 / 1023.0) * 2.0;  // Voltage divider
  
  // Check emergency button
  currentData.emergencyPressed = (digitalRead(EMERGENCY_BUTTON_PIN) == LOW);
  
  // Update timestamp
  currentData.timestamp = millis();
  
  // Print temperature status
  Serial.print("Temperature: ");
  Serial.print(currentData.temperature, 1);
  Serial.print("°C (");
  if (currentData.temperature < TEMP_MIN) {
    Serial.print("TOO COLD");
  } else if (currentData.temperature > TEMP_MAX) {
    Serial.print("TOO HOT");
  } else {
    Serial.print("SAFE");
  }
  Serial.print("), Battery: ");
  Serial.print(currentData.batteryVoltage, 1);
  Serial.println("V");
}

void checkTemperatureThresholds() {
  bool newAlert = false;
  uint8_t alertType = 0;
  String alertMessage = "";
  
  // Check if temperature is too hot
  if (currentData.temperature > TEMP_MAX) {
    newAlert = true;
    alertType = 1;
    alertMessage = "VACCINE ALERT: Temperature too hot! " + String(currentData.temperature, 1) + "°C";
  }
  // Check if temperature is too cold
  else if (currentData.temperature < TEMP_MIN) {
    newAlert = true;
    alertType = 2;
    alertMessage = "VACCINE ALERT: Temperature too cold! " + String(currentData.temperature, 1) + "°C";
  }
  
  // Check battery level
  if (currentData.batteryVoltage < BATTERY_LOW) {
    newAlert = true;
    alertType = 4;
    alertMessage = "Battery low: " + String(currentData.batteryVoltage, 1) + "V";
  }
  
  if (newAlert && !alertActive) {
    triggerAlert(alertType, alertMessage);
  }
}

void triggerAlert(uint8_t type, String message) {
  alertActive = true;
  currentData.alertActive = true;
  currentData.alertType = type;
  
  // Create alert message
  alertMsg.deviceId = deviceId;
  alertMsg.alertType = type;
  alertMsg.timestamp = millis();
  alertMsg.temperature = currentData.temperature;
  message.toCharArray(alertMsg.message, 40);
  
  // Send LoRa alert
  LoRa.beginPacket();
  LoRa.write((uint8_t*)&alertMsg, sizeof(alertMsg));
  LoRa.endPacket();
  
  // Visual and audio alerts
  digitalWrite(LED_PIN, HIGH);
  if (type == 1 || type == 2) {
    // Critical temperature alert - continuous buzzer
    tone(BUZZER_PIN, 2000, 200);
    delay(200);
    tone(BUZZER_PIN, 2000, 200);
  } else {
    // Other alerts - single beep
    tone(BUZZER_PIN, 1000, 500);
  }
  
  Serial.println("?? ALERT SENT: " + message);
}

void triggerEmergencyAlert() {
  String message = "EMERGENCY: Manual alert triggered!";
  triggerAlert(3, message);
}

void sendHeartbeat() {
  // Send regular monitoring data
  LoRa.beginPacket();
  LoRa.write((uint8_t*)&currentData, sizeof(currentData));
  LoRa.endPacket();
  
  Serial.println("Status update sent");
}

void clearAlert() {
  alertActive = false;
  currentData.alertActive = false;
  currentData.alertType = 0;
  digitalWrite(LED_PIN, LOW);
  noTone(BUZZER_PIN);
  Serial.println("Alert cleared");
}

void startupSequence() {
  // Blink LED 3 times to indicate startup
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(300);
    digitalWrite(LED_PIN, LOW);
    delay(300);
  }
  
  // Play startup sound
  tone(BUZZER_PIN, 800, 200);
  delay(300);
  tone(BUZZER_PIN, 1200, 200);
}
