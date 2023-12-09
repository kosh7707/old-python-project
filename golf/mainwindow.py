from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import os
from time import sleep

class MainWindow(QtWidgets.QWidget):
    startmacro_signal = QtCore.pyqtSignal(list)
    stopmacro_signal = QtCore.pyqtSignal()
    worker_browser_login_signal = QtCore.pyqtSignal(list)
    worker_browser_logout_signal = QtCore.pyqtSignal()

    def __init__(self, worker_count):
        super(MainWindow, self).__init__()
        self.worker_count = worker_count
        self.login_check = [False for _ in range(self.worker_count)]
        self.area = ''
        self.date = []
        self.time = ''
        self.order = ''
        self.resv_list = []
        self.resv_success_idx_list = []
        self.settings_window = SettingsWindow()

        # MainWindow
        self.setObjectName("MainWindow")
        self.setGeometry(1100, 100, 580, 800)
        self.setFixedSize(580, 800)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(12)
        self.centralwidget.setFont(font)
        self.setWindowTitle("123")
        self.setWindowIcon(QtGui.QIcon('./image/icon.ico'))

        # <-------- login part start -------->
        # login_button (QPushButton)
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(180, 15, 60, 55))
        self.login_button.setFont(font)
        self.login_button.setObjectName("login_button")
        self.login_button.setText("Login")
        self.login_button.clicked.connect(self.login_button_clicked)

        # id_input (QLineEdit)
        self.id_input = QtWidgets.QLineEdit(self.centralwidget)
        self.id_input.setGeometry(QtCore.QRect(20, 15, 150, 25))
        self.id_input.setObjectName("id_input")
        self.id_input.setPlaceholderText("Id")
        self.id_input.returnPressed.connect(self.login_button_clicked)

        # pw_input (QLineEdit)
        self.pw_input = QtWidgets.QLineEdit(self.centralwidget)
        self.pw_input.setGeometry(QtCore.QRect(20, 45, 150, 25))
        self.pw_input.setObjectName("pw_input")
        self.pw_input.setPlaceholderText("Password")
        self.pw_input.returnPressed.connect(self.login_button_clicked)

        # loginlist_button (QPushButton)
        self.loginlist_button = QtWidgets.QPushButton(self.centralwidget)
        self.loginlist_button.setGeometry(QtCore.QRect(20, 80, 220, 30))
        self.loginlist_button.setObjectName("loginlist_button")
        self.loginlist_button.setText("아이디 리스트")
        self.loginlist_button.clicked.connect(self.loginlist_button_clicked)
        # <-------- login part end -------->

        # <-------- status part start -------->
        # current_time_label (QLabel)
        self.current_time_label = QtWidgets.QLabel(self.centralwidget)
        self.current_time_label.setGeometry(QtCore.QRect(260, 45, 300, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.current_time_label.setFont(font)
        self.current_time_label.setObjectName("current_time_label")
        self.now_date = QtCore.QDate.currentDate().toString(QtCore.Qt.DefaultLocaleLongDate)
        self.now_time = QtCore.QTime.currentTime().toString(" hh:mm:ss")
        self.current_time_label.setText(self.now_date + self.now_time)
        self.timeVar = QtCore.QTimer()
        self.timeVar.setInterval(500)
        self.timeVar.timeout.connect(self.updateTime)
        self.timeVar.start()

        # status_label (QLabel)
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(260, 15, 260, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.status_label.setFont(font)
        self.status_label.setObjectName("status_label")
        self.status_label.setText("로그인 필요")

        self.settings_button = QtWidgets.QPushButton(self.centralwidget)
        self.settings_button.setGeometry(QtCore.QRect(535, 15, 25, 25))
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setIcon(QtGui.QIcon('./image/settings_icon.png'))
        self.settings_button.clicked.connect(self.settings_button_clicked)
        # <-------- status part end -------->

        # <-------- resv part start -------->
        # area_combobox (QComboBox)
        self.area_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.area_combobox.setGeometry(QtCore.QRect(65, 125, 160, 25))
        self.area_combobox.setObjectName("area_combobox")
        self.area_combobox.addItem("1")
        self.area_combobox.addItem("2")
        self.area_combobox.addItem("3")
        self.area_combobox.addItem("4")
        self.area_combobox.currentTextChanged.connect(self.area_combobox_changed)

        # dateedit (QDateEdit)
        self.dateedit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateedit.setGeometry(QtCore.QRect(290, 125, 160, 25))
        self.dateedit.setObjectName("dateedit")
        self.dateedit.setCalendarPopup(True)
        self.dateedit.setDate(QtCore.QDate.currentDate())
        self.dateedit.dateChanged.connect(self.dateedit_changed)

        # time_combobox (QComboBox)
        self.time_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.time_combobox.setGeometry(QtCore.QRect(65, 160, 160, 25))
        self.time_combobox.setObjectName("time_combobox")
        for i in range(6, 21):
            if i < 10:
                self.time_combobox.addItem('0' + str(i))
            else:
                self.time_combobox.addItem(str(i))
        self.time_combobox.currentTextChanged.connect(self.time_combobox_changed)

        # order_combobox (QComboBox)
        self.order_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.order_combobox.setGeometry(QtCore.QRect(290, 160, 160, 25))
        self.order_combobox.setObjectName("order_combobox")
        for i in range(1, 13):
            self.order_combobox.addItem(str(i))
        self.order_combobox.currentTextChanged.connect(self.order_combobox_changed)

        # phonenumber_input (QLineEdit)
        self.phonenumber_input = QtWidgets.QLineEdit(self.centralwidget)
        self.phonenumber_input.setGeometry(QtCore.QRect(65, 195, 160, 25))
        self.phonenumber_input.setObjectName("phonenumber_input")
        self.phonenumber_input.setPlaceholderText("01012345678")
        self.phonenumber_input.returnPressed.connect(self.login_button_clicked)
        self.phonenumber_input.setValidator(QtGui.QIntValidator())

        # phonenumber_checkbox (QCheckBox)
        self.phonenumber_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.phonenumber_checkbox.setGeometry(QtCore.QRect(245, 195, 160, 25))
        self.phonenumber_checkbox.setText("원래 번호 사용")
        self.phonenumber_checkbox.stateChanged.connect(self.phonenumber_checkbox_changed)

        # addresv_button (QPushButton)
        self.addresv_button = QtWidgets.QPushButton(self.centralwidget)
        self.addresv_button.setGeometry(QtCore.QRect(460, 125, 100, 100))
        self.addresv_button.setObjectName("addresv_button")
        self.addresv_button.setText("예약 추가")
        self.addresv_button.clicked.connect(self.addresv_button_clicked)

        # tablewidget (QTableWidget)
        self.tablewidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tablewidget.setGeometry(QtCore.QRect(20, 240, 540, 500))
        self.tablewidget.setObjectName("tablewidget")
        self.tablewidget.setColumnCount(7)
        self.tablewidget.setHorizontalHeaderLabels(['지역', '날짜', '시간', '순번', '번호', '상태', '삭제'])
        self.tablewidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tablewidget.setSortingEnabled(False)
        self.tablewidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tablewidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tablewidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tablewidget.resizeColumnsToContents()
        # <-------- resv part end -------->

        # <-------- exec part start -------->
        # settings_save_button (QPushButton)
        self.settings_save_button = QtWidgets.QPushButton(self.centralwidget)
        self.settings_save_button.setGeometry(QtCore.QRect(20, 750, 120, 40))
        self.settings_save_button.setObjectName("settings_save_button")
        self.settings_save_button.setText("설정 저장하기")
        self.settings_save_button.setDisabled(True)
        self.settings_save_button.clicked.connect(self.settings_save_button_clicked)

        # settings_load_button (QPushButton)
        self.settings_load_button = QtWidgets.QPushButton(self.centralwidget)
        self.settings_load_button.setGeometry(QtCore.QRect(150, 750, 120, 40))
        self.settings_load_button.setObjectName("settings_load_button")
        self.settings_load_button.setText("설정 불러오기")
        self.settings_load_button.clicked.connect(self.settings_load_button_clicked)

        # start_button (QPushButton)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(390, 750, 80, 40))
        self.start_button.setObjectName("start_button")
        self.start_button.setText("시작")
        self.start_button.setDisabled(True)
        self.start_button.clicked.connect(self.start_button_clicked)

        # stop_button (QPushButton)
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(480, 750, 80, 40))
        self.stop_button.setObjectName("stop_button")
        self.stop_button.setText("종료")
        self.stop_button.setDisabled(True)
        self.stop_button.clicked.connect(self.stop_button_clicked)
        # <-------- exec part end -------->

        # <-------- etc part start -------->
        # label_0 --> '지역 :'
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setGeometry(QtCore.QRect(20, 125, 50, 25))
        self.label_0.setObjectName("label")
        self.label_0.setText("지역 :")

        # label_1 --> '날짜 :'
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(QtCore.QRect(245, 125, 50, 25)))
        self.label_1.setObjectName("label_1")
        self.label_1.setText("날짜 :")

        # label_2 --> '시간 :'
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 160, 50, 25))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("시간 :")

        # label_3 --> '순번 :'
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(245, 160, 50, 25))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("순번 :")

        # label_4 --> '번호 :'
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 195, 50, 25))
        self.label_4.setObjectName("label_4")
        self.label_4.setText("번호 :")

        # etc
        QtCore.QMetaObject.connectSlotsByName(self)
        self.area_combobox_changed()
        self.dateedit_changed()
        self.time_combobox_changed()
        self.order_combobox_changed()
        # <-------- etc part end -------->

    def updateTime(self):
        self.now_time = QtCore.QTime.currentTime().toString(" hh:mm:ss")
        self.current_time_label.setText(self.now_date + self.now_time)

    def login_button_clicked(self):
        self.login_button.setDisabled(True)
        self.id_input.setDisabled(True)
        self.pw_input.setDisabled(True)
        login_id = self.id_input.text()
        login_pw = self.pw_input.text()
        self.worker_browser_login_signal.emit([login_id, login_pw])     # To Worker.worker_browser_login

    @QtCore.pyqtSlot(int)      # From Worker.worker_browser_login
    def login_validation_check(self, success_idx):
        if success_idx >= 0:
            self.status_label.setText("로그인 완료")
            self.start_button.setDisabled(False)
            self.settings_save_button.setDisabled(False)
            self.login_check[success_idx] = True
        elif success_idx == -1:
            self.status_label.setText("로그인 실패, id와 pw를 확인해주세요")
            self.login_button.setDisabled(False)
            self.id_input.setDisabled(False)
            self.pw_input.setDisabled(False)

    def area_combobox_changed(self):
        self.area = self.area_combobox.currentText()

    def dateedit_changed(self):
        self.date = str(self.dateedit.date().toPyDate())
        self.date = self.date.split("-")

    def time_combobox_changed(self):
        self.time = self.time_combobox.currentText()

    def order_combobox_changed(self):
        self.order = self.order_combobox.currentText()

    def addresv_button_clicked(self):
        phone_number = self.phonenumber_input.text()
        if (self.area, self.date, self.time, self.order, phone_number) in self.resv_list:
            QtWidgets.QMessageBox.warning(self, "예약 추가 실패", "중복되는 예약은 넣으실 수 없습니다.")
        else:
            if self.phonenumber_checkbox.isChecked():
                self.resv_list.append((self.area, self.date, self.time, self.order, phone_number))
                self.itemwidget_add_item(self.resv_list[-1])
            else:
                if len(phone_number) != 11 or (len(phone_number) == 11 and phone_number[0] == '-'):
                    QtWidgets.QMessageBox.warning(self, "예약 추가 실패", "휴대폰 번호를 확인해주세요.")
                else:
                    self.resv_list.append((self.area, self.date, self.time, self.order, phone_number))
                    self.itemwidget_add_item(self.resv_list[-1])

    def delete_button_clicked(self):
        button = self.sender()
        row = self.tablewidget.indexAt(button.pos()).row()
        self.tablewidget.removeRow(row)
        if row in self.resv_success_idx_list:
            self.resv_success_idx_list.remove(row)
        for i in range(len(self.resv_success_idx_list)):
            if self.resv_success_idx_list[i] > row:
                self.resv_success_idx_list[i] -= 1
        self.resv_list.pop(int(row))

    @QtCore.pyqtSlot(tuple)      # From Worker.resv_success_signal // Worker.Start
    def resv_success(self, poped_resv):
        idx = self.resv_list.index(poped_resv)
        self.resv_success_idx_list.append(idx)
        self.resv_success_idx_list.sort()
        status_item = QtWidgets.QTableWidgetItem('예약 성공')
        status_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tablewidget.setItem(idx, 5, status_item)
        self.tablewidget.resizeColumnsToContents()

    def start_button_clicked(self):
        if len(self.resv_success_idx_list) != 0:
            while len(self.resv_success_idx_list) != 0:
                idx = self.resv_success_idx_list.pop(-1)
                self.resv_list.pop(idx)
                self.tablewidget.removeRow(idx)
        self.stop_button.setDisabled(False)
        self.start_button.setDisabled(True)
        self.addresv_button.setDisabled(True)
        self.tablewidget.setDisabled(True)
        self.settings_button.setDisabled(True)
        self.startmacro_signal.emit(self.resv_list)       # To Worker.Start

    def stop_button_clicked(self):
        self.stop_button.setDisabled(True)
        self.start_button.setDisabled(False)
        self.addresv_button.setDisabled(False)
        self.tablewidget.setDisabled(False)
        self.settings_button.setDisabled(False)
        self.stopmacro_signal.emit()        # To WindowThread.Stop

    def itemwidget_add_item(self, ls):      # ls: (area, date, time, order, phone_number) --> tuple을 받게될거임.
        # Insert new row
        rowIndex = self.tablewidget.rowCount()
        self.tablewidget.insertRow(rowIndex)
        # set area_item column 0
        area_item = QtWidgets.QTableWidgetItem(ls[0])
        area_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tablewidget.setItem(rowIndex, 0, area_item)
        # set date_item column 1
        date_item = QtWidgets.QTableWidgetItem('{}-{}-{}'.format(ls[1][0], ls[1][1], ls[1][2]))
        date_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tablewidget.setItem(rowIndex, 1, date_item)
        # set time_item column 2
        time_item = QtWidgets.QTableWidgetItem(ls[2])
        time_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tablewidget.setItem(rowIndex, 2, time_item)
        # set order_item column 3
        order_item = QtWidgets.QTableWidgetItem(ls[3])
        order_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tablewidget.setItem(rowIndex, 3, order_item)
        # set phone_number_item column 4
        phone_number = ls[4][0:3] + '-' + ls[4][3:7] + '-' + ls[4][7:11]
        phone_number_item = QtWidgets.QTableWidgetItem(phone_number)
        phone_number_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tablewidget.setItem(rowIndex, 4, phone_number_item)
        # set status_item column 5
        status_item = QtWidgets.QTableWidgetItem('')
        status_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tablewidget.setItem(rowIndex, 5, status_item)
        # set delete_button column 6
        delete_button = QtWidgets.QPushButton()
        delete_button.setFixedSize(50, 30)
        delete_button.setText('삭제')
        delete_button.clicked.connect(self.delete_button_clicked)
        self.tablewidget.setCellWidget(rowIndex, 6, delete_button)
        self.tablewidget.resizeColumnsToContents()

    def settings_save_button_clicked(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, 'save settings', './', 'Config Files(*.ini)')
        file_path = file_path[0]
        if file_path:
            login_info = [self.id_input.text(), self.pw_input.text()]
            save_resv_list = self.resv_list
            config = configparser.ConfigParser()
            config['login'] = {}
            config['login']['id'] = login_info[0]
            config['login']['pw'] = login_info[1]
            config['resv_list'] = {}
            for i in range(len(save_resv_list)):
                config['resv_list']['resv{}'.format(i)] = str(save_resv_list[i])
            with open(file_path, 'w') as f:
                config.write(f)

    def settings_load_button_clicked(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'open settings', './', 'Config Files(*.ini)')
        file_path = file_path[0]
        if file_path:
            config = configparser.ConfigParser()
            config.read(file_path)
            if config.has_section('login') and config.has_section('resv_list'):
                login_info = [config['login']['id'], config['login']['pw']]
                if False in self.login_check:
                    self.login_button.setDisabled(True)
                    self.id_input.setDisabled(True)
                    self.pw_input.setDisabled(True)
                    self.id_input.setText(login_info[0])
                    self.pw_input.setText(login_info[1])
                    self.worker_browser_login_signal.emit(login_info)       # To Worker.worker_browser_login
                raw_resv_list = config.items('resv_list')
                for i in range(len(raw_resv_list)):
                    self.resv_list.append(eval(raw_resv_list[i][1]))
                    self.itemwidget_add_item(self.resv_list[-1])
            else:
                QtWidgets.QMessageBox.warning(self, '파일 누락', '설정 파일이 누락되었습니다.')

    def settings_button_clicked(self):
        self.settings_window.exec_()

    def loginlist_button_clicked(self):
        loginlist_window = LoginListWindow()
        accepted = loginlist_window.exec_()
        loginlist = loginlist_window.loginlist
        with open('./idlist.txt', 'w+') as f:
            for i in range(len(loginlist)):
                item = loginlist[i]
                item[2] = loginlist_window.loginlist_tablewidget.cellWidget(i, 2).text()
                f.write(item[0] + ',,,' + item[1] + ',,,' + item[2] + '\n')
        if accepted:
            rowIndex = loginlist_window.loginlist_tablewidget.currentRow()
            login_id = loginlist[rowIndex][0]
            login_pw = loginlist[rowIndex][1]
            self.id_input.setText(login_id)
            self.pw_input.setText(login_pw)
            self.status_label.setText(f"선택한 아이디 로그인 시도")
            self.worker_browser_logout_signal.emit()
            sleep(1)
            self.login_button_clicked()

    def phonenumber_checkbox_changed(self):
        if self.phonenumber_checkbox.isChecked():
            self.phonenumber_input.setEnabled(False)
            self.phonenumber_input.setPlaceholderText("")
            self.phonenumber_input.setText("")
        else:
            self.phonenumber_input.setEnabled(True)
            self.phonenumber_input.setPlaceholderText("01012345678")


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.config = configparser.ConfigParser()
        self.config.read('./settings.ini')
        self.logger_filepath = self.config['logger']['filepath']
        self.worker_count = self.config['worker_count']['count']
        self.waiting_time_prev_start = self.config['waiting']['waiting_time_prev_start']
        self.feedback_time = self.config['waiting']['feedback_time']
        self.shutdown_resv = self.config['waiting']['shutdown_resv']

        self.setWindowIcon(QtGui.QIcon('./image/icon.ico'))
        self.setWindowTitle('설정')
        self.setFixedSize(390, 330)
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(12)
        self.setFont(font)

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setGeometry(QtCore.QRect(15, 15, 300, 30))
        self.label1.setText('로그 파일 경로 지정 (재실행시 적용)')

        self.filepath_lineedit = QtWidgets.QLineEdit(self)
        self.filepath_lineedit.setGeometry(QtCore.QRect(15, 55, 330, 30))
        self.filepath_lineedit.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(8)
        self.filepath_lineedit.setFont(font)
        self.filepath_lineedit.setAlignment(QtCore.Qt.AlignLeft)
        self.filepath_lineedit.setText(self.logger_filepath)

        self.filepath_button = QtWidgets.QPushButton(self)
        self.filepath_button.setGeometry(QtCore.QRect(344, 54, 32, 32))
        self.filepath_button.setIcon(QtGui.QIcon('./image/filepath_icon.png'))
        self.filepath_button.clicked.connect(self.filepath_button_clicked)

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setGeometry(QtCore.QRect(15, 115, 260, 30))
        self.label2.setText('백그라운드 크롬 수 (재실행시 적용)')

        self.chrome_number_combobox = QtWidgets.QComboBox(self)
        self.chrome_number_combobox.setGeometry(QtCore.QRect(300, 115, 76, 30))
        for i in range(1, 10):
            self.chrome_number_combobox.addItem(str(i))
        self.chrome_number_combobox.setCurrentText(self.worker_count)

        self.label3 = QtWidgets.QLabel(self)
        self.label3.setGeometry(QtCore.QRect(65, 185, 150, 30))
        self.label3.setText('대기시간( 5 ~ 60초)')

        self.waiting_time_lineedit = QtWidgets.QLineEdit(self)
        self.waiting_time_lineedit.setGeometry(QtCore.QRect(220, 185, 35, 30))
        self.waiting_time_lineedit.setText(self.waiting_time_prev_start)
        self.waiting_time_lineedit.setValidator(QtGui.QIntValidator(10, 60, self))

        self.label4 = QtWidgets.QLabel(self)
        self.label4.setGeometry(QtCore.QRect(260, 185, 70, 30))
        self.label4.setText('초 전까지')

        self.label5 = QtWidgets.QLabel(self)
        self.label5.setGeometry(QtCore.QRect(65, 230, 150, 30))
        self.label5.setText('피드백 텀(단위: 초)')

        self.feedback_time_lineedit = QtWidgets.QLineEdit(self)
        self.feedback_time_lineedit.setGeometry(QtCore.QRect(220, 230, 35, 30))
        self.feedback_time_lineedit.setText(self.feedback_time)
        self.feedback_time_lineedit.setValidator(QtGui.QIntValidator(30, 600, self))

        self.label6 = QtWidgets.QLabel(self)
        self.label6.setGeometry(QtCore.QRect(260, 230, 70, 30))
        self.label6.setText('초 마다')

        self.quit_button = QtWidgets.QPushButton(self)
        self.quit_button.setGeometry(QtCore.QRect(300, 285, 76, 30))
        self.quit_button.setText('닫기')
        self.quit_button.clicked.connect(self.quit_button_clicked)

        self.shutdown_resv_checkbox = QtWidgets.QCheckBox(self)
        self.shutdown_resv_checkbox.setGeometry(QtCore.QRect(20, 285, 160, 30))
        self.shutdown_resv_checkbox.setText("컴퓨터 자동종료")
        if self.shutdown_resv == '1':
            self.shutdown_resv_checkbox.setChecked(True)


    def filepath_button_clicked(self):
        filepath = QtWidgets.QFileDialog.getExistingDirectory(self, 'log filepath')
        if filepath == '':
            return
        self.config['logger']['filepath'] = filepath + '/log.txt'
        self.filepath_lineedit.setText(filepath + '/log.txt')
        with open('./settings.ini', 'w+') as f:
            self.config.write(f)

    def closeEvent(self, close_event):
        self.quit_button_clicked()

    def quit_button_clicked(self):
        if not 5 <= int(self.waiting_time_lineedit.text()) <= 60:
            QtWidgets.QMessageBox.warning(self, '에러', '대기 시간을 확인해주세요(5 ~ 60사이)')
            return
        self.config['worker_count']['count'] = self.chrome_number_combobox.currentText()
        self.config['waiting']['waiting_time_prev_start'] = self.waiting_time_lineedit.text()
        self.config['waiting']['feedback_time'] = self.feedback_time_lineedit.text()
        self.config['waiting']['shutdown_resv'] = str(int(self.shutdown_resv_checkbox.isChecked()))
        with open('./settings.ini', 'w+') as f:
            self.config.write(f)
        self.accept()


