from gpiozero import Button
from hardware import ADCReader, LCDDisplay
import joystickvalues
import update
import shutdown
import time
import os

# Setup
btn = Button(18, pull_up=True)
adc = ADCReader()
lcd = LCDDisplay()

# Menu options
OPTIONS = [ # Label 10 char max
    {
        "label": "Joystick",
        "handler": lambda: joystickvalues.run(lcd, adc, btn)
    },
    {
        "label": "Update",
        "handler": lambda: update.run(lcd, adc, btn)
    },
    {
        "label": "Shutdown",
        "handler": lambda: shutdown.run(lcd, adc, btn)
    }
]

# Splash screen
def show_splash():
    lcd.cmd(0x01)
    lcd.message(0, 0, "-- WELCOME")
    lcd.message(8, 1, "BOZ --")
    time.sleep(0.05)
show_splash()

# Menu logic
def get_options_list():
    return [f"{i+1}. {opt['label']}" for i, opt in enumerate(OPTIONS)]

def handle_selection(selection):
    OPTIONS[selection]["handler"]()

options = get_options_list()
selected = 0

try:
    while True:
        y_nav = adc.read(0)

        lcd.message(0, 0, "-- MAIN MENU --")
        lcd.message(0, 1, "> " + options[selected])

        # Up and down
        if y_nav < 50: # Up
            selected = (selected - 1) % len(options)
            lcd.cmd(0x01)
            time.sleep(0.2)
        elif y_nav > 200: # Down
            selected = (selected + 1) % len(options)
            lcd.cmd(0x01)
            time.sleep(0.2)

        # Click to select
        if btn.is_pressed:
            time.sleep(0.3) # stop it pressing multiple times
            handle_selection(selected)
            lcd.cmd(0x01)

        time.sleep(0.05)

except KeyboardInterrupt:
    lcd.cmd(0x01)