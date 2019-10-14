#!/usr/bin/python

#import pypot.robot
import time
import numpy
import subprocess
from functools import partial
from remote.zmqserver import ZMQRobotServerExt
from threading import Thread

from pypot.creatures import AbstractPoppyCreature

from ui import RobotUI, UIScreenLoop
from primitives.posture import StandPosition, SitPosition, HeadIdleMotion, Balance
from primitives.interaction import WaveLeft, WaveBoth

class MH2(AbstractPoppyCreature):


    def setupPrimitives(self):
        self.screen_loop = UIScreenLoop(self, '/home/pi/mh2/ui/screens.json')
        self.screen_loop.start()
        self.ui = RobotUI(self)
        self.attach_primitive(StandPosition(self), 'stand_position')
        self.attach_primitive(SitPosition(self), 'sit_position')    
        self.attach_primitive(HeadIdleMotion(self, 50), 'head_idle_motion')
        self.attach_primitive(WaveLeft(self), 'wave_left')
        self.attach_primitive(WaveBoth(self), 'wave_both')
        self.attach_primitive(Balance(self, 20), 'balance')
        self.balance.start()
        self.zmq = ZMQRobotServerExt(self, "*", 5555)
        s = Thread(target=self.zmq.run, name='zmq_server')
        s.daemon = True
        s.start()
        
    def turnHandsCompliant(self):
        for m in self.arms:
            m.compliant = True

    def turnLegsCompliant(self):
        for m in self.legs:
            m.compliant = True

    def turnHeadCompliant(self):
        for m in self.head:
            m.compliant = True

    def changeGovernor(self, newGovernor):
        cmd = 'sudo sh -c "echo {} > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor"'.format(newGovernor)
        res = subprocess.check_output(cmd, shell=True)
        if res != '':
            print(res)
        self.screen_loop.splashScreen('Governor', 'Changed\nGovernor to\n{}'.format(newGovernor), 2)


if __name__ == '__main__':

    mh2 = MH2(config='/home/pi/mh2/config/mh2-22.json')
    mh2.__class__ = MH2

    mh2.setupPrimitives()
    time.sleep(2)
    # check governor
    with open('/sys/devices/system/cpu/cpufreq/policy0/scaling_governor', 'r') as f:
        gov = f.readline()
    if gov != 'performance\n':
        mh2.changeGovernor('performance')

    while(mh2._syncing):
        mh2.ui.processKeys()
        time.sleep(0.02)

    time.sleep(2) # that the last messages are issued
    mh2.screen_loop.stop()

    print "Main thread finished."
    print "Bye"
