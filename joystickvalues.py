import time

def run(lcd, adc, btn):
    lcd.cmd(0x01)
    while True:
        x_val = adc.read(1)
        y_val = adc.read(0)
        lcd.message(0, 0, f"X: {x_val:<3}   Y: {y_val:<3}")
        lcd.message(0, 1, "Click to go back")

        if btn.is_pressed:
            break
        time.sleep(0.1)