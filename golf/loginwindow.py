from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
from cryptography.fernet import Fernet
import datetime
import wmi


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.auth = False

        self.setObjectName("LoginWindow")
        self.setGeometry(1100, 100, 370, 300)
        self.setFixedSize(370, 300)
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(12)
        self.setFont(font)
        self.setWindowTitle("123")
        self.setWindowIcon(QtGui.QIcon('./image/icon.ico'))

        self.id_input = QtWidgets.QLineEdit(self)
        self.id_input.setGeometry(QtCore.QRect(110, 30, 150, 30))
        self.id_input.setObjectName("id_input")
        self.id_input.setPlaceholderText("Id")
        self.id_input.returnPressed.connect(self.login_button_clicked)

        self.pw_input = QtWidgets.QLineEdit(self)
        self.pw_input.setGeometry(QtCore.QRect(110, 75, 150, 30))
        self.pw_input.setObjectName("pw_input")
        self.pw_input.setPlaceholderText("Password")
        self.pw_input.returnPressed.connect(self.login_button_clicked)

        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.setGeometry(QtCore.QRect(110, 200, 150, 60))
        self.login_button.setFont(font)
        self.login_button.setObjectName("login_button")
        self.login_button.setText("Login")
        self.login_button.clicked.connect(self.login_button_clicked)

    def login_button_clicked(self):
        key = b'9ttf2R4vegGEsD1gSGKvnHrbH5igesp6AD7FZ1iVaNo='
        cipher_suite = Fernet(key)
        # login_info --> customer_info
        # customer_info : [id, pw, date, diskdriveSN, motherboardSN]
        try:
            with open('login_info', 'rb') as f:
                cipher_text = f.readline()
                plain_text = cipher_suite.decrypt(cipher_text)
                plain_text = plain_text.decode()
                customer_info = plain_text.split("/")
        except:
            self.auth = False
            self.close()
        # authorization serial_number
        c = wmi.WMI()
        diskdrive_serial_number = c.Win32_PhysicalMedia()[0].SerialNumber
        diskdrive_serial_number = diskdrive_serial_number.replace(" ", "")
        motherboard_product = c.Win32_BaseBoard()[0].Product
        motherboard_product = motherboard_product.replace(" ", "")
        if '/' in diskdrive_serial_number:
            diskdrive_serial_number = diskdrive_serial_number.replace('/', '')
        if '/' in motherboard_product:
            motherboard_product = motherboard_product.replace('/', '')
        if customer_info[3] != diskdrive_serial_number:
            QtWidgets.QMessageBox.warning(self, "인증 실패", "인증에 실패하였습니다. 관리자에게 문의해주세요")
            return
        if customer_info[4] != motherboard_product:
            QtWidgets.QMessageBox.warning(self, "인증 실패", "인증에 실패하였습니다. 관리자에게 문의해주세요")
            return
        # id, pw, expire_date check
        login_info = [self.id_input.text(), self.pw_input.text()]
        now = datetime.datetime.now()
        expire_date = datetime.datetime.strptime(customer_info[2], '%Y-%m-%d')
        if login_info[0] == customer_info[0] and login_info[1] == customer_info[1]:
            if now <= expire_date:
                QtWidgets.QMessageBox.information(self, "인증 성공", f'{customer_info[0]}님 반갑습니다.\n'
                                                                 f'프로그램 만기 기한: {customer_info[2]}')
                self.auth = True
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "기한 만료", f'프로그램 이용 기한 만료.\n프로그램 만기 기한: {customer_info[2]}')
                self.auth = False
        else:
            QtWidgets.QMessageBox.warning(self, '인증 실패', '인증 실패')
            self.auth = False








