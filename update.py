import subprocess
import time
import os

def run(lcd, adc, btn):
    lcd.cmd(0x01)
    lcd.message(0, 0, "Confirm Update?")
    lcd.message(0, 1, "Click=Y Other=N")

    while True:
        x_val = adc.read(1)
        y_val = adc.read(0)

        if btn.is_pressed:
            lcd.cmd(0x01)
            lcd.message(0, 0, "Updating...")
            subprocess.check_output(["git", "pull"])
            lcd.cmd(0x01)
            lcd.message(0, 0, "Success!")
            lcd.message(0, 1, "Reloading...")
            time.sleep(2)
            os.system("sudo systemctl restart mainmenu.service")

        elif x_val < 50 or x_val > 200 or y_val < 50 or y_val > 200:
            lcd.cmd(0x01)
            lcd.message(0, 0, "Cancelled")
            time.sleep(1)
            break

        time.sleep(0.1)