"""Main daemon for ComputerSelector that runs on Raspberry Pi.

- Controls what happens when panel buttons are pressed.
- Sets USB hub to corresponding position.
- Sends TCP messages to Legion to switch monitor inputs.
- Sends IR commands to HDMI switch.
- Controls LED lights on panel buttons.
"""

import sys
import signal
import time

import gpiozero

from absl import app
from absl import flags
from absl import logging

import hdmi_hub
from panel_button_leds import PanelButtonLEDsController
import tcp_client
import usb_hub
import pi_header_pinout

FLAGS = flags.FLAGS

BUTTON_TO_COMPUTER_MAP = pi_header_pinout.BUTTON_GPIO_PIN_TO_COMPUTER_CONFIG_MAP

class ComputerSelector:
    """Controls what happens when panel buttons are pressed."""

    def __init__(self):
        self.usb_hub_controller = usb_hub.USBHubController()
        self.panel_button_leds_controller = PanelButtonLEDsController()

    def button_callback(self, button):
        """Callback fn for panel button press."""
        button_pin = button.pin.number
        panel_button = BUTTON_TO_COMPUTER_MAP[button_pin]
        print('')
        logging.info(
            'Button pressed! Pin: %s Switching to %s.',
            button_pin,
            panel_button.computer_name)
        self.panel_button_leds_controller.turn_off_all_leds()
        self.panel_button_leds_controller.turn_on_led(button.pin.number)
        logging.info(
            f'Switching USB hub to position {panel_button.usb_position}.')
        self.usb_hub_controller.switch_to(panel_button.usb_position)
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

    def register_button_callbacks(self):
        """Register callbacks for panel buttons."""
        button_1 = gpiozero.Button(pi_header_pinout.BUTTON_1_GPIO_PIN)
        button_2 = gpiozero.Button(pi_header_pinout.BUTTON_2_GPIO_PIN)
        button_3 = gpiozero.Button(pi_header_pinout.BUTTON_3_GPIO_PIN)
        button_4 = gpiozero.Button(pi_header_pinout.BUTTON_4_GPIO_PIN)
        button_1.when_pressed = self.button_callback
        button_2.when_pressed = self.button_callback
        button_3.when_pressed = self.button_callback
        button_4.when_pressed = self.button_callback


def main(argv):
    """Main function."""
    del argv  # Unused.
    logging.set_verbosity(logging.INFO)
    logging.get_absl_handler().use_absl_log_file()
    logging.info('Main loop.')
    controller = ComputerSelector()
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
