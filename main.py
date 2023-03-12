import time

from absl import app
from absl import flags

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print('Error importing RPi.GPIO!'
          'This is probably because you need superuser privileges.'
          'You can achieve this by using "sudo" to run your script')

FLAGS = flags.FLAGS
flags.DEFINE_integer("num_times", 1,
                     "Number of times to print greeting.")

# Set up GPIO pins.
GPIO.setmode(GPIO.BOARD)
LED_2 = 7
LED_1 = 11
LED_3 = 13
LED_4 = 15
GPIO.setup(LED_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def main(argv):
  del argv  # Unused.
  led_values = [0, 0, 0, 0]
  try:  
    # here you put your main loop or block of code  
    while True:  
      new_led_values = ([GPIO.input(LED_1), GPIO.input(LED_2), GPIO.input(LED_3), GPIO.input(LED_4)])
      if sum(new_led_values) != 1:
        continue  # Transition between LEDs.
      if new_led_values != led_values:
        led_values = new_led_values
        print(led_values.index(1) + 1)
    time.sleep(0.3)
  
  except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print('\nBye!') # print value of counter  
  
  except Exception as e:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print(str(e))
  
  finally:  
    GPIO.cleanup() # this ensures a clean exit  


if __name__ == '__main__':
  app.run(main)
