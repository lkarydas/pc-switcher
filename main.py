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
# No flags for now.

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
    while True:  
      new_led_values = ([GPIO.input(LED_1), GPIO.input(LED_2), GPIO.input(LED_3), GPIO.input(LED_4)])
      if sum(new_led_values) != 1:
        continue  # Discard transitions between LEDs.
      if new_led_values != led_values:
        led_values = new_led_values
        print(led_values.index(1) + 1)
    time.sleep(0.3)
  
  except KeyboardInterrupt:  
    print('\nBye!')
  
  except Exception as e:  
    print(str(e))
  
  finally:  
    GPIO.cleanup()

if __name__ == '__main__':
  app.run(main)
