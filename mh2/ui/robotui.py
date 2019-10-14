import smbus2

from screenloop import UIScreenLoop

import time
import subprocess


class RobotUI():                                         

    def __init__(self, robot):
        self.robot = robot
        self.bus = smbus2.SMBus(0)
        self.bus.write_byte_data(0x70, 0x03, 0xff)
        self.lastbutt = 255          

    def processKeys(self):
        butt = self.bus.read_byte_data(0x70, 0x00)
        if butt != self.lastbutt:
            display = self.robot.screen_loop
            navigation = display.navigation()
            if butt == 247 and 'I' in navigation:
                # info button
                display.switchScreen(navigation['I'])
            elif butt == 253 and 'M' in navigation:
                # menu button 
                display.switchScreen(navigation['M'])
            elif butt == 127 and 'U' in navigation and navigation['U'] == True:
                # button up
                display.navUp()
            elif butt == 239 and 'D' in navigation and navigation['D'] == True:
                # button down
                display.navDown()
            elif butt == 191 and 'B' in navigation:
                # back button
                display.switchScreen(navigation['B'])
            elif butt == 223 and 'F' in navigation:
                # forward button
                sel = display.screen.cursel
                if navigation['F'][sel] == "__action__":
                    getattr(self, display.screen.actions[sel])()
                else:
                    display.switchScreen(navigation['F'][sel])
            elif butt == 254:
                if 'S' in navigation:
                    display.switchScreen(navigation['S']) 
                else:
                    display.switchScreen('shutDown') 

            self.lastbutt = butt

    def stopRobot(self):
        display = self.robot.screen_loop
        display.switchScreen('info')
        display.screen.title = "Stopping Robot"
        self.commonStop()

    def powerDown(self):
        subprocess.check_output('sudo shutdown -h', shell=True)
        display = self.robot.screen_loop
        display.switchScreen('info')
        display.screen.title = "Power Down"
        display.screen.updateText("Shutdown Requested.\nWill power off\nin 1min")
        time.sleep(2)
        self.commonStop()

    def resetSoC(self):
        subprocess.check_output('sudo shutdown -r', shell=True)
        display = self.robot.screen_loop
        display.switchScreen('info')
        display.screen.title = "Reboot"
        display.screen.updateText("Reboot Requested.\nWill reboot\nin 1min")
        time.sleep(2)
        self.commonStop()

    def commonStop(self):
        screen = self.robot.screen_loop.screen
        for count in range(5,0, -1):
            screen.updateText("Robot will\nbecome compliant\nin {}s".format(count))
            time.sleep(1)
        screen.updateText("Making\ncompliant...")
        self.robot.compliant = True
        screen.updateText("Closing down\nrobot...")
        self.robot.close()
        screen.updateText("Finished.\nBye")
        #sys.exit() # we need to close this thread too

    def toggleMove(self, title, text, primitive, sleep):
        display = self.robot.screen_loop
        old_screen = display.switchScreen('info')
        display.screen.title = title
        display.screen.text = text
        if primitive.is_alive():
            primitive.stop()
        else:
            primitive.start()
        time.sleep(sleep)
        display.switchScreen(old_screen)

    def startStandUp(self):
        self.toggleMove("Stand Up", "Running\nStand Up\nMove", self.robot.stand_position, 2)

    def startSitDown(self):
        self.toggleMove("Sit Down", "Running\nSit Down\nMove", self.robot.sit_position, 2)

    def startHeadIdle(self):
        self.toggleMove("Head Idle", "Toggling\nHead Idle\nMove", self.robot.head_idle_motion, 2)

    def startWaveLeft(self):
        self.toggleMove("Wave Left", "Running\nWave Left\nMove", self.robot.wave_left, 2)
        
    def startWaveBoth(self):
        self.toggleMove("Wave Both", "Running\nWave Both\nMove", self.robot.wave_both, 2)

    def turnCompliantOn(self): 
        self.robot.compliant = True
        self.robot.screen_loop.splashScreen('Compliant On', 'Turned\nCompliant\nON', 2)

    def turnCompliantOff(self): 
        self.robot.power_up()
        self.robot.screen_loop.splashScreen('Compliant Off', 'Turned\nCompliant\nOFF', 2)

    def turnHandsCompliant(self):
        self.robot.turnHandsCompliant()
        self.robot.screen_loop.splashScreen('Hands', 'Turned\nHands\nCompliant', 2)

    def turnLegsCompliant(self):
        self.robot.turnLegsCompliant()
        self.robot.screen_loop.splashScreen('Legs', 'Turned\nLegs\nCompliant', 2)

    def turnHeadCompliant(self):
        self.robot.turnHeadCompliant()
        self.robot.screen_loop.splashScreen('Legs', 'Turned\nHead\nCompliant', 2)


    def governorPerformance(self): self.robot.changeGovernor('performance')
    def governorOnDemand(self): self.robot.changeGovernor('ondemand')
    def governorPowerSave(self): self.robot.changeGovernor('powersave')
    def governorConservative(self): self.robot.changeGovernor('conservative')