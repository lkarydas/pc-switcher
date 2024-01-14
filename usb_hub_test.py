"""Manual test for USB hub control."""

import time
import usb_hub

controller = usb_hub.USBHubController()

position = controller.get_current_position()
print(f'Initial position: {position}')
print(f'This will switch to positions 1, 2, 3, 4 and then back to f{position}.')
print('Test starts in 3 seconds, go look at the USB hub.')
time.sleep(3)
print('Switching to position 1.')
controller.switch_to(1)
time.sleep(1)
print('Switching to position 2.')
controller.switch_to(2)
time.sleep(1)
print('Switching to position 3.')
controller.switch_to(3)
time.sleep(1)
print('Switching to position 4.')
controller.switch_to(4)
time.sleep(1)

print(f'Switching to initial position {position}.')
controller.switch_to(position)

print('Done.')
