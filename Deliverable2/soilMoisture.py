
import ADC
import time

def init():
    ADC.setup()

def run():
    res = ADC.getADC(0)
    moisture = 255 - res
  
    return moisture

if __name__ == '__main__':
    init()
    try:
        run()
    except KeyboardInterrupt: 
        ADC.destroy()
        print ('The end !')
