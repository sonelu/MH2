from luma.core.render import canvas
from PIL import ImageFont
import numpy as np

class BaseScreen(object):

    def __init__(self, display, robot, title, navigation):
        self.display = display
        self.robot = robot
        self.title = title
        self.navigation = navigation
        self.size = self.display.size
        self.mode = self.display.mode
        self.avail = None
        self.font = ImageFont.truetype('//usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
        self.bfont = ImageFont.truetype('//usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf')
        self.font9 = ImageFont.truetype('//usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', size=9)

    def show(self):
        with canvas(self.display) as draw:
            self.render(draw)

    def render(self, draw):
        # does the actual drawing
        # the Base prints the title
        # and adjusts the drawable area
        # subclasses shoudl invoke the super class
        # and then do their own drawing
        size = draw.textsize(self.title, font=self.bfont)
        #posx = (self.size[0] - size[0]) // 2
        draw.text((2, 0), self.title, fill="white", font=self.bfont)
        draw.line((0, size[1]+1, self.size[0], size[1]+1), fill="white")
        draw.line((0, size[1]+3, self.size[0], size[1]+3), fill="white")
        # battery
        # volts = np.mean([m.present_voltage for m in self.robot.motors])
        # max_v = 8.0            # max voltage to represent (100%)
        # min_v = 6.0           # min voltage to represent (0%)
        # volts = min(volts, max_v)     # in case there is above max_v
        # perc = (volts - min_v)/(max_v - min_v)
        # battery placement
        b_x = 110 # x pos
        b_y = 1    # y pos
        b_h = 7   # height
        b_l = 15  # lenght
        draw.rectangle((b_x, b_y, b_x+b_l, b_y+b_h), outline="white", fill="black")
        draw.rectangle((b_x+b_l, b_y+2, b_x+b_l+1, b_y+b_h-2), outline="white", fill="white")
        bar = int(self.robot.voltage.perc * (b_l-2))
        if bar > 1:
            draw.rectangle((b_x+1, b_y+1, b_x+bar+1, b_y+b_h-1), outline="black", fill="white")
        else:
            c_x = b_x + b_l // 2 + 1
            c_y = b_y + b_h // 2
            draw.line((c_x-2, c_y-2, c_x+2, c_y+2), fill="white")
            draw.line((c_x+2, c_y-2, c_x-2, c_y+2), fill="white")
        self.avail = ((0,size[1]+4), self.size)
        
