"""Manual test for the LEDs on the panel buttons."""

import time
import pi_header_pinout
import panel_button_leds


controller = panel_button_leds.PanelButtonLEDsController()

print('This will flash all LEDs once, then turn them on and off sequentially.')

# Flash LEDs.
controller.turn_on_all_leds()
time.sleep(0.2)
controller.turn_off_all_leds()
time.sleep(0.5)

for i in range(4):
    print(f'Turning on LED {i + 1}.')
    controller.turn_on_led(i)
    time.sleep(0.6)
    controller.turn_off_led(i)
    time.sleep(0.1)
print('Done.')
