import RPi.GPIO as GPIO
from time import sleep

# Define RGB LED pins
LedPinRed = 13
LedPinGreen = 19
LedPinBlue = 26

# Colors (hexadecimal values)
colors = [
    0xFF0000,  # Red
    0x00FF00,  # Green
    0x0000FF,  # Blue
    0xFFFF00,  # Yellow
    0x00FFFF,  # Cyan
    0xFF00FF,  # Magenta
    0xFFFFFF,  # White
    0x9400D3   # Purple
]

# Initialize GPIO pins for PWM
def led_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LedPinRed, GPIO.OUT)
    GPIO.setup(LedPinGreen, GPIO.OUT)
    GPIO.setup(LedPinBlue, GPIO.OUT)
    global pwm_red, pwm_green, pwm_blue
    pwm_red = GPIO.PWM(LedPinRed, 100)
    pwm_green = GPIO.PWM(LedPinGreen, 100)
    pwm_blue = GPIO.PWM(LedPinBlue, 100)
    pwm_red.start(0)
    pwm_green.start(0)
    pwm_blue.start(0)

# Map function to convert values
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Set RGB LED color
def led_color_set(color):
    r_val = map_value((color & 0xFF0000) >> 16, 0, 255, 0, 100)
    g_val = map_value((color & 0x00FF00) >> 8, 0, 255, 0, 100)
    b_val = map_value((color & 0x0000FF), 0, 255, 0, 100)
    pwm_red.ChangeDutyCycle(100 - r_val)
    pwm_green.ChangeDutyCycle(100 - g_val)
    pwm_blue.ChangeDutyCycle(100 - b_val)

# Main loop
try:
    led_init()
    while True:
        for color in colors:
            led_color_set(color)
            sleep(0.5)
except KeyboardInterrupt:
    pwm_red.stop()
    pwm_green.stop()
    pwm_blue.stop()
    GPIO.cleanup()
