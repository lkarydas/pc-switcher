"""Manual test for the LEDs on the panel buttons."""

import time
import pi_header_pinout
import panel_button_leds


BUTTON_PINS = [
    pi_header_pinout.BUTTON_1_GPIO_PIN,
    pi_header_pinout.BUTTON_2_GPIO_PIN,
    pi_header_pinout.BUTTON_3_GPIO_PIN,
    pi_header_pinout.BUTTON_4_GPIO_PIN,
]

controller = panel_button_leds.PanelButtonLEDsController()

print('This will turn on and off each LED in order.')

for i in range(4):
    print(f'Turning on LED {i + 1}.')
    controller.turn_on_led(BUTTON_PINS[i])
    time.sleep(1)
    controller.turn_off_led(BUTTON_PINS[i])
    time.sleep(0.5)
print('Done.')
