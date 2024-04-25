"""Controls the USB hub."""
import time
import orei_ukm_404_usb_switch_lib


# The position on the OREI USB switch where the USB hub (under desk) plugs in.
# Note: The numbering of the devices on the OREI USB switch is 1, 2, 3, 4.
_DEVICE_BEING_USED = 1


class UKM404USBSwitch:
    """Controls the OREI UKM-404 4x4 USB 3.0 Matrix Switch over HTTP."""

    def __init__(self) -> None:
        assert _DEVICE_BEING_USED > 0 and _DEVICE_BEING_USED <= 4, (
            "Valid device numbers for the OREI UKM-404 switch "
            "are 1, 2, 3 and 4.")
        # TODO Disconnect the rest of the devices.

    def get_current_position(self):
        """Returns the current position of the USB switch."""
        status = orei_ukm_404_usb_switch_lib.get_status()
        return int(status[_DEVICE_BEING_USED - 1])
        

    def switch_to(self, position):
        """Switch USB switch to a specific position."""
        orei_ukm_404_usb_switch_lib.switch_usb_position(
            _DEVICE_BEING_USED, position)
