from PyQt5 import QtCore, QtGui, QtWidgets
from selenium_function import *
from mainwindow import MainWindow
from ocr import OcrTool
import sys, os
import logging
from time import sleep

# setting logger
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
def GetLogger(filename):
    formatter = logging.Formatter(fmt='[%(levelname)s]\t| %(asctime)s |\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # console_logger
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    console_logger.setFormatter(formatter)
    logger.addHandler(console_logger)
    # file_logger
    file_logger = logging.FileHandler(filename)
    file_logger.setLevel(logging.DEBUG)
    file_logger.setFormatter(formatter)
    logger.addHandler(file_logger)
GetLogger("./log.txt")

class Worker(QtCore.QObject):
    tnrzh_list_signal = QtCore.pyqtSignal(tuple)

    def __init__(self, worker_number):
        super(Worker, self).__init__()
        self.browser = None
        self.worker_number = worker_number

    @QtCore.pyqtSlot()          # From MainThread.worker_browser_setting_signal
    def worker_browser_setting(self):
        logging.debug(f"worker {self.worker_number} browser setting start")
        self.browser = SettingBrowser("./chromedriver.exe", True)
        logging.debug(f"worker {self.worker_number} browser setting success")

    @QtCore.pyqtSlot()          # From MainThread.worker_browser_quit_signal
    def worker_browser_quit(self):
        self.browser.quit()
        self.browser = None

    @QtCore.pyqtSlot(list)          # From MainWindow.search_signal
    def search(self, search_list):
        search_list = search_list[self.worker_number*2:(self.worker_number+1)*2]
        logging.debug(f"worker {self.worker_number}, name_list: {search_list}")
        self.tnrzh_list_signal.emit((self.worker_number+1, Search(self.browser, search_list[0])))
        self.tnrzh_list_signal.emit((self.worker_number+5, Search(self.browser, search_list[1])))


class MainThread(QtCore.QObject):
    worker_browser_setting_signal = QtCore.pyqtSignal()
    worker_browser_quit_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(MainThread, self).__init__()
        self.worker_count = 4
        self.mainwindow = MainWindow(self.worker_count)
        self.worker_list = []
        self.worker_thread_list = []
        for i in range(self.worker_count):
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
            # connect signal MainWindow
            self.mainwindow.search_signal.connect(self.worker_list[i].search)
            self.worker_list[i].tnrzh_list_signal.connect(self.mainwindow.getTnrzhList)


def main():
    if not os.path.isfile('./chromedriver.exe'):
        logging.error('chromedriver.exe missing')
        os.system('pause')
        sys.exit()
    mainThread = None
    try:
        app = QtWidgets.QApplication(sys.argv)
        app.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
        mainThread = MainThread()
        mainThread.worker_browser_setting_signal.emit()
        mainThread.mainwindow.show()
        app.exec_()
        mainThread.worker_browser_quit_signal.emit()
        while mainThread.worker_list[-1].browser:
            logging.info("waiting browser quit")
            sleep(1)
        logging.info("browser quit success")
        logging.info("system close")
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        while mainThread.worker_list[-1].browser:
            logging.info("waiting browser quit")
            sleep(1)
        logging.info("browser quit success")
        logging.info("system close")
        sys.exit(0)

if __name__ == "__main__":
    main()
