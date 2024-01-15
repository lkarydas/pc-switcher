

# Visual drawing of pinout:
# https://docs.google.com/drawings/d/1v56Ztgi_ypiBD4tRo_7iUOf9xP8JAnZEOGvu_qgjYyM



# Pins connected to panel buttons and their LEDs.
# The numbers 1, 2, 3, 4 go from left to right (as you see the panel).
BUTTON_1_GPIO_PIN = 19 # UM350.
BUTTON_1_LED_GPIO_PIN = 12

BUTTON_2_GPIO_PIN = 6  # MSI.
BUTTON_2_LED_GPIO_PIN = 16

BUTTON_3_GPIO_PIN = 13 # Dock.
BUTTON_3_LED_GPIO_PIN = 21

BUTTON_4_GPIO_PIN = 5  # Lenovo.
BUTTON_4_LED_GPIO_PIN = 20

# Pins connected to the Startech USB switch.

USB_HUB_BUTTON_GPIO_PIN = 10
USB_HUB_POSITION_LEDS_GPIO_PINS = [4, 22, 15, 27]

# Infrared communication (in /boot/config.txt).
# dtoverlay=gpio-ir,gpio_pin=17
# dtoverlay=gpio-ir-tx,gpio_pin=18
