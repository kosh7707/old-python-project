import subprocess
import pytesseract
import os, sys
from time import sleep, time
import re
import cv2

class SmsAuth:
    def __init__(self):
        self._image_path = "image/screen.png"
        self._config = "-l kor+eng --oem 3 --psm 11"
        self._tesseract_path = r'.\Tesseract\tesseract.exe'
        self._last_number = "00000"
        self._has_phone_number = True
        self._phone_number = ["010", "6659", "0484"]
        pytesseract.pytesseract.tesseract_cmd = self._tesseract_path

    def subprocess_open(self, command, encoding='cp949', close_fds=False):
        popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                 close_fds=close_fds, cwd='./adb')
        (out, error) = popen.communicate()
        return out.decode(encoding), error.decode(encoding)

    def get_connected_device_list(self):
        out, err = self.subprocess_open("adb devices -l")
        lines = out.split("\r\n")
        device_list = []
        for line in lines:
            if "device product" not in line:
                continue
            if "offline" in line:
                continue
            name = line.split(" ", 2)[0].strip()
            desc = line.split("model:", 2)[1]
            model = desc.split(" ")[0]
            device = {'name': name, 'model': model}
            device_list.append(device)
        return device_list

    def get_wm_size(self, device_name=None):
        add_cmd = ''
        if device_name is not None:
            add_cmd = f"-s {device_name}"
        cmd = f"adb {add_cmd} shell wm size"
        out, err = self.subprocess_open(cmd)
        lines = out.split("\r\n")
        width = height = 0
        for line in lines:
            if "Override size" in line:
                line = line.split(":")[1].strip()
                strs = line.split("x")
                width = int(strs[0])
                height = int(strs[1])
        return width, height

    def capture_screen(self, device_name=None):
        add_cmd = ''
        if device_name is not None:
            add_cmd = f"-s {device_name}"
        cmd = f"adb {add_cmd} shell screencap -p /sdcard/Download/screen.png"
        self.subprocess_open(cmd)
        cmd = f"adb {add_cmd} pull /sdcard/Download/screen.png \"{self._image_path}\""
        self.subprocess_open(cmd)

    def image_search(self, template_filepath, original_filepath, thr=0.6):
        template_image = cv2.imread(template_filepath, 0)
        gray_image = cv2.imread(original_filepath, cv2.IMREAD_GRAYSCALE)
        res = cv2.matchTemplate(gray_image, template_image, cv2.TM_CCOEFF_NORMED)
        _, maxval, _, maxloc = cv2.minMaxLoc(res)
        success = maxval >= thr
        return success, maxloc

    def open_kakaotalk_first_message(self, device_name=None):
        add_cmd = ''
        if device_name is not None:
            add_cmd = f"-s {device_name}"
        cmd = f"adb {add_cmd} shell am start -n com.kakao.talk/.activity.SplashActivity"
        self.subprocess_open(cmd)
        while True:
            self.capture_screen()
            success, maxloc = self.image_search("./image/template.png", "./adb/image/screen.png", 0.9)
            px = maxloc[0]
            py = maxloc[1]
            if success:
                cmd = f"adb {add_cmd} shell input tap {px+20} {py+10}"
                self.subprocess_open(cmd)
                return

    def check_chatroom(self):
        count = 0
        while count < 5:
            sleep(0.5)
            self.capture_screen()
            success, maxloc = self.image_search("./image/template2.png", "./adb/image/screen.png", 0.9)
            if success:
                return True
            count += 1
        return False

    def update_last_number(self):
        try:
            self.open_kakaotalk_first_message()
            self.capture_screen()
            if not self.check_chatroom():
                self._last_number = '00000'
                return
            text = pytesseract.image_to_string('./adb/' + self._image_path, config=self._config)
            text = text.replace("\n\n", "\n").replace(" ", "")
            strs = text.split('예약인증번호')
            temp = strs[-1]
            auth_number = temp[temp.find('[')+1:temp.find(']')]
            if re.match(r"^\d{5}$", auth_number):
                self._last_number = auth_number
            else:
                self._last_number = '00000'
        except Exception as e:
            self._last_number = '00000'

    def set_phone_number(self, phone_number: str):
        if len(phone_number) == 0:
            self._has_phone_number = False
        else:
            self._has_phone_number = True
            self._phone_number[0] = phone_number[0:3]
            self._phone_number[1] = phone_number[3:7]
            self._phone_number[2] = phone_number[7:11]

    def get_phone_number(self):
        if self._has_phone_number:
            return self._phone_number
        else:
            return []

    def has_phone_number(self):
        return self._has_phone_number

    def OCR(self):
        try:
            start_time = time()
            self.open_kakaotalk_first_message()
            if not self.check_chatroom():
                return "00000"
            while True:
                self.capture_screen()
                text = pytesseract.image_to_string('./adb/' + self._image_path, config=self._config)
                text = text.replace("\n\n", "\n").replace(" ", "")
                strs = text.split('예약인증번호')
                temp = strs[-1]
                auth_number = temp[temp.find('[')+1:temp.find(']')]
                if re.match(r"^\d{5}$", auth_number) and auth_number != self._last_number:
                    self._last_number = auth_number
                    return auth_number
        except Exception as e:
            return self._last_number









