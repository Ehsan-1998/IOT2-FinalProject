# -*- coding: utf-8 -*-  # Add this line at the top of your file

import ADC0832
import time
import RPi.GPIO as GPIO
from time import sleep
import thermistor
import soilMoisture
import photoresistor
import RGBLed
import dcmotor

# GPIO pin definitions
FAN_PIN_A = 25
FAN_PIN_B = 12
PUMP_PIN_A = 20
PUMP_PIN_B = 21
LED_RED_PIN = 13
LED_GREEN_PIN = 19
LED_BLUE_PIN = 26

# User-defined thresholds (can be set by the user)
TEMP_THRESHOLD = 30  # Temperature threshold in Celsius
MOISTURE_THRESHOLD = 150  # Soil moisture threshold
DAYLIGHT_THRESHOLD = 128  # Light level threshold to distinguish day/night

# Initialize GPIO and components
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN_A, GPIO.OUT)
    GPIO.setup(FAN_PIN_B, GPIO.OUT)
    GPIO.setup(PUMP_PIN_A, GPIO.OUT)
    GPIO.setup(PUMP_PIN_B, GPIO.OUT)
    GPIO.setup(LED_RED_PIN, GPIO.OUT)
    GPIO.setup(LED_GREEN_PIN, GPIO.OUT)
    GPIO.setup(LED_BLUE_PIN, GPIO.OUT)

    # Initialize PWM for LED colors
    global pwm_red, pwm_green, pwm_blue
    pwm_red = GPIO.PWM(LED_RED_PIN, 100)
    pwm_green = GPIO.PWM(LED_GREEN_PIN, 100)
    pwm_blue = GPIO.PWM(LED_BLUE_PIN, 100)
    pwm_red.start(0)
    pwm_green.start(0)
    pwm_blue.start(0)

    # Initialize PWM for fan control
    global pwm_fan
    pwm_fan = GPIO.PWM(FAN_PIN_A, 50)  # 50Hz frequency for PWM control
    pwm_fan.start(0)  # Start with 0% duty cycle (fan off)

    ADC0832.setup()

# Map function for LED color control
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Set grow lamp color
def set_led_color(color):
    r_val = map_value((color & 0xFF0000) >> 16, 0, 255, 0, 100)
    g_val = map_value((color & 0x00FF00) >> 8, 0, 255, 0, 100)
    b_val = map_value((color & 0x0000FF), 0, 255, 0, 100)
    pwm_red.ChangeDutyCycle(100 - r_val)
    pwm_green.ChangeDutyCycle(100 - g_val)
    pwm_blue.ChangeDutyCycle(100 - b_val)

# Control fan speed using PWM
def control_fan_speed(speed):
    pwm_fan.ChangeDutyCycle(speed)

# Control pump
def control_pump(status):
    GPIO.output(PUMP_PIN_A, status)
    GPIO.output(PUMP_PIN_B, not status)

# Read sensors
def read_temperature():
    # Use the thermistor module to read temperature
    return thermistor.read_temperature()  # Modify this to fit your thermistor module

def read_soil_moisture():
    # Use soilMoisture module to read moisture
    return soilMoisture.read_moisture()  # Modify this to fit your soilMoisture module

def read_light_level():
    # Use photresistor module to read light level
    return photresistor.read_light()  # Modify this to fit your photresistor module

# Main control loop
def main_loop():
    try:
        while True:
            # Read sensor values
            temperature = read_temperature()
            moisture = read_soil_moisture()
            light_level = read_light_level()

            print(f"Temperature: {temperature}\u00b0C, Moisture: {moisture}, Light Level: {light_level}")

            # Control fan speed based on temperature
            if temperature > TEMP_THRESHOLD:
                fan_speed = min((temperature - TEMP_THRESHOLD) * 10, 100)  # Scale speed with temperature
                print(f"Setting fan speed to {fan_speed}%")
                control_fan_speed(fan_speed)
                sleep(5)  # Run fan for 5 seconds
                control_fan_speed(0)  # Turn off fan
            else:
                print("Turning off fan.")
                control_fan_speed(0)

            # Control water pump if soil moisture is low
            if moisture < MOISTURE_THRESHOLD:
                print("Activating water pump...")
                control_pump(True)
                sleep(5)  # Run water pump for 5 seconds
                control_pump(False)
            else:
                print("Soil moisture sufficient, pump off.")

            # Control grow lamp based on light level (day/night)
            if light_level < DAYLIGHT_THRESHOLD:
                print("It's dark, turning on grow lamp.")
                set_led_color(0x00FF00)  # Green for grow light
            else:
                print("It's bright, turning off grow lamp.")
                set_led_color(0x000000)  # Off (lamp off)

            sleep(1)  # Main loop delay

    except KeyboardInterrupt:
        pwm_fan.stop()
        GPIO.cleanup()
        print("Exiting program.")

# Run the program
if __name__ == "__main__":
    setup()  # Initialize GPIO and sensors
    main_loop()  # Start the main control loop
