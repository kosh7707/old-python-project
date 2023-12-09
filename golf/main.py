import sys, os
import time
import dateutil.relativedelta
import datetime
import configparser
import random

admin = True

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
def GetLogger(filename):
    formatter = logging.Formatter(fmt='[%(levelname)s]\t| %(asctime)s |\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    console_logger.setFormatter(formatter)
    logger.addHandler(console_logger)
    file_logger = logging.FileHandler(filename)
    file_logger.setLevel(logging.DEBUG)
    file_logger.setFormatter(formatter)
    logger.addHandler(file_logger)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
cwd = os.getcwd()
cwd = cwd.replace('\\', '/')
logger_filepath = cwd + '/log.txt'
def MakeSettingsFile():
    with open('./settings.ini', 'w+') as f:
        cwd = os.getcwd()
        cwd = cwd.replace('\\', '/')
        logger_filepath = cwd + '/log.txt'
        config = configparser.ConfigParser()
        config['logger'] = {}
        config['logger']['filepath'] = logger_filepath
        config['worker_count'] = {}
        config['worker_count']['count'] = '1'
        config['waiting'] = {}
        config['waiting']['waiting_time_prev_start'] = '20'
        config['waiting']['feedback_time'] = '30'
        config['waiting']['shutdown_resv'] = '1'
        config.write(f)
try:
    if os.path.isfile('./settings.ini'):
        config = configparser.ConfigParser()
        config.read('./settings.ini')
        temp_logger_filepath = config['logger']['filepath']
        if os.path.exists(temp_logger_filepath[:-7]):
            logger_filepath = temp_logger_filepath
        else:
            MakeSettingsFile()
    else:
        MakeSettingsFile()
except:
    MakeSettingsFile()
GetLogger(logger_filepath)
from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import MainWindow
from loginwindow import LoginWindow
if not os.path.isfile('./idlist.txt'):
    with open('./idlist.txt', 'w+') as f:
        pass
if not os.path.isfile('./chromedriver.exe'):
    os.system('pause')
    sys.exit()
if not os.path.isfile('./login_info'):
    os.system('pause')
    sys.exit()
if not os.path.isdir('./adb'):
    os.system('pause')
    sys.exit()
if not os.path.isdir('./Tesseract'):
    os.system('pause')
    sys.exit()
from selenium_function import *
from smsauth import SmsAuth
config = configparser.ConfigParser()
config.read('./settings.ini')

class Worker(QtCore.QObject):
    login_validation_check_signal = QtCore.pyqtSignal(int)
    resv_success_signal = QtCore.pyqtSignal(tuple)

    def __init__(self, idx):
        super(Worker, self).__init__()
        self.worker_idx = idx
        self.browser = None
        self.login_check = False
        self.config = configparser.ConfigParser()
        self.config.read('./settings.ini')
        self.smsauth = SmsAuth()


    @QtCore.pyqtSlot()          # From WindowThread.worker_browser_setting_signal
    def worker_browser_setting(self):
        self.browser = SettingBrowser('./chromedriver.exe', True)

    @QtCore.pyqtSlot()          # From WindowThread.worker_browser_quit_signal
    def worker_browser_quit(self):
        self.browser.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/ul[2]/li[1]/a").click()
        time.sleep(1)
        self.browser.quit()
        self.browser = None

    @QtCore.pyqtSlot()  # From MainWindow.loginlist_button_clicked
    def worker_browser_logout(self):
        if self.login_check is True:
            self.browser.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/ul[2]/li[1]/a").click()
            time.sleep(1)
            self.login_check = False

    @QtCore.pyqtSlot(list)      # From MainWindow.login_button_clicked
    def worker_browser_login(self, ls):
        url = "www.naver.com"
        self.browser.get(url)
        if self.login_check is False:
            login_ret = Login(self.browser, ls[0], ls[1])
            if login_ret is True:
                self.login_check = True
                self.login_validation_check_signal.emit(self.worker_idx)        # To MainWindow.login_validation_check
            elif login_ret is False:
                self.login_validation_check_signal.emit(-1)                     # To MainWindow.login_validation_check
            else:
                self.browser = login_ret
                self.login_validation_check_signal.emit(-1)                     # To MainWindow.login_validation_check

    def doWork(self, resv_list):
        for i in range(len(resv_list)):
            self.smsauth.set_phone_number(resv_list[i][4])
            self.browser.get("www.naver.com")
            if resv_list[i][0] == '1':
                self.browser.get('www.naver.com')
            elif resv_list[i][0] == '2':
                self.browser.get('www.naver.com')
            elif resv_list[i][0] == '3':
                self.browser.get('www.naver.com')
            elif resv_list[i][0] == '4':
                self.browser.get('www.naver.com')
            if FindResv(self.browser, resv_list[i], self.worker_idx):
                if MakeResv(self.browser, self.smsauth, self.worker_idx):
                    poped_resv = resv_list.pop(i)
                    self.resv_success_signal.emit(poped_resv)  # To MainWindow.resv_success
                    break

    @QtCore.pyqtSlot(list)      # From MainWindow.startmacro_signal
    def Start(self, resv_list):
        if len(self.smsauth.get_connected_device_list()) == 0:
            return
        self.smsauth.update_last_number()
        waiting_time = int(self.config['waiting']['waiting_time_prev_start'])
        feedback_time = int(self.config['waiting']['feedback_time'])
        shutdown_resv = bool(int(self.config['waiting']['shutdown_resv']))
        main_resv_start = False
        today = datetime.datetime.now().date()
        next_monday = today + dateutil.relativedelta.relativedelta(weekday=0)
        next_monday_9am = datetime.datetime(next_monday.year, next_monday.month, next_monday.day, 9)
        next_monday_9am_prev_waiting_time = datetime.datetime(next_monday.year, next_monday.month, next_monday.day, 8, 59, 60 - waiting_time)
        next_monday_9am_post_3min = datetime.datetime(next_monday.year, next_monday.month, next_monday.day, 9, 3, 0)
        raw_time = time.time()
        while not main_resv_start and len(resv_list) > 0:
            now = datetime.datetime.now()
            feedback_time_random = max(1, feedback_time + random.randint(-10, 10))
            time.sleep(1)
            if today == next_monday and now <= next_monday_9am:
                if now <= next_monday_9am_prev_waiting_time and time.time() - raw_time >= feedback_time_random:
                    raw_time = time.time()
                    self.doWork(resv_list)
                elif now >= next_monday_9am_prev_waiting_time:
                    main_resv_start = True
            else:
                if time.time() - raw_time >= feedback_time_random:
                    raw_time = time.time()
                    self.doWork(resv_list)
        while main_resv_start and len(resv_list) > 0:
            if datetime.datetime.now() >= next_monday_9am_post_3min:
                if shutdown_resv:
                    os.system("shutdown -s -f -t 120")
                break
            self.doWork(resv_list)

class WindowThread(QtCore.QObject):
    worker_browser_setting_signal = QtCore.pyqtSignal()
    worker_browser_quit_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(WindowThread, self).__init__()
        self.worker_count = 1
        self.mainwindow = MainWindow(self.worker_count)
        self.worker_list = []
        self.worker_thread_list = []
        for i in range(self.worker_count):
            # generate worker and thread
            worker = Worker(i)
            worker_thread = QtCore.QThread()
            self.worker_list.append(worker)
            self.worker_thread_list.append(worker_thread)
        for i in range(self.worker_count):
            # thread start
            self.worker_list[i].moveToThread(self.worker_thread_list[i])
            self.worker_thread_list[i].start()
            # connect signal WindowThread
            self.worker_browser_setting_signal.connect(self.worker_list[i].worker_browser_setting)
            self.worker_browser_quit_signal.connect(self.worker_list[i].worker_browser_quit)
            # connect signal Mainwindow
            self.mainwindow.startmacro_signal.connect(self.worker_list[i].Start)
            self.mainwindow.worker_browser_login_signal.connect(self.worker_list[i].worker_browser_login)
            self.mainwindow.worker_browser_logout_signal.connect(self.worker_list[i].worker_browser_logout)
            # connect signal worker_list[i] == Worker
            self.worker_list[i].resv_success_signal.connect(self.mainwindow.resv_success)
            self.worker_list[i].login_validation_check_signal.connect(self.mainwindow.login_validation_check)
        self.mainwindow.stopmacro_signal.connect(self.Stop)

    @QtCore.pyqtSlot()      # From MainWindow.stopmacro_signal // stop_button_clicked
    def Stop(self):
        for i in range(self.worker_count):
            if self.worker_thread_list[i].isRunning():
                self.worker_thread_list[i].terminate()
                self.worker_thread_list[i].wait()
                self.worker_thread_list[i].start()

if __name__ == "__main__":
    if admin:
        app = QtWidgets.QApplication(sys.argv)
        app.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
        MyWindow = WindowThread()
        MyWindow.worker_browser_setting_signal.emit()
        MyWindow.mainwindow.show()
        app.exec_()
        MyWindow.worker_browser_quit_signal.emit()
        while MyWindow.worker_list[-1].browser:
            sleep(1)
        sys.exit()
    else:
        app = QtWidgets.QApplication(sys.argv)
        app.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
        loginwindow = LoginWindow()
        loginwindow.show()
        app.exec_()
        if loginwindow.auth:
            MyWindow = WindowThread()
            MyWindow.worker_browser_setting_signal.emit()
            MyWindow.mainwindow.show()
            app.exec_()
            MyWindow.worker_browser_quit_signal.emit()
            while MyWindow.worker_list[-1].browser:
                sleep(1)
        sys.exit()





















