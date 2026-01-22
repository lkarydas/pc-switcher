from monitorcontrol import get_monitors, InputSource
import time

from absl import logging

# TODO: Fix this documentation.
# When you read the monitor input.
# InputSource.ANALOG1 is HDMI
# DP2:  InputSource.DVI2  

# When you set the monitor input.
SET_MONITOR_INPUT_MAP = {
    'HDMI': 'HDMI1',
    'DP2': 'DP2',
}

def _get_monitor():
    monitors = get_monitors()
    if len(monitors) == 0:
        raise ValueError('No monitor found.')
    elif len(monitors) > 1:
        raise ValueError('More than one monitor found.')
    return monitors[0]

def set_monitor_input_source(input_source: str):
    if input_source not in SET_MONITOR_INPUT_MAP:
        logging.error('set_monitor_input_source with invalid input_source value: %s', input_source)
    monitor = _get_monitor()
    logging.info(f'Setting monitor input source to {input_source}.')
    retry_counter = 0
    success = False
    while not success and retry_counter < 5:
        try:
            with monitor:
                monitor.set_input_source(SET_MONITOR_INPUT_MAP[input_source])
                success = True
                return
        except Exception as e:
            logging.error('Error: ' + str(e))
        retry_counter += 1
        time.sleep(0.8)
    logging.error('Total failure.')


