# Desk Panel

![Photos of the front panel siting on the desk.](doc/images/panel_banner.png)

## Install as a service

```
sudo ln -s /home/lkary/src/usb-switch/usb-switch.service /lib/systemd/system/usb-switch.service
```

Enable the service:

```
sudo systemctl enable usb-switch.service
```

Similarly, to start, stop, or disable it:

```
sudo systemctl start usb-switch.service
sudo systemctl stop usb-switch.service
sudo systemctl disable usb-switch.service
```

## Debugging

### USB Hub

Run the manual test:

```
sudo systemctl stop usb-switch.service

cd ~/src/usb-switch/
python usb_hub_test.py
```

This will cycle through the 4 positions and return to the initial position.

### Panel Button LEDs

Run the manual test:

```
sudo systemctl stop usb-switch.service

cd ~/src/usb-switch/
python panel_button_leds_test.py
```