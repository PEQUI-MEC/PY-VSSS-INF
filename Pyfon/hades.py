import cv2
# from digi.xbee.devices import


class Hades:
    """
    Manager of all modules.
    """

    def __init__(self, srcCam, srcBee):
        self.srcCamera = srcCam
        self.srcXbee = srcBee
        self.cap = self.summonCapture()
        # self.comm = self.summonCommunication()

    def summonCapture(self):
        """Set link between camera and software"""
        try:
            cap = cv2.VideoCapture(self.srcCamera)
        except cv2.error:
            return None
        else:
            return cap

    def killCapture(self):
        """Unlink camera and software"""
        try:
            self.cap.release()
            cv2.destroyAllWindows()
        except cv2.error:
            print("Sorry =( I cannot stop your capture connection.\n")
            return self.cap
        else:
            return None

    def refreshCapture(self):
        """Cleanup capture flags and set again"""
        self.killCapture()
        self.summonCapture()
        return True

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
