from pypot.primitive import LoopPrimitive, Primitive


class WaveLeft(Primitive):

    def run(self):

        save_position = dict([(m.name, m.present_position) for m in self.robot.left_arm])

        # lift left arm
        self.robot.goto_position({'lsy': 150.0,
                                  'lsx': 14.0,
                                  'laz': -93.0,
                                  'ley': 28.0}, 1, wait=True)

        # wave 3 times
        for v in range(3):
            self.robot.goto_position({'lsx': -6.0,'ley': 46.0}, 0.75, wait=True)
            self.robot.goto_position({'lsx': 25.0,'ley': -2.0}, 0.75, wait=True)

        #return to normal position
        self.robot.goto_position(save_position, 1, wait=True)


class WaveBoth(Primitive):

    def run(self):

        save_position = dict([(m.name, m.present_position) for m in self.robot.arms])

        # lift left arm
        self.robot.goto_position({'lsy': 150.0,
                                  'lsx': 14.0,
                                  'laz': -93.0,
                                  'ley': 28.0,
                                  'rsy': 150.0,
                                  'rsx': 14.0,
                                  'raz': -93.0,
                                  'rey': 28.0}, 1, wait=True)

        # wave 3 times
        for v in range(3):
            self.robot.goto_position({'lsx': -6.0,
                                      'ley': 46.0,
                                      'rsx': -6.0,
                                      'rey': 46.0}, 0.75, wait=True)
            self.robot.goto_position({'lsx': 25.0,
                                      'ley': -2.0, 
                                      'rsx': 25.0,
                                      'rey': -2.0}, 0.75, wait=True)

        #return to normal position
        self.robot.goto_position(save_position, 1, wait=True)
