import sys
import time
import gpiozero
import signal
import dataclasses

from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS
# No flags for now.

@dataclasses.dataclass
class PanelButton:
  pin: int
  led_pin: int
  usb_position: int
  computer_name: str

_PANEL_BUTTON_MAP = {
  13: PanelButton(13, 0, 1, 'red'),
  5: PanelButton(5, 0, 2, 'white'),
  6: PanelButton(6, 0, 3, 'blue'),
}

USB_HUB_LED_PINS = [4, 22, 17, 27]
USB_HUB_BUTTON_PIN = 10


class PanelController:

  def __init__(self):
    self.hub_led_input_devices = list([gpiozero.InputDevice(pin) for pin in
                                USB_HUB_LED_PINS])
    self.hub_button = gpiozero.OutputDevice(USB_HUB_BUTTON_PIN)

  def button_callback(self, button):
    panel_button = _PANEL_BUTTON_MAP[button.pin.number]
    print('Button pressed! Pin: %s Color: %s' % (panel_button.pin,
                                                 panel_button.computer_name))
    print(f'Switching to {panel_button.usb_position}')
    self.switch_to(panel_button.usb_position)

  def register_button_callbacks(self):
    b1 = gpiozero.Button(5)
    b2 = gpiozero.Button(6)
    b3 = gpiozero.Button(13)
    b1.when_pressed = self.button_callback
    b2.when_pressed = self.button_callback
    b3.when_pressed = self.button_callback

  def press_hub_button(self):
    self.hub_button.on()
    time.sleep(0.1)
    self.hub_button.off()

  def switch_to(self, position):
    current_position = self.get_current_position()
    while (current_position != position):
      self.press_hub_button()
      time.sleep(0.1)
      current_position = self.get_current_position()

  def get_current_position(self):
    led_values = self.read_led_values()
    if not led_values:
      print('Error - led values is: %s' % led_values)
      return 0
    current_position = led_values.index(1) + 1
    #  print(f'Current_position: {current_position}')
    return current_position

  def read_led_values(self):
    for attempt in range(0, MAX_ATTEMPTS):
      led_values = list([device.value for device in self.hub_led_input_devices])
      if sum(led_values) != 1:
        time.sleep(0.1)
        continue  # Discard transitions between LEDs.
      return led_values


def main(argv):
  del argv  # Unused.
  logging.info('Main loop.')
  controller = PanelController()
  controller.register_button_callbacks()
  signal.pause()


if __name__ == '__main__':
  try:
    app.run(main)
  except KeyboardInterrupt:
    print('\nBye!')
    sys.exit(0);
