import psutil
import time
import subprocess
from datetime import timedelta

def get_cpu_usage():
    cpu = psutil.cpu_percent(interval=0.1)
    return f"{cpu:.1f}%"

def get_ram_usage():
    ram = psutil.virtual_memory().percent
    return f"{ram:.1f}%"

def get_disk_usage():
    disk = psutil.disk_usage('/').percent
    return f"{disk:.1f}%"

def get_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read()) / 1000.0
        return f"{temp:.1f}C"
    except:
        return "N/A"

def get_fan_status():
    try:
        with open('/sys/class/hwmon/hwmon0/pwm1', 'r') as f:
            pwm = int(f.read())
        fan = (pwm / 255.0) * 100
        return f"{fan:.1f}%"
    except:
        return "N/A"

def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    return f"{hours:02d}H {minutes:02d}M {seconds:02d}S"

def run(lcd, adc, btn):
    stats = [
        ("CPU", get_cpu_usage),
        ("RAM", get_ram_usage),
        ("DISK", get_disk_usage),
        ("TEMP", get_temperature),
        ("FAN", get_fan_status),
        ("UPTIME", get_uptime),
    ]

    current_stat = 0

    try:
        while True:
            label, getter = stats[current_stat]
            display_value = getter()
            lcd.cmd(0x01)
            lcd.message(0, 0, label)
            lcd.message(0, 1, display_value)
            y_nav = adc.read(0)
            if y_nav < 50:  # Up
                current_stat = (current_stat + 1) % len(stats)
                lcd.cmd(0x01)
                time.sleep(0.2)
            elif y_nav > 200:  # Down
                current_stat = (current_stat - 1) % len(stats)
                lcd.cmd(0x01)
                time.sleep(0.2)
            # Click to exit
            if btn.is_pressed:
                time.sleep(0.3)
                return
            time.sleep(0.5)
    except KeyboardInterrupt:
        lcd.cmd(0x01)
