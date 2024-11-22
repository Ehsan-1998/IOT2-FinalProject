import RPi.GPIO as GPIO
from time import sleep

# Define motor pins
MotorPin_A = 25
MotorPin_B = 12

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(MotorPin_A, GPIO.OUT)
GPIO.setup(MotorPin_B, GPIO.OUT)

# Setup PWM
pwm_A = GPIO.PWM(MotorPin_A, 100)  # 100 Hz frequency
pwm_B = GPIO.PWM(MotorPin_B, 100)
pwm_A.start(0)  # Start with 0% duty cycle (off)
pwm_B.start(0)

def motor(status, direction, speed=50):
    """
    Control motor status, direction, and speed.
    :param status: 0 (stop) or 1 (run)
    :param direction: 0 (clockwise) or 1 (anticlockwise)
    :param speed: Speed percentage (0 to 100)
    """
    if status == 0:  # Stop
        pwm_A.ChangeDutyCycle(0)
        pwm_B.ChangeDutyCycle(0)
    else:  # Run
        if direction == 0:  # Clockwise
            pwm_A.ChangeDutyCycle(speed)
            pwm_B.ChangeDutyCycle(0)
        else:  # Anticlockwise
            pwm_A.ChangeDutyCycle(0)
            pwm_B.ChangeDutyCycle(speed)

try:
    while True:
        motor(1, 1, speed=30)  # Run anticlockwise at 30% speed
        sleep(5)

        motor(0, 1)  # Stop
        sleep(5)

        motor(1, 0, speed=30)  # Run clockwise at 30% speed
        sleep(5)

except KeyboardInterrupt:
    print("Exiting program")
    pwm_A.stop()  # Stop PWM
    pwm_B.stop()
    GPIO.cleanup()
