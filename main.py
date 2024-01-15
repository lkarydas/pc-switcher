"""Main daemon for pc-switcher that runs on Raspberry Pi.

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

COMPUTER_CONFIGS = pi_header_pinout.COMPUTER_CONFIGS


class ComputerSwitcher:
    """Controls what happens when panel buttons are pressed."""

    def __init__(self):
        self.usb_hub_controller = usb_hub.USBHubController()
        self.panel_button_leds_controller = PanelButtonLEDsController()
        self._initilize_leds()

    def _initilize_leds(self):
        current_usb_position = self.usb_hub_controller.get_current_position()
        current_index = 0
        for i, config in enumerate(COMPUTER_CONFIGS):
            if config.usb_position == current_usb_position:
                current_index = i
                break
        logging.info('Current USB position: %i', current_usb_position)
        logging.info('Corresponding index: %i', current_index)
        # Flash all LEDs for show.
        self.panel_button_leds_controller.turn_on_all_leds()
        time.sleep(0.3)
        led_indices_to_turn_off = [0, 1, 2, 3]
        led_indices_to_turn_off.remove(current_index)
        logging.info('led_indices_to_turn_off: %s', led_indices_to_turn_off)
        for i in led_indices_to_turn_off:
            self.panel_button_leds_controller.turn_off_led(i)

    def button_callback(self, button):
        """Callback fn for panel button press."""
        index = pi_header_pinout.BUTTON_GPIO_PINS.index(button.pin.number)
        computer_config = pi_header_pinout.COMPUTER_CONFIGS[index]
        print('')
        logging.info(
            'Button pressed! Button: %s Switching to %s.',
            index,
            computer_config.computer_name)
        self.panel_button_leds_controller.turn_off_all_leds()
        self.panel_button_leds_controller.turn_on_led(index)
        logging.info(
            f'Switching USB hub to position {computer_config.usb_position}.')
        self.usb_hub_controller.switch_to(computer_config.usb_position)
        hdmi_position = computer_config.hdmi_position
        logging.info('hdmi_position: %i', hdmi_position)
        hdmi_hub.switch_to(2)  # So that C730 can send the DDC command.
        time.sleep(2)  # To give time for the HDMI swicth.
        if computer_config.computer_name == 'MSI':
            logging.info('Sending UDP command to switch monitor input to DP2.')
            tcp_client.send_message('DP2')
        else:
            logging.info(
                'Sending UDP command to switch monitor input to HDMI.')
            tcp_client.send_message('HDMI')
        hdmi_hub.switch_to(hdmi_position)

    def register_button_callbacks(self):
        """Register callbacks for panel buttons."""
        button_1 = gpiozero.Button(pi_header_pinout.BUTTON_GPIO_PINS[0])
        button_2 = gpiozero.Button(pi_header_pinout.BUTTON_GPIO_PINS[1])
        button_3 = gpiozero.Button(pi_header_pinout.BUTTON_GPIO_PINS[2])
        button_4 = gpiozero.Button(pi_header_pinout.BUTTON_GPIO_PINS[3])
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
    switcher = ComputerSwitcher()
    switcher.register_button_callbacks()
    # Signal pause only works on Linux.
    signal.pause()  # pylint: disable=no-member


if __name__ == '__main__':
    try:
        app.run(main)
    except KeyboardInterrupt:
        print('')
        logging.info('Bye!')
        sys.exit(0)
