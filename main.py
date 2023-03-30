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

LED_2 = 15
LED_1 = 7
LED_3 = 11
LED_4 = 13
USB_SWITCH_BUTTON = 19
BUTTON_1 = 29
BUTTON_2 = 23
BUTTON_3 = 31

MAX_ATTEMPTS = 10

def read_led_values():
  for attempt in range(0, MAX_ATTEMPTS):
    led_values = ([GPIO.input(LED_1), GPIO.input(LED_2), GPIO.input(LED_3), GPIO.input(LED_4)])
    if sum(led_values) != 1:
      continue  # Discard transitions between LEDs.
    return led_values
    time.sleep(0.1)

def press_button():
  GPIO.output(USB_SWITCH_BUTTON, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(USB_SWITCH_BUTTON, GPIO.LOW)
  time.sleep(0.1)

def get_current_position():
  led_values = read_led_values()
  if not led_values:
    print('Error - led values is: %s' % led_values)
    return 0
  current_position = led_values.index(1) + 1
  #  print(f'Current_position: {current_position}')
  return current_position

def switch_to(position):
  current_position = get_current_position()
  while (current_position != position):
    press_button()
    current_position = get_current_position()

def button_callback_1(channel):
  print("Button 1 was pushed!")
  switch_to(1)

def button_callback_2(channel):
  print("Button 2 was pushed!")
  switch_to(2)

def button_callback_3(channel):
  print("Button 3 was pushed!")
  switch_to(3)

BOUNCE_TIME=700

def main(argv):
  del argv  # Unused.
  # Set up GPIO pins.
  GPIO.setmode(GPIO.BOARD)
  print('setting up led inputs.')
  GPIO.setup(LED_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(LED_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(LED_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(LED_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  print('setting up switch button output')
  GPIO.setup(USB_SWITCH_BUTTON, GPIO.OUT)
  GPIO.output(USB_SWITCH_BUTTON, GPIO.LOW)

  print('setting up panel buttons.')
  GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BUTTON_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  print('adding listeners')
  GPIO.add_event_detect(BUTTON_1, GPIO.FALLING ,callback=button_callback_1,
                        bouncetime=BOUNCE_TIME)
  GPIO.add_event_detect(BUTTON_2, GPIO.FALLING ,callback=button_callback_2,
                        bouncetime=BOUNCE_TIME)
  GPIO.add_event_detect(BUTTON_3, GPIO.FALLING ,callback=button_callback_3,
                        bouncetime=BOUNCE_TIME)
  print('Main loop.')
  position = 0
  try:
    while True:
      time.sleep(0.2)
      new_position = get_current_position()
      if (new_position != position):
        position = new_position
        print(f'Position: {position}')

  except KeyboardInterrupt:
    print('\nBye!')

  except Exception as e:
    print(str(e))

  finally:  
    GPIO.cleanup()

if __name__ == '__main__':
  app.run(main)
