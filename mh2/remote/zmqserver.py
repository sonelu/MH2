from pypot.server import ZMQRobotServer
from rest import RESTRobotExt

class ZMQRobotServerExt(ZMQRobotServer):
    """ Uses the extended REST API
    """
    def __init__(self, robot, host, port):
        super(ZMQRobotServerExt, self).__init__(robot, host, port)
        self.restful_robot = RESTRobotExt(robot)
