import pypot.primitive
import pypot.utils

from dynamicscreen import StatusScreen, TemperatureScreen, PositionScreen
from menuscreen import MenuScreen
from infoscreen import InfoScreen, InfoScreenButton

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1327

import json
import time
import numpy as np


class UIScreenLoop(pypot.utils.StoppableLoopThread):

    _history_file = '/home/pi/mh2/etc/battery.dat'
     
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
        # battery voltage reading
        # self.robot.volt = 0                 # current battery
        # self.robot.volt_per = 0             # current battery percentage
        # self.volt_samples = 0               # we will do a running average
        # self.SAMPLES_LIMIT = 10             # number of samples for the average
        # # voltage history
        try:
            with open(self._history_file,'r') as f:
                # time on battery, last voltage
                tobstr, hvoltstr = f.readline().split(",")
                self.robot.tob = float(tobstr)
                self.last_volt = float(hvoltstr)
        except IOError:
            # file does not exist
            self.robot.tob = 0
            self.last_volt = 0
        self.last_read = time.time()
        # we will update the history in etc/battery.dat not at every update() cycle
        self.history_update = 0

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
        # read current voltage
        self.robot.voltage.read()
        # tob update
        now = time.time()
        self.robot.tob += (now - self.last_read)
        self.last_read = now
        if self.robot.voltage()-self.last_volt > 0.10:
            # an sudden increase of more than 0.1V for the average
            # this means at least a 1V change in the voltage
            # we assume the batteries changed
            # reset the TOB and history start
            self.robot.tob = 0
        self.last_volt = self.robot.voltage()

        # update history every 60 clycles ~ 30s
        self.history_update = (self.history_update + 1) % 60
        if self.history_update == 0:
            with open(self._history_file, 'w') as f:
                f.write("{},{}\n".format(self.robot.tob, self.robot.voltage()))
        self.screen.show()