"""Control the LEDs on the panel buttons."""

import gpiozero

import pi_header_pinout

BUTTON_1_PIN = pi_header_pinout.BUTTON_1_GPIO_PIN
BUTTON_2_PIN = pi_header_pinout.BUTTON_2_GPIO_PIN
BUTTON_3_PIN = pi_header_pinout.BUTTON_3_GPIO_PIN
BUTTON_4_PIN = pi_header_pinout.BUTTON_4_GPIO_PIN
LED_1_PIN = pi_header_pinout.BUTTON_1_LED_GPIO_PIN
LED_2_PIN = pi_header_pinout.BUTTON_2_LED_GPIO_PIN
LED_3_PIN = pi_header_pinout.BUTTON_3_LED_GPIO_PIN
LED_4_PIN = pi_header_pinout.BUTTON_4_LED_GPIO_PIN


class PanelButtonLEDsController:
    """Controls the panel button LEDs."""

    def __init__(self):
        # Maps button pins to corresponding LED pins.
        self.leds = {
            BUTTON_1_PIN: gpiozero.LED(LED_1_PIN, active_high=False),
            BUTTON_2_PIN: gpiozero.LED(LED_2_PIN),
            BUTTON_3_PIN: gpiozero.LED(LED_3_PIN),
            BUTTON_4_PIN: gpiozero.LED(LED_4_PIN)
        }

    def turn_on_led(self, button_pin: int):
        """Turn on the LED corresponding to the given button pin number."""
        self.leds[button_pin].on()

    def turn_off_led(self, button_pin: int):
        """Turn off the LED corresponding to the given button pin number."""
        self.leds[button_pin].off()

    def turn_off_all_leds(self):
        """Turn off all LEDS on the panel buttons."""
        for _, led in self.leds.items():
            led.off()

    def turn_on_all_leds(self):
        """Turn on all LEDS on the panel buttons."""
        for _, led in self.leds.items():
            led.on()
