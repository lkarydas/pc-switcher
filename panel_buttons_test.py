
import sys
import signal

import gpiozero

from absl import app
from absl import logging

import pi_header_pinout


def button_callback(button):
    """Callback fn for panel button press."""
    print(f'Pressed button {button.pin.number}.')

def register_button_callbacks():
    """Register callbacks for panel buttons."""
    button_1 = gpiozero.Button(pi_header_pinout.BUTTON_GPIO_PINS[0])
    button_2 = gpiozero.Button(pi_header_pinout.BUTTON_GPIO_PINS[1])
    button_3 = gpiozero.Button(pi_header_pinout.BUTTON_GPIO_PINS[2])
    button_4 = gpiozero.Button(pi_header_pinout.BUTTON_GPIO_PINS[3])
    button_1.when_pressed = button_callback
    button_2.when_pressed = button_callback
    button_3.when_pressed = button_callback
    button_4.when_pressed = button_callback


def main(argv):
    """Main function."""
    del argv  # Unused.
    logging.set_verbosity(logging.INFO)
    logging.get_absl_handler().use_absl_log_file()
    logging.info('Press buttons!')
    register_button_callbacks()
    # Signal pause only works on Linux.
    signal.pause()  # pylint: disable=no-member


if __name__ == '__main__':
    try:
        app.run(main)
    except KeyboardInterrupt:
        print('')
        logging.info('Bye!')
        sys.exit(0)
