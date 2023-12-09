import cv2
import pytesseract
import re
import logging

class OcrTool:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract\tesseract.exe'
        self._config = "-l kor+eng --oem 2 --psm 8"
        self._regex = r"[^가-힣a-zA-Z0-9]"
        self._template = "image/template.png"

    def ocr(self, filepath: str) -> str:
        logging.info(f"{filepath} ocr start")
        text = pytesseract.image_to_string(filepath, config=self._config)
        text = text.replace("\n\n", "\n").replace(" ", "")
        text = re.sub(self._regex, "", text)
        text = text.rstrip('0')
        logging.info(f"{filepath}'s text: {text}")
        return text

    def ImageSearch(self, filepath, threshold=0.6):
        template_image = cv2.imread(self._template, 0)
        gray_image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        res = cv2.matchTemplate(gray_image, template_image, cv2.TM_CCOEFF_NORMED)
        _, maxval, _, _ = cv2.minMaxLoc(res)
        logging.debug("--> maxval: {}".format(maxval))
        return maxval >= threshold



