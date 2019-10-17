import cv2


class Camera():

    def __init__(self, device=0):
        self.cam = cv2.VideoCapture(device)

    def get_resolution(self):
        return self.cam.get(3), self.cam.get(4)

    def get_frame(self):
        ret, frame = self.cam.read()
        return frame
