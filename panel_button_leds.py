"""Control the LEDs on the panel buttons."""

import gpiozero

import pi_header_pinout

BUTTON_PINS = pi_header_pinout.BUTTON_GPIO_PINS
LED_PINS = pi_header_pinout.BUTTON_LED_GPIO_PINS


class PanelButtonLEDsController:
    """Controls the panel button LEDs."""

    def __init__(self):
        # Maps button pins to corresponding LED pins.
        self.leds = [
            gpiozero.LED(LED_PINS[0], active_high=False),  # RGB LED.
            gpiozero.LED(LED_PINS[1]),
            gpiozero.LED(LED_PINS[2]),
            gpiozero.LED(LED_PINS[3])
        ]

    def turn_on_led(self, led_index: int):
        """Turn on a LED."""
        self.leds[led_index].on()

    def turn_off_led(self, led_index: int):
        """Turn off a LED."""
        self.leds[led_index].off()

    def turn_off_all_leds(self):
        """Turn off all LEDS."""
        for led in self.leds:
            led.off()

    def turn_on_all_leds(self):
        """Turn on all LEDS."""
        for led in self.leds:
            led.on()
