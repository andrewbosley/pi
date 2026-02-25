import time
import os

def run(lcd, adc, btn):
    lcd.cmd(0x01)
    lcd.message(0, 0, "Shutdown?")
    lcd.message(0, 1, "Click to confirm")

    while True:
        x_val = adc.read(1)
        y_val = adc.read(0)

        if btn.is_pressed:
            time.sleep(0.3)
            lcd.cmd(0x01)
            lcd.message(0, 0, "Powering Off...")
            time.sleep(2)
            os.system("sudo shutdown now")
            break

        elif x_val < 50 or x_val > 200 or y_val < 50 or y_val > 200:
            lcd.cmd(0x01)
            lcd.message(0, 0, "Cancelled")
            time.sleep(1)
            break

        time.sleep(0.05)
