import RPi.GPIO as GPIO  # Import GPIO to manage warnings
import ADC0832
import time

def init():
    ADC0832.setup()

def run():
    res = ADC0832.getADC(0)
    moisture = 255 - res
    print(f"Moisture: {moisture}")
    return moisture

if __name__ == '__main__':
    GPIO.setwarnings(False)  # Disable GPIO warnings
    try:
        init()
        while True:
            run()
            time.sleep(1)
    except KeyboardInterrupt:
        ADC0832.destroy()
        print('The end!')
