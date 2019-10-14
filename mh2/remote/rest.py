from pypot.server.rest import RESTRobot


class RESTRobotExt(RESTRobot):
    """
    Adds some more methods to make easier the interaction
    """
    def get_pos_vel_load(self):
        return dict([(m.name, (m.present_position, m.present_speed, m.present_load)) for m in self.robot.motors])

    def get_methods(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]

    # compliance
    def turnHandsCompliant(self): self.robot.turnHandsCompliant()
    def turnLegsCompliant(self): self.robot.turnLegsCompliant()
    def turnHeadCompliant(self): self.robot.turnHeadCompliant()
    def turnCompliantOn(self): self.robot.compliant = True
    def turnCompliantOff(self): self.robot.power_up() 

    # power
    def stopRobot(self): self.robot.ui.stopRobot()
    def powerDown(self): self.robot.ui.powerDown()
    def resetSoC(self): self.robot.ui.resetSoC()


    def goto_position(self, positions, duration):
        for (motor_name, position) in positions.iteritems():
            m = getattr(self.robot, motor_name)
            m.goto_position(position, duration, wait=False)

    def get_position(self): return dict([(m.name, round(m.present_position,2)) for m in self.robot.motors])

    # balance
    def balanceOff(self): self.robot.balance.stop()
    def balanceOn(self): self.robot.balance.start()

    # display
    def dispStatus(self): self.robot.screen_loop.switchScreen('status')
    def dispPositions(self): self.robot.screen_loop.switchScreen('positions')
    def dispTemperatures(self): self.robot.screen_loop.switchScreen('temperatures')