class LoginListWindow(QtWidgets.QDialog):
    def __init__(self):
        super(LoginListWindow, self).__init__()

        self.setWindowIcon(QtGui.QIcon('./image/icon.ico'))
        self.setWindowTitle('아이디 리스트')
        self.setFixedSize(510, 450)
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(12)
        self.setFont(font)
        self.loginlist = []

        self.loginlist_tablewidget = QtWidgets.QTableWidget(self)
        self.loginlist_tablewidget.setGeometry(QtCore.QRect(10, 10, 400, 430))
        self.loginlist_tablewidget.setColumnCount(3)
        self.loginlist_tablewidget.setHorizontalHeaderLabels(['id', 'pw', 'description'])
        self.loginlist_tablewidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.loginlist_tablewidget.setSortingEnabled(False)
        self.loginlist_tablewidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        with open('./idlist.txt', 'r+') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            for line in lines:
                ls = line.split(',,,')
                if len(ls) == 3:
                    self.loginlist.append(ls)
                    self.itemwidget_add_item(ls)
        self.loginlist_tablewidget.resizeColumnsToContents()
        self.loginlist_tablewidget.doubleClicked.connect(self.accept)

        self.add_button = QtWidgets.QPushButton(self)
        self.add_button.setGeometry(QtCore.QRect(420, 10, 80, 40))
        self.add_button.setText("추가")
        self.add_button.clicked.connect(self.add_button_clicked)

        self.remove_button = QtWidgets.QPushButton(self)
        self.remove_button.setGeometry(QtCore.QRect(420, 60, 80, 40))
        self.remove_button.setText("제거")
        self.remove_button.clicked.connect(self.remove_button_clicked)

        self.reject_button = QtWidgets.QPushButton(self)
        self.reject_button.setGeometry(QtCore.QRect(420, 400, 80, 40))
        self.reject_button.setText("닫기")
        self.reject_button.clicked.connect(self.reject)

    def itemwidget_add_item(self, ls):
        rowIndex = self.loginlist_tablewidget.rowCount()
        self.loginlist_tablewidget.insertRow(rowIndex)
        id_item = QtWidgets.QTableWidgetItem(ls[0])
        id_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.loginlist_tablewidget.setItem(rowIndex, 0, id_item)
        pw_item = QtWidgets.QTableWidgetItem(ls[1])
        pw_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.loginlist_tablewidget.setItem(rowIndex, 1, pw_item)
        description_lineedit = QtWidgets.QLineEdit()
        description_lineedit.setPlaceholderText("Description")
        description_lineedit.setText(ls[2])
        description_lineedit.setBaseSize(250, 30)
        self.loginlist_tablewidget.setCellWidget(rowIndex, 2, description_lineedit)
        self.loginlist_tablewidget.resizeColumnsToContents()

    def add_button_clicked(self):
        idPwInputDialog = IdPwInputDialog()
        if idPwInputDialog.exec_():
            login_id = idPwInputDialog.id_input.text()
            login_pw = idPwInputDialog.pw_input.text()
            ls = [login_id, login_pw, '']
            self.loginlist.append(ls)
            self.itemwidget_add_item(ls)

    def remove_button_clicked(self):
        row = self.loginlist_tablewidget.currentRow()
        self.loginlist_tablewidget.removeRow(row)
        self.loginlist.pop(row)


class IdPwInputDialog(QtWidgets.QDialog):
    def __init__(self):
        super(IdPwInputDialog, self).__init__()

        self.setWindowIcon(QtGui.QIcon('./image/icon.ico'))
        self.setWindowTitle('아이디 추가')
        self.setFixedSize(190, 150)
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(12)
        self.setFont(font)

        self.id_input = QtWidgets.QLineEdit(self)
        self.id_input.setGeometry(QtCore.QRect(20, 15, 150, 25))
        self.id_input.setObjectName("id_input")
        self.id_input.setPlaceholderText("Id")
        self.id_input.returnPressed.connect(self.accept_button_clicked)

        self.pw_input = QtWidgets.QLineEdit(self)
        self.pw_input.setGeometry(QtCore.QRect(20, 45, 150, 25))
        self.pw_input.setObjectName("pw_input")
        self.pw_input.setPlaceholderText("Password")
        self.pw_input.returnPressed.connect(self.accept_button_clicked)

        self.accept_button = QtWidgets.QPushButton(self)
        self.accept_button.setGeometry(QtCore.QRect(20, 100, 70, 30))
        self.accept_button.setText("확인")
        self.accept_button.clicked.connect(self.accept_button_clicked)

        self.reject_button = QtWidgets.QPushButton(self)
        self.reject_button.setGeometry(QtCore.QRect(100, 100, 70, 30))
        self.reject_button.setText("취소")
        self.reject_button.clicked.connect(self.reject)

    def accept_button_clicked(self):
        if self.id_input.text() == "" or self.pw_input.text() == "":
            QtWidgets.QMessageBox.warning(self, "아이디 추가 실패", "유효하지 않은 id / pw")
        else:
            self.accept()

