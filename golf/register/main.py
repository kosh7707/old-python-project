from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
from cryptography.fernet import Fernet

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setObjectName("RegisterWindow")
        self.setGeometry(1100, 100, 370, 300)
        self.setFixedSize(370, 300)
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(12)
        self.setFont(font)
        self.setWindowTitle("회원등록")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        self.id_input = QtWidgets.QLineEdit(self)
        self.id_input.setGeometry(QtCore.QRect(110, 30, 150, 30))
        self.id_input.setObjectName("id_input")
        self.id_input.setPlaceholderText("Id")

        self.pw_input = QtWidgets.QLineEdit(self)
        self.pw_input.setGeometry(QtCore.QRect(110, 75, 150, 30))
        self.pw_input.setObjectName("pw_input")
        self.pw_input.setPlaceholderText("Password")

        self.dateedit = QtWidgets.QDateEdit(self)
        self.dateedit.setGeometry(QtCore.QRect(110, 120, 150, 30))
        self.dateedit.setObjectName("dateedit")
        self.dateedit.setCalendarPopup(True)
        self.dateedit.setDate(QtCore.QDate.currentDate())

        self.register_button = QtWidgets.QPushButton(self)
        self.register_button.setGeometry(QtCore.QRect(110, 200, 150, 60))
        self.register_button.setFont(font)
        self.register_button.setObjectName("register_button")
        self.register_button.setText("등록")
        self.register_button.clicked.connect(self.register_button_clicked)

    def register_button_clicked(self):
        try:
            with open('customer_info', 'rb') as f:
                serial_number_encrypted = f.readline()
                serial_number = cipher_suite2.decrypt(serial_number_encrypted)
                serial_number = serial_number.decode()
        except:
            QtWidgets.QMessageBox.warning(self, '에러', 'customer_info 파일을 찾을 수 없습니다.')
            return
        self.id = self.id_input.text()
        self.pw = self.pw_input.text()
        self.date = str(self.dateedit.date().toPyDate())
        if self.id == '':
            QtWidgets.QMessageBox.warning(self, '에러', 'id칸이 공백입니다.')
            return
        elif self.pw == '':
            QtWidgets.QMessageBox.warning(self, '에러', 'password칸이 공백입니다.')
            return
        ret = QtWidgets.QMessageBox.question(self, '등록', f'id: {self.id}\npw: {self.pw}\n기한: {self.date}\n위 내용으로 등록합니다.', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if ret:
            with open('login_info', 'wb') as f:
                plain_text = self.id + '/' + self.pw + '/' + self.date + '/' + serial_number
                plain_text = plain_text.encode()
                cipher_text = cipher_suite.encrypt(plain_text)
                f.write(cipher_text)
            QtWidgets.QMessageBox.information(self, '완료', '등록이 완료되었습니다.\n폴더 내의 login_info를 확인해주세요.')

if __name__ == "__main__":
    key = b'9ttf2R4vegGEsD1gSGKvnHrbH5igesp6AD7FZ1iVaNo='
    get_serial_number_key = b'3yAxkyG8snCR8rqpRuTaMejhxrkTpf1eNnrg7WHBkhw='
    cipher_suite = Fernet(key)
    cipher_suite2 = Fernet(get_serial_number_key)
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())





