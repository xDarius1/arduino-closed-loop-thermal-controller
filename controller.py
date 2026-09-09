/**
 * Closed-Loop Thermal Regulation System
 * Hardware: Arduino / ESP, DHT11 Sensor, L298N H-Bridge Driver, TM1637 4-Digit Display
 * Author: Darius Vasilache
 */

#include <DHT.h>
#include <TM1637Display.h>

// Sensor configuration
#define DHTPIN 4 
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// L298N H-Bridge motor driver pins
#define IN1 14  
#define IN2 12  
#define ENA 5   

// TM1637 7-Segment display configuration
#define CLK 0  
#define DIO 2  
TM1637Display display(CLK, DIO);

// Temperature threshold limits (°C)
#define TEMP_THRESHOLD_LOW_20     26.2
#define TEMP_THRESHOLD_LOW_40     26.5
#define TEMP_THRESHOLD_MEDIUM_60  27.0
#define TEMP_THRESHOLD_HIGH_80    27.2
#define TEMP_THRESHOLD_MAX_100    27.5

// PWM duty cycle limits (scaled for motor voltage headroom)
#define PWM_20   26
#define PWM_40   31
#define PWM_60   57
#define PWM_80   82
#define PWM_100  108

void setup() {
  Serial.begin(115200);
  dht.begin();
  display.setBrightness(2);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  // Initial state: Motor halted
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
}

void loop() {
  float temperature = dht.readTemperature();

  // Guard clause against sensor read errors
  if (isnan(temperature)) {
    Serial.println("Warning: Failed to read from DHT sensor!");
    delay(1000);
    return;
  }

  // Display temperature formatted as XX.X with 'C' symbol
  int tempDisplay = (int)(temperature * 10);
  display.showNumberDecEx(tempDisplay, 0b01000000, true, 3, 0);
  uint8_t degC[1] = {0x39}; // 'C' segment
  display.setSegments(degC, 1, 3);

  // Closed-loop stepped speed modulation
  if (temperature >= TEMP_THRESHOLD_MAX_100) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, PWM_100);
  } else if (temperature >= TEMP_THRESHOLD_HIGH_80) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, PWM_80);
  } else if (temperature >= TEMP_THRESHOLD_MEDIUM_60) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, PWM_60);
  } else if (temperature >= TEMP_THRESHOLD_LOW_40) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, PWM_40);
  } else if (temperature >= TEMP_THRESHOLD_LOW_20) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, PWM_20);
  } else {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, 0);
  }

  delay(1000);
}
