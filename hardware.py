import smbus
import time

class ADCReader: #Joystick
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x4b

    def read(self, chn):
        cmd = 0x84 | (((chn << 2 | chn >> 1) & 0x07) << 4)
        return self.bus.read_byte_data(self.address, cmd)

class LCDDisplay:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.addr = 0x27
        self.init_lcd()

    def cmd(self, comm):
        for nibble in [(comm & 0xF0), ((comm & 0x0F) << 4)]:
            self.bus.write_byte(self.addr, nibble | 0x0C)
            time.sleep(0.002)
            self.bus.write_byte(self.addr, nibble | 0x08)

    def init_lcd(self):
        for c in [0x33, 0x32, 0x28, 0x0C, 0x01]:
            self.cmd(c)
            time.sleep(0.005)

    def message(self, x, y, text):
        pos = 0x80 + 0x40 * y + x
        self.cmd(pos)
        for char in text:
            byte = ord(char)
            for nibble in [(byte & 0xF0), ((byte & 0x0F) << 4)]:
                self.bus.write_byte(self.addr, nibble | 0x0D)
                time.sleep(0.002)
                self.bus.write_byte(self.addr, nibble | 0x09)