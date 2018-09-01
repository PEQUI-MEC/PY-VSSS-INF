# import numpy as np
import cv2
# from Pyfon.interface.afrodite import Afrodite
# from Pyfon.communication.hermes import Hermes

from observer import Subscriber, Publisher

class Hades:

    channels = ['vision', 'control', 'communication']
    srcCamera = None

    hadesPub = None
    hadesSub = None
    hermesPub = None
    hermesSub = None


    # def __init__(self, srcCam=None):
    #     self.srcCamera = srcCam
    #     # self.srcXbee = srcBee
    #     self.pub = Publisher(Hades.states)
    #     self.xbeeSub = Subscriber('xbee')

    def setup(self):
        hades = Hades()
        hades.srcCamera = '/dev/ttyUSB0'

        hades.hadesPub = Publisher(hades.channels)

        # registering Hermes
        hades.hermesSub = Subscriber('hermes')
        hades.hadesPub.register("communication", hades.hermesSub)

    # Set link between camera and software
    # def summonCapture(self):
    #     try:
    #         cap = cv2.VideoCapture(self.srcCamera)
    #     except cv2.error:
    #         return None
    #     else:
    #         return cap
    #
    # # Unlink camera and software
    # def killCapture(self):
    #     try:
    #         self.cap.release()
    #         cv2.destroyAllWindows()
    #     except cv2.error:
    #         print("Sorry =( I cannot stop your capture connection.\n")
    #         return self.cap
    #     else:
    #         return None
    #
    # # Cleanup capture flags and set again
    # def refreshCapture(self):
    #     self.killCapture()
    #     self.summonCapture()
    #     return True

    def summonCommunication(self):
        return True

    def puppetLoop(self):
        return True

    def updatePositions(self):
        return True

    def updateFormation(self):
        return True

    def createFormation(self):
        return True

    def recordGame(self):
        return True


if __name__ == "__main__":
    h = Hades()
    h.setup()

    h.hadesPub.