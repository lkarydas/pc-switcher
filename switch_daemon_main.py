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
from panel_button_leds import PanelButtonLEDsController
import tcp_client
import usb_hub
import pi_header_pinout

FLAGS = flags.FLAGS


@dataclasses.dataclass
class PanelButton:
    """Data class that represents a panel button."""
    pin: int
    usb_position: int
    computer_name: str
    button_color: str
    hdmi_position: int


_PANEL_BUTTON_MAP = {
    13: PanelButton(13, 1, 'Dock', 'white', 1),
    5: PanelButton(5, 2, 'Lenovo', 'red', 2),
    6: PanelButton(6, 3, 'MSI', 'blue', 2),
    19: PanelButton(19, 4, 'UM350', 'RGB', 4),
}

class PanelController:
    """Controls what happens when panel buttons are pressed."""

    def __init__(self):
        self.usb_hub_controller = usb_hub.USBHubController()
        self.panel_button_leds_controller = PanelButtonLEDsController()

    def button_callback(self, button):
        """Callback fn for panel button press."""
        panel_button = _PANEL_BUTTON_MAP[button.pin.number]
        print('')
        logging.info(
            'Button pressed! Pin: %s Switching to %s.',
            panel_button.pin,
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
