"""Controls the USB hub."""
import time
import gpiozero

from absl import logging

import pi_header_pinout

POSITION_LED_PINS = pi_header_pinout.USB_HUB_POSITION_LEDS_GPIO_PINS
BUTTON_PIN = pi_header_pinout.USB_HUB_BUTTON_GPIO_PIN
MAX_ATTEMPTS_TO_READ_LED_VALUE = 3

class USBHubController:
    """Controls the USB hub."""

    def __init__(self):
        self.hub_led_input_devices = list(
            [gpiozero.InputDevice(pin) for pin in POSITION_LED_PINS])
        self.hub_button = gpiozero.OutputDevice(BUTTON_PIN)

    def read_led_values(self):
        """Read the LED values from USB switch and return them."""
        for _ in range(0, MAX_ATTEMPTS_TO_READ_LED_VALUE):
            led_values = list(
                [device.value for device in self.hub_led_input_devices])
            if sum(led_values) != 1:
                time.sleep(0.1)
                continue  # Discard transitions between LEDs.
            return led_values

    def get_current_position(self):
        """Returns the current position of the USB switch."""
        led_values = self.read_led_values()
        if not led_values:
            logging.error('Error - led values is: %s', led_values)
            return 0
        current_position = led_values.index(1) + 1
        return current_position

    def press_hub_button(self):
        """Simulate a button press to the USB switch (advances to next input)."""
        self.hub_button.on()
        time.sleep(0.1)
        self.hub_button.off()

    def switch_to(self, position):
        """Switch USB switch to a specific position."""
        current_position = self.get_current_position()
        while current_position != position:
            self.press_hub_button()
            time.sleep(0.1)
            current_position = self.get_current_position()
