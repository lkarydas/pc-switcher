""" Sends DDC commands to Samsung G9 using ddcutil."""

import subprocess
import time

from absl import logging

DDCUTIL_BIN = r'C:\Program Files (x86)\winddcutil\winddcutil.exe'
GET_VCP_INPUT_CODES = {
    '1': 'HDMI',
    '4': 'DP2',
}
SET_VCP_INPUT_CODES = {
    'HDMI': '1',
    'DP2': '10',
}
MAX_RETRIES = 3
TIME_BETWEEN_RETRIES_SECONDS = 1


def switch_monitor_input(tcp_message):
    """Switch monitor input."""
    if tcp_message in SET_VCP_INPUT_CODES:
        retry_counter = 0
        while True:
            retry_counter += 1
            return_code = ddcutil_set_input(SET_VCP_INPUT_CODES[tcp_message])
            if return_code == 1:
                logging.info('Success.')
                break
            logging.info('Error.')
            if retry_counter <= MAX_RETRIES:
                time.sleep(TIME_BETWEEN_RETRIES_SECONDS)
                logging.info('Retrying. Attempt %i of %i',
                             retry_counter, MAX_RETRIES)
            else:
                logging.info('Max retries reached.')
                break
    else:
        logging.info('Received unknown message: %s', tcp_message)


def ddcutil_get_input():
    """Send DDC command to set monitor input."""
    result = subprocess.run([DDCUTIL_BIN, 'getvcp', '0', '60'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=False,
                            text=True)
    output = result.stdout.strip()
    return GET_VCP_INPUT_CODES.get(output.lstrip('VCP 60 '), None)


def ddcutil_set_input(vcp_code):
    """Send DDC command to get monitor input."""
    result = subprocess.run([DDCUTIL_BIN, 'setvcp', '0', '60', vcp_code],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=False,
                            text=True)
    return result.returncode
