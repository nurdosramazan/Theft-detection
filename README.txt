Project Title: ESP32 Theft Detection System

Description
This project involves an ESP32 microcontroller using an MPU6050 sensor for motion detection and an ultrasonic sensor for distance measurement. It sends email alerts if potential theft is detected.

Hardware Requirements
ESP32 Microcontroller
MPU6050 accelerometer and gyroscope sensor
Ultrasonic distance sensor (HC-SR04)

This project requires the following Python libraries:
urequests: For making HTTP requests (sending emails via Mailgun).
ubinascii: For ASCII conversions (used in email sending).
network: For Wi-Fi connectivity.

Setup Instructions
Download the necessary libraries: urequests, ubinascii, and network.
Connecting to Wi-Fi
Update the Wi-Fi credentials in the message.py script with your network's SSID and password.
Running the Script
Upload the main.py, message.py and mpu6050.py scripts to your ESP32.
Run main.py using Thonny IDE or by resetting the ESP32.

Wiring Instructions
- Connect the SDA and SCL pins of the MPU-6050 to GPIO 19 and GPIO 18 on the ESP32, respectively.
- Connect the Trig and Echo pins of the US-015 sensor to GPIO 23 and GPIO 22 on the ESP32.
- Ensure all GND (ground) pins on the sensors are connected to a GND pin on the ESP32.
- Connect the VCC pin of the MPU-6050 to 3v3, and the VCC pin of the US-015 to 5v