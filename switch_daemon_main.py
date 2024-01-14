"""Main daemon that runs on Raspberry Pi.

- Controls what happens when panel buttons are pressed.
- Sets USB hub to corresponding position.
- Sends TCP messages to Legion to switch monitor inputs.
- Sends IR commands to HDMI switch.
- Controls LED lights on panel buttons.
"""

import dataclasses
import sys
import signal
import time

import gpiozero

from absl import app
from absl import flags
from absl import logging

import hdmi_hub
import tcp_client

FLAGS = flags.FLAGS


@dataclasses.dataclass
class PanelButton:
    """Data class that represents a panel button."""
    pin: int
    led_pin: int
    usb_position: int
    computer_name: str
    button_color: str
    hdmi_position: int


_PANEL_BUTTON_MAP = {
    13: PanelButton(13, 0, 1, 'Dock', 'white', 1),
    5: PanelButton(5, 0, 2, 'Lenovo', 'red', 2),
    6: PanelButton(6, 0, 3, 'MSI', 'blue', 2),
    19: PanelButton(19, 0, 4, 'UM350', 'RGB', 4),
}

USB_HUB_LED_PINS = [4, 22, 15, 27]
USB_HUB_BUTTON_PIN = 10
MAX_ATTEMPTS = 3


class PanelController:
    """Controls what happens when panel buttons are pressed."""

    def __init__(self):
        self.hub_led_input_devices = list([gpiozero.InputDevice(pin) for pin in
                                           USB_HUB_LED_PINS])
        self.hub_button = gpiozero.OutputDevice(USB_HUB_BUTTON_PIN)
        self.button_leds = {
            5: gpiozero.LED(20),
            6: gpiozero.LED(16),
            13: gpiozero.LED(21),
            19: gpiozero.LED(12, active_high=False),
        }

    def button_callback(self, button):
        """Callback fn for panel button press."""
        panel_button = _PANEL_BUTTON_MAP[button.pin.number]
        print('')
        logging.info(
            'Button pressed! Pin: %s Switching to %s.',
            panel_button.pin,
            panel_button.computer_name)
        self.turn_off_all_button_leds()
        self.button_leds[button.pin.number].on()
        logging.info(
            f'Switching USB hub to position {panel_button.usb_position}.')
        self.switch_to(panel_button.usb_position)
        hdmi_position = panel_button.hdmi_position
        logging.info('hdmi_position: %i', hdmi_position)
        hdmi_hub.switch_to(2)  # So that C730 can send the DDC command.
        time.sleep(2)  # To give time for the HDMI swicth.
        if panel_button.computer_name == 'MSI':
            logging.info('Sending UDP command to switch monitor input to DP2.')
            tcp_client.send_message('DP2')
        else:
            logging.info(
                'Sending UDP command to switch monitor input to HDMI.')
            tcp_client.send_message('HDMI')
        hdmi_hub.switch_to(hdmi_position)

    def turn_off_all_button_leds(self):
        """Turn off all LEDS on the panel buttons."""
        for _, led in self.button_leds.items():
            led.off()

    def register_button_callbacks(self):
        """Register callbacks for panel buttons."""
        button_1 = gpiozero.Button(5)
        button_2 = gpiozero.Button(6)
        button_3 = gpiozero.Button(13)
        button_4 = gpiozero.Button(19)
        button_1.when_pressed = self.button_callback
        button_2.when_pressed = self.button_callback
        button_3.when_pressed = self.button_callback
        button_4.when_pressed = self.button_callback

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



    def read_led_values(self):
        """Read the LED values from USB switch and return them."""
        for _ in range(0, MAX_ATTEMPTS):
            led_values = list(
                [device.value for device in self.hub_led_input_devices])
            if sum(led_values) != 1:
                time.sleep(0.1)
                continue  # Discard transitions between LEDs.
            return led_values


def main(argv):
    """Main function."""
    del argv  # Unused.
    logging.set_verbosity(logging.INFO)
    logging.get_absl_handler().use_absl_log_file()
    logging.info('Main loop.')
    controller = PanelController()
    controller.register_button_callbacks()
    # Signal pause only works on Linux.
    signal.pause()  # pylint: disable=no-member


if __name__ == '__main__':
    try:
        app.run(main)
    except KeyboardInterrupt:
        print('')
        logging.info('Bye!')
        sys.exit(0)
