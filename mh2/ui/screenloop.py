import pypot.primitive
import pypot.utils

from dynamicscreen import StatusScreen, TemperatureScreen, PositionScreen
from menuscreen import MenuScreen
from infoscreen import InfoScreen, InfoScreenButton

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1327

import json
import time


class UIScreenLoop(pypot.utils.StoppableLoopThread):

    def __init__(self, robot, screen_config, freq=2.0):
        # we have higher frequency to allow better read of buttons
        pypot.utils.StoppableLoopThread.__init__(self, freq)
        self.robot = robot
        self.serial = i2c(port=0, address=0x3c)
        self.display = ssd1327(self.serial, rotate=2, mode="1")
        # load screens
        with open(screen_config) as f:
            self.screens = json.load(f)
        self.currscreen = 'status'
        self.screen = self.screen_from_config(self.screens[self.currscreen])        

    def screen_from_config(self, config):
        screenCls = globals()[config['class']]
        if 'actions' in config:
            return screenCls(display=self.display,
                             robot=self.robot,
                             title=config['title'],
                             navigation=config['navigation'],
                             options=config['options'],
                             actions=config['actions'])
        else:
            return screenCls(display=self.display,
                             robot=self.robot,
                             title=config['title'],
                             navigation=config['navigation'])            

    def switchScreen(self, new_screen):
        old_screen = self.currscreen
        self.currscreen = new_screen
        self.screen = self.screen_from_config(self.screens[self.currscreen])
        return old_screen

    def splashScreen(self, title, text, pause):
        old_screen = self.switchScreen('info')
        self.screen.title = title
        self.screen.text = text
        self.update()
        time.sleep(pause)
        self.switchScreen(old_screen)
        
    def navigation(self):
        return self.screen.navigation

    def navUp(self):
        self.screen.navUp()

    def navDown(self):
        self.screen.navDown()

    def update(self):
        self.screen.show()

