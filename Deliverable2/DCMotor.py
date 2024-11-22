import RPi.GPIO as GPIO
from time import sleep

# Define motor pins
MotorPin_A = 25
MotorPin_B = 12

# Setup GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(MotorPin_A, GPIO.OUT)
GPIO.setup(MotorPin_B, GPIO.OUT)

def motor(status, direction):
    if status == 0:  # Stop
        GPIO.output(MotorPin_A, GPIO.HIGH)
        GPIO.output(MotorPin_B, GPIO.HIGH)
    else:  # Run
        if direction == 0:  # Clockwise
            GPIO.output(MotorPin_A, GPIO.HIGH)
            GPIO.output(MotorPin_B, GPIO.LOW)
        else:  # Anticlockwise
            GPIO.output(MotorPin_A, GPIO.LOW)
            GPIO.output(MotorPin_B, GPIO.HIGH)

try:
    while True:
        motor(1, 1)  # Run anticlockwise
        sleep(5)

        motor(0, 1)  # Stop
        sleep(5)

        motor(1, 0)  # Run clockwise
        sleep(5)

except KeyboardInterrupt:
    print("Exiting program")
    GPIO.cleanup()
