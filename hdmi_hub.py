""" Controls the HDMI switch using ir-ctl.

Assumes that lirc is already set up.
"""

import subprocess

from absl import logging

IR_COMMAND_MAP = {
    1: 'nec:0x8001',
    2: 'nec:0x8004',
    3: 'nec:0x8002',
    4: 'nec:0x800d',
}


def switch_to(hdmi_position):
    """Send IR command to HDMI switch to change input."""
    ir_command = IR_COMMAND_MAP[hdmi_position]
    logging.info('Switching HDMI hub to position %s.', hdmi_position)
    command = ['ir-ctl', '-S', ir_command]
    logging.info('Running command: %s', ' '.join(command))
    subprocess.run(command, check=False)
