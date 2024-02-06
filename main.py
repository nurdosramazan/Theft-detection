from machine import Pin, SoftI2C, RTC, deepsleep, time_pulse_us
import time, message, machine
from mpu6050 import MPU6050

# Constants
MOVEMENT_THRESHOLD = 500  # Threshold for accelerometer
DISTANCE_THRESHOLD = 10  # Threshold for US, 10cm
DEEP_SLEEP_TIME = 60000  # Time in milliseconds, e.g., 1 minutes
SOUND_SPEED = 343  # Speed of sound in air in m/s
TRIG_PIN = 23  # Trigger pin for Ultrasonic Sensor
ECHO_PIN = 22  # Echo pin for Ultrasonic Sensor
SDA_PIN = 19  # SDA pin for MPU6050
SCL_PIN = 18  # SCL pin for MPU6050
CHECK_INTERVAL = 2  # Time between checks in seconds in case of potential theft
MAX_CHECKS = 3  # Maximum number of checks before confirming a theft

# MPU6050 Setup
i2c = SoftI2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
mpu = MPU6050(i2c)

# Ultrasonic Sensor Setup
trig_pin = Pin(TRIG_PIN, Pin.OUT)
echo_pin = Pin(ECHO_PIN, Pin.IN)

# RTC for storing initial distance
rtc = RTC()

def read_distance():
    trig_pin.value(0)  # Ensure trigger is LOW
    time.sleep_us(2)
    trig_pin.value(1)  # Set trigger HIGH
    time.sleep_us(10)  # Wait 10 microseconds
    trig_pin.value(0)  # Set trigger back to LOW

    pulse_duration = time_pulse_us(echo_pin, 1)
    distance = (pulse_duration * SOUND_SPEED) / (2 * 10000)
    return distance

def store_to_rtc(distance, readings):
    data_str = f"{distance},{readings['x']},{readings['y']},{readings['z']}"
    rtc.memory(bytearray(data_str, 'utf-8'))
    
def retrieve_from_rtc():
    data_str = rtc.memory().decode('utf-8')
    distance_str, x_str, y_str, z_str = data_str.split(',')

    distance = float(distance_str)
    readings = {'x': float(x_str), 'y': float(y_str), 'z': float(z_str)}
    
    print("Data in RTC: {}, {}".format(distance, readings))

    return distance, readings

def check_movement(previous_readings, current_readings, threshold=MOVEMENT_THRESHOLD):
    for axis in ['x', 'y', 'z']:
        if abs(previous_readings[axis] - current_readings[axis]) > threshold:
            return True
    return False

def perform_checks(initial_distance):
    for _ in range(MAX_CHECKS):
        current_distance = read_distance()
        print(current_distance)
        if abs(current_distance - initial_distance) <= DISTANCE_THRESHOLD:
            return False  # Object is in place, no theft
        time.sleep(CHECK_INTERVAL)
    return True  # Potential theft detected

def main():
    time.sleep(2)
    initial_distance_data = rtc.memory()

    if not initial_distance_data:
        initial_distance = read_distance()
        previous_readings = mpu.get_accel_data()
        store_to_rtc(initial_distance, previous_readings)
    else:
        initial_distance, previous_readings = retrieve_from_rtc()

    while True:
        time.sleep(0.1)
        current_readings = mpu.get_accel_data()
        print(current_readings)
        if check_movement(previous_readings, current_readings):
            print("Motion detected")
            if perform_checks(initial_distance):
                print("Potential theft detected!")
                message.connect_to_wifi()
                #first string is receivers email, check spam box if you can't find it
                message.send_email('nurmukhammed.tangatarov@nu.edu.kz', 'Theft Alert', 'A potential theft has been detected!')
                time.sleep(5)

            else:
                store_to_rtc(initial_distance, current_readings)
                print("False positive from accelerometer")
                deepsleep(DEEP_SLEEP_TIME)
        else:
            print("Going to Deep Sleep")
            deepsleep(DEEP_SLEEP_TIME)

if __name__ == "__main__":
    main()