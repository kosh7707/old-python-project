from PIL import Image, ImageGrab
import cv2
import numpy as np
import logging

class CaptureTool:
    def __init__(self):
        self._imagePos = (1300, 298)
        self._partyOneImagePos = [(1285, 376, 1515, 403), (1285, 406, 1515, 433),
                                  (1285, 436, 1515, 463), (1285, 466, 1515, 493)]
        self._partyTwoImagePos = [(1585, 376, 1815, 403), (1585, 406, 1815, 433),
                                  (1585, 436, 1815, 463), (1585, 466, 1815, 493)]
        self._partyOneOrignalImageFilePath = ["image/1_1_orig.png", "image/1_2_orig.png",
                                              "image/1_3_orig.png", "image/1_4_orig.png"]
        self._partyOneThreshImageFilePath  = ["image/1_1_thr.png", "image/1_2_thr.png",
                                              "image/1_3_thr.png", "image/1_4_thr.png"]
        self._partyTwoOrignalImageFilePath = ["image/2_1_orig.png", "image/2_2_orig.png",
                                              "image/2_3_orig.png", "image/2_4_orig.png"]
        self._partyTwoThreshImageFilePath  = ["image/2_1_thr.png", "image/2_2_thr.png",
                                              "image/2_3_thr.png", "image/2_4_thr.png"]

    def preprocessingImage(self, image: np.array) -> np.array:
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, thr = cv2.threshold(gray_image, 20, 255, cv2.THRESH_TOZERO)
        thr = 255 - thr
        return thr

    def updateImagePos(self):
        logging.debug("updateImagePos()")
        raw_image = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        raw_image = np.array(raw_image)
        template_image = cv2.imread("image/template2.png", 0)
        gray_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray_image, template_image, cv2.TM_CCOEFF_NORMED)
        _, maxval, _, maxloc = cv2.minMaxLoc(res)
        self._imagePos = maxloc
        logging.debug(f"self._imagePos: {self._imagePos}")
        self._partyOneImagePos = [(self._imagePos[0]-15, self._imagePos[1]+78, self._imagePos[0]+215, self._imagePos[1]+105),
                                  (self._imagePos[0]-15, self._imagePos[1]+108, self._imagePos[0]+215, self._imagePos[1]+135),
                                  (self._imagePos[0]-15, self._imagePos[1]+138, self._imagePos[0]+215, self._imagePos[1]+165),
                                  (self._imagePos[0]-15, self._imagePos[1]+168, self._imagePos[0]+215, self._imagePos[1]+195)]
        self._partyTwoImagePos = [(self._imagePos[0]+285, self._imagePos[1]+78, self._imagePos[0]+515, self._imagePos[1]+105),
                                  (self._imagePos[0]+285, self._imagePos[1]+108, self._imagePos[0]+515, self._imagePos[1]+135),
                                  (self._imagePos[0]+285, self._imagePos[1]+138, self._imagePos[0]+515, self._imagePos[1]+165),
                                  (self._imagePos[0]+285, self._imagePos[1]+168, self._imagePos[0]+515, self._imagePos[1]+195)]

    def capturePartyOne(self) -> None:
        logging.info("capturePartyOne start")
        self.updateImagePos()
        for i in range(0, 4):
            raw_image = ImageGrab.grab(bbox=self._partyOneImagePos[i])
            raw_image.save(self._partyOneOrignalImageFilePath[i])
            np_image = np.array(raw_image)
            thr = self.preprocessingImage(np_image)
            cv2.imwrite(self._partyOneThreshImageFilePath[i], thr)
        logging.info("capturePartyOne end")

    def capturePartyTwo(self) -> None:
        logging.info("capturePartyTwo start")
        self.updateImagePos()
        for i in range(0, 4):
            raw_image = ImageGrab.grab(bbox=self._partyTwoImagePos[i])
            raw_image.save(self._partyTwoOrignalImageFilePath[i])
            np_image = np.array(raw_image)
            thr = self.preprocessingImage(np_image)
            cv2.imwrite(self._partyTwoThreshImageFilePath[i], thr)
        logging.info("capturePartyTwo end")

    def getPartyOneOriginalImageFilePath(self) -> list:
        return self._partyOneOrignalImageFilePath

    def getPartyOneThreshImageFilePath(self) -> list:
        return self._partyOneThreshImageFilePath

    def getPartyTwoOriginalImageFilePath(self) -> list:
        return self._partyTwoOrignalImageFilePath

    def getPartyTwoThreshImageFilePath(self) -> list:
        return self._partyTwoThreshImageFilePath

