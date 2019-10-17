from luma.core.interface.serial import i2c
from luma.oled.device import ssd1327

class Display():
    """
    A convenience wrapper for the display used by the robot
    """
    def __init__(self, robot):
        self.robot = robot
        self.serial = i2c(port=0, address=0x3c)
        self.display = ssd1327(self.serial, rotate=2, mode="1")


    def clear(self):
        self.display.clear()

    def contrast(self, level):
        self.display.contrast(level)

    def size(self):
        return self.display.size

    def mode(self):
        return self.display.mode

