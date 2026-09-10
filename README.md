# Closed-Loop Thermal Regulation System

Automated closed-loop temperature control system utilizing stepped PWM fan actuation, an L298N H-bridge driver, a DHT11 environmental sensor, and a TM1637 4-digit display for real-time telemetry.

---

## Overview

The system regulates ambient temperature by driving a DC cooling fan with progressive PWM duty cycles based on strict thermal thresholds. It reads ambient conditions every second, updates the local display, and adjusts fan speed dynamically to restore thermal equilibrium.

### Hardware Setup
* **Microcontroller:** Arduino / ESP compatible board
* **Sensing:** DHT11 Digital Temperature & Humidity Sensor
* **Driver:** L298N Dual H-Bridge Motor Driver
* **Actuator:** 12V DC Cooling Fan (PWM-controlled)
* **Display:** TM1637 4-Digit 7-Segment Display

---

## Pinout Mapping

| Component | Pin Function | Board GPIO / Pin |
| :--- | :--- | :---: |
| **DHT11 Sensor** | Data Out | `GPIO 4` |
| **L298N Driver** | IN1 (Direction) | `GPIO 14` |
| **L298N Driver** | IN2 (Direction) | `GPIO 12` |
| **L298N Driver** | ENA (PWM Speed) | `GPIO 5` |
| **TM1637 Display** | CLK (Clock) | `GPIO 0` |
| **TM1637 Display** | DIO (Data) | `GPIO 2` |

---

## Control Logic & Duty Cycles

The controller applies a multi-stage stepped PWM curve to ensure acoustic comfort and energy efficiency at lower temperatures, scaling up to maximum throughput during thermal peaks:

| Temperature Range (°C) | Target State | PWM Value (0–255) | Duty Cycle (%) |
| :---: | :---: | :---: | :---: |
| **< 26.2** | Idle / Off | `0` | 0% |
| **26.2 – 26.4** | Stage 1 (Low) | `26` | ~20% |
| **26.5 – 26.9** | Stage 2 (Low-Mid) | `31` | ~40% |
| **27.0 – 27.1** | Stage 3 (Medium) | `57` | ~60% |
| **27.2 – 27.4** | Stage 4 (High) | `82` | ~80% |
| **≥ 27.5** | Stage 5 (Max) | `108` | 100% (voltage-capped) |

---

## Key Features
* **Sensor Error Handling:** Guard clauses prevent erratic controller states if sensor communication drops (`isnan()` check).
* **Live Telemetry:** Outputs current temperature with decimal precision and degree unit notation (`XX.X C`) directly on the 7-segment panel.
* **Driver Isolation:** Separation of logic signals and motor power via H-bridge prevents inductive kickback into the microcontroller.

---

## Installation & Setup

1. Open the project in the **Arduino IDE** or **PlatformIO**.
2. Install dependencies via the Library Manager:
   * `DHT sensor library` by Adafruit
   * `TM1637Display` by Avishay Orpaz
3. Flash the code to your board.

---

## Hardware Demonstration

* **Fan Speed & Stepped PWM Control:** [Watch Video](Video%20Project%203.mp4)
* **Real-Time Telemetry & Thermal Response:** [Watch Video](WhatsApp%20Video%202026-09-10%20at%2012.30.28.mp4)
