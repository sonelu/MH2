import pypot.primitive
from pypot.primitive.utils import Sinus
import prctl
from devices import LSM330

class StandPosition(pypot.primitive.Primitive):

    def run(self):

        self.robot.goto_position({  "hz": 0, "hy": 0,
                                    "rsx": 0, "rsy": 0, "raz": 0, "rey": 0,
                                    "lsx": 0, "lsy": 0, "laz": 0, "ley": 0,
                                    "rhz": 0, "rhx": 0, "rhy": 0, "rky": 0, "ray": 0, "rax":0,
                                    "lhz": 0, "lhx": 0, "lhy": 0, "lky": 0, "lay": 0, "lax":0},
                                 1.0,
                                 wait=True)
        self.robot.balance.resume()
        # Restore the motor speed



class SitPosition(pypot.primitive.Primitive):
    def run(self):
	    # Sit postion from Robotis pages
        self.robot.goto_position({  "hz": 0, "hy": 0,
                                    "rsx": -15, "rsy": 0, "raz": 0, "rey": 0,
                                    "lsx": -15, "lsy": 0, "laz": 0, "ley": 0,
                                    "rhz": 0, "rhx": 0, "rhy": 80, "rky": 110, "ray": 30, "rax":0,
                                    "lhz": 0, "lhx": 0, "lhy": 80, "lky": 110, "lay": 30, "lax":0},
                                 1.0,
                                 wait=True)
        self.robot.balance.pause()

class HeadIdleMotion(pypot.primitive.LoopPrimitive):
    def __init__(self, robot, freq):
        pypot.primitive.LoopPrimitive.__init__(self, robot, freq)

        sinus_args = [{'motor_list': [self.robot.hz, ], 'amp': 60, 'freq': 0.05},
                      {'motor_list': [self.robot.hz, ], 'amp': 60, 'freq': 0.1},
                      {'motor_list': [self.robot.hy, ], 'amp': 10, 'freq': 0.04},
                      {'motor_list': [self.robot.hy, ], 'amp': 5, 'freq': 0.09}]

        self.head_sinus = [Sinus(self.robot, 50, **s) for s in sinus_args]

    def start(self):
        self.save_position = dict([(m.name, m.present_position) for m in self.robot.head])

        pypot.primitive.LoopPrimitive.start(self)

        for m in self.robot.head:
            m.compliant = False

        [hs.start() for hs in self.head_sinus]

    def pause(self):
        [hs.pause() for hs in self.head_sinus]

    def resume(self):
        [hs.resume() for hs in self.head_sinus]

    def stop(self):
        [hs.stop() for hs in self.head_sinus]
        pypot.primitive.LoopPrimitive.stop(self, wait=True)
        # return to start position
        self.robot.goto_position(self.save_position, 0.75, wait=True)

    def update(self):
        pass

class Balance(pypot.primitive.LoopPrimitive):
    def __init__(self, robot, freq):
       super(Balance, self).__init__(robot, freq)
       self.accel = LSM330()
       self.ax_p = 0.001 # P factor for accelerometer X direction
       self.ax_i = 5e-6   # I factor for accelerometer X direction
       self.ax_E = 0
       self.ax_limits = [-25.0, 25.0]
       self.compliant = True

    def update(self):
        # new_compliant = all(m.compliant for m in self.robot.legs)
        # if new_compliant != self.compliant:
        #     self.compliant = new_compliant
        #     if self.compliant == False:
        #         # we started a new non-compliant session
        #         # reset I error
        #         self.ax_E = 0

        if not any([m.compliant for m in [self.robot.lhy, self.robot.rhy]]):
            a_x, _, _ = self.accel.get_acc()
            self.ax_E += a_x
            #print(a)
            adj = a_x*self.ax_p + self.ax_E*self.ax_i
            adj = max(adj, self.ax_limits[0])
            adj = min(adj, self.ax_limits[1])
            #print("adjustment: {:.1f}".format(adj))
            lhypos = self.robot.lhy.present_position
            rhypos = self.robot.rhy.present_position
            self.robot.goto_position({  "lhy": lhypos+adj, "rhy": rhypos+adj},
                                    self.period*2,
                                    wait=False)

    def pause(self):
        # reset cummulative error
        self.ax_E = 0