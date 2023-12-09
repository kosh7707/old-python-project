from PyQt5 import QtCore, QtGui, QtWidgets
from capture import CaptureTool
from ocr import OcrTool
import webbrowser
import logging
import configparser

class MainWindow(QtWidgets.QWidget):
    search_signal = QtCore.pyqtSignal(list)

    def __init__(self, worker_count):
        super(MainWindow, self).__init__()
        self.worker_conut = worker_count
        self.tnrzh_list = {}
        self.settings_window = SettingsWindow()

        # MainWindow
        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.setGeometry(1100, 100, 800, 600)
        self.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(12)
        self.centralwidget.setFont(font)
        self.setWindowTitle("사사게 검색기")
        self.setWindowIcon(QtGui.QIcon('./image/icon.ico'))

        # horizontalLayoutWidget_1
        self.horizontalLayoutWidget_1 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_1.setGeometry(QtCore.QRect(20, 20, 460, 40))
        self.horizontalLayoutWidget_1.setObjectName("horizontalLayoutWidget_1")

        # horizontalLayout_1            --> in horizontalLayoutWidget_1
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_1)
        self.horizontalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")

        # settings_button (QPushButton)
        self.settings_button = QtWidgets.QPushButton(self.centralwidget)
        self.settings_button.setGeometry(QtCore.QRect(730, 20, 40, 40))
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setIcon(QtGui.QIcon("./image/settings_icon.png"))
        self.settings_button.clicked.connect(self.settings_button_clicked)

        # capture_button (QPushButton)  --> in horizontalLayout_1
        self.capture_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.capture_button.sizePolicy().hasHeightForWidth())
        self.capture_button.setSizePolicy(sizePolicy)
        self.capture_button.setObjectName("capture_button")
        self.capture_button.setText("화면 캡쳐")
        self.capture_button.clicked.connect(self.capture_button_clicked)
        self.horizontalLayout_1.addWidget(self.capture_button)

        # ocr_button (QPushButton)      --> in horizontalLayout_1
        self.ocr_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ocr_button.sizePolicy().hasHeightForWidth())
        self.ocr_button.setSizePolicy(sizePolicy)
        self.ocr_button.setObjectName("ocr_button")
        self.ocr_button.setText("글자 추출")
        self.ocr_button.clicked.connect(self.ocr_button_clicked)
        self.horizontalLayout_1.addWidget(self.ocr_button)

        # search_button (QPushButton)   --> in horizontalLayout_1
        self.search_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_button.sizePolicy().hasHeightForWidth())
        self.search_button.setSizePolicy(sizePolicy)
        self.search_button.setObjectName("search_button")
        self.search_button.setText("검색")
        self.search_button.clicked.connect(self.search_button_clicked)
        self.horizontalLayout_1.addWidget(self.search_button)

        # raid_4_radiobutton (QRadioButton) --> in horizontalLayout_1
        self.raid_4_radiobutton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_1)
        self.raid_4_radiobutton.setObjectName("raid_4_radiobutton")
        self.raid_4_radiobutton.setText("4인 레이드")
        self.horizontalLayout_1.addWidget(self.raid_4_radiobutton)

        # raid_8_radiobutton (QRadioButton) --> in horizontalLayout_1
        self.raid_8_radiobutton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_1)
        self.raid_8_radiobutton.setObjectName("raid_8_radiobutton")
        self.raid_8_radiobutton.setText("8인 레이드")
        self.raid_8_radiobutton.setChecked(True)
        self.horizontalLayout_1.addWidget(self.raid_8_radiobutton)

        # raid_buttongroup (QButtonGroup) --> in horizontalLayout_1
        self.raid_buttongroup = QtWidgets.QButtonGroup(self.horizontalLayoutWidget_1)
        self.raid_buttongroup.setObjectName("raid_buttongroup")
        self.raid_buttongroup.addButton(self.raid_4_radiobutton)
        self.raid_buttongroup.addButton(self.raid_8_radiobutton)

        # verticalLayoutWidget_1
        self.verticalLayoutWidget_1 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_1.setGeometry(QtCore.QRect(20, 70, 760, 500))
        self.verticalLayoutWidget_1.setObjectName("verticalLayoutWidget_1")

        # verticalLayout_1 --> in verticalLayoutWidget_1
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_1)
        self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_1.setObjectName("verticalLayout_1")

        # horizontalLayout_2 --> in verticalLayout_1
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_1.addLayout(self.horizontalLayout_2)

        # gridLayout_1 --> in horizontalLayout_2
        self.gridLayout_1 = QtWidgets.QGridLayout()
        self.gridLayout_1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_1.setContentsMargins(10, 5, 10, 5)
        self.gridLayout_1.setSpacing(6)
        self.gridLayout_1.setObjectName("gridLayout_1")
        self.horizontalLayout_2.addLayout(self.gridLayout_1)

        # label_1 : 파티1 --> in gridLayout_1
        self.label_1 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.label_1.setText("1파티")
        self.gridLayout_1.addWidget(self.label_1, 0, 0, 1, 2)

        # label_1_1 : 1번 --> in gridLayout_1
        self.label_1_1 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1_1.sizePolicy().hasHeightForWidth())
        self.label_1_1.setSizePolicy(sizePolicy)
        self.label_1_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1_1.setObjectName("label_1_1")
        self.label_1_1.setText("1번")
        self.gridLayout_1.addWidget(self.label_1_1, 1, 0, 1, 1)

        # label_1_2 : 2번 --> in gridLayout_1
        self.label_1_2 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1_2.sizePolicy().hasHeightForWidth())
        self.label_1_2.setSizePolicy(sizePolicy)
        self.label_1_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1_2.setObjectName("label_1_2")
        self.label_1_2.setText("2번")
        self.gridLayout_1.addWidget(self.label_1_2, 2, 0, 1, 1)

        # label_1_3 : 3번 --> in gridLayout_1
        self.label_1_3 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1_3.sizePolicy().hasHeightForWidth())
        self.label_1_3.setSizePolicy(sizePolicy)
        self.label_1_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1_3.setObjectName("label_1_3")
        self.label_1_3.setText("3번")
        self.gridLayout_1.addWidget(self.label_1_3, 3, 0, 1, 1)

        # label_1_4 : 4번 --> in gridLayout_1
        self.label_1_4 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1_4.sizePolicy().hasHeightForWidth())
        self.label_1_4.setSizePolicy(sizePolicy)
        self.label_1_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1_4.setObjectName("label_1_4")
        self.label_1_4.setText("4번")
        self.gridLayout_1.addWidget(self.label_1_4, 4, 0, 1, 1)

        # party1_1_lineedit (QLineEdit) --> in gridLayout_1
        self.party1_1_lineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.party1_1_lineedit.sizePolicy().hasHeightForWidth())
        self.party1_1_lineedit.setSizePolicy(sizePolicy)
        self.party1_1_lineedit.setObjectName("party1_1_lineedit")
        self.gridLayout_1.addWidget(self.party1_1_lineedit, 1, 1, 1, 1)

        # party1_2_lineedit (QLineEdit) --> in gridLayout_1
        self.party1_2_lineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.party1_2_lineedit.sizePolicy().hasHeightForWidth())
        self.party1_2_lineedit.setSizePolicy(sizePolicy)
        self.party1_2_lineedit.setObjectName("party1_2_lineedit")
        self.gridLayout_1.addWidget(self.party1_2_lineedit, 2, 1, 1, 1)

        # party1_3_lineedit (QLineEdit) --> in gridLayout_1
        self.party1_3_lineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.party1_3_lineedit.sizePolicy().hasHeightForWidth())
        self.party1_3_lineedit.setSizePolicy(sizePolicy)
        self.party1_3_lineedit.setObjectName("party1_3_lineedit")
        self.gridLayout_1.addWidget(self.party1_3_lineedit, 3, 1, 1, 1)

        # party1_4_lineedit (QLineEdit) --> in gridLayout_1
        self.party1_4_lineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.party1_4_lineedit.sizePolicy().hasHeightForWidth())
        self.party1_4_lineedit.setSizePolicy(sizePolicy)
        self.party1_4_lineedit.setObjectName("party1_4_lineedit")
        self.gridLayout_1.addWidget(self.party1_4_lineedit, 4, 1, 1, 1)

        # spacerItem_1 --> in gridLayout_1
        spacerItem_1 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_1.addItem(spacerItem_1, 5, 1, 1, 1)

        # spacerItem_2 --> in horizontalLayout_2
        spacerItem_2 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem_2)

        # gridLayout_2 --> in horizontalLayout_2
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setContentsMargins(10, 5, 10, 5)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2.addLayout(self.gridLayout_2)

        # label_2 : 2파티 --> in gridLayout_2
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("2파티")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 2)

        # label_2_1 : 1번 --> in gridLayout_2
        self.label_2_1 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2_1.sizePolicy().hasHeightForWidth())
        self.label_2_1.setSizePolicy(sizePolicy)
        self.label_2_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2_1.setObjectName("label_2_1")
        self.label_2_1.setText("1번")
        self.gridLayout_2.addWidget(self.label_2_1, 1, 0, 1, 1)

        # label_2_2 : 2번 --> in gridLayout_2
        self.label_2_2 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2_2.sizePolicy().hasHeightForWidth())
        self.label_2_2.setSizePolicy(sizePolicy)
        self.label_2_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2_2.setObjectName("label_2_2")
        self.label_2_2.setText("2번")
        self.gridLayout_2.addWidget(self.label_2_2, 2, 0, 1, 1)

        # label_2_3 : 3번 --> in gridLayout_2
        self.label_2_3 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2_3.sizePolicy().hasHeightForWidth())
        self.label_2_3.setSizePolicy(sizePolicy)
        self.label_2_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2_3.setObjectName("label_2_3")
        self.label_2_3.setText("3번")
        self.gridLayout_2.addWidget(self.label_2_3, 3, 0, 1, 1)

        # label_2_4 : 4번 --> in gridLayout_2
        self.label_2_4 = QtWidgets.QLabel(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2_4.sizePolicy().hasHeightForWidth())
        self.label_2_4.setSizePolicy(sizePolicy)
        self.label_2_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2_4.setObjectName("label_2_4")
        self.label_2_4.setText("4번")
        self.gridLayout_2.addWidget(self.label_2_4, 4, 0, 1, 1)

        # party2_1_lineedit (QLineEdit) --> in gridLayout_2
        self.party2_1_lineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.party2_1_lineedit.sizePolicy().hasHeightForWidth())
        self.party2_1_lineedit.setSizePolicy(sizePolicy)
        self.party2_1_lineedit.setObjectName("party2_1_lineedit")
        self.gridLayout_2.addWidget(self.party2_1_lineedit, 1, 1, 1, 1)

        # party2_2_lineedit (QLineEdit) --> in gridLayout_2
        self.party2_2_lineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.party2_2_lineedit.sizePolicy().hasHeightForWidth())
        self.party2_2_lineedit.setSizePolicy(sizePolicy)
        self.party2_2_lineedit.setObjectName("party2_2_lineedit")
        self.gridLayout_2.addWidget(self.party2_2_lineedit, 2, 1, 1, 1)

        # party2_3_lineedit (QLineEdit) --> in gridLayout_2
        self.party2_3_lineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.party2_3_lineedit.sizePolicy().hasHeightForWidth())
        self.party2_3_lineedit.setSizePolicy(sizePolicy)
        self.party2_3_lineedit.setObjectName("party2_3_lineedit")
        self.gridLayout_2.addWidget(self.party2_3_lineedit, 3, 1, 1, 1)

        # party2_4_lineedit (QLineEdit) --> in gridLayout_2
        self.party2_4_lineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.party2_4_lineedit.sizePolicy().hasHeightForWidth())
        self.party2_4_lineedit.setSizePolicy(sizePolicy)
        self.party2_4_lineedit.setObjectName("party2_4_lineedit")
        self.gridLayout_2.addWidget(self.party2_4_lineedit, 4, 1, 1, 1)

        # spacerItem_3 --> in gridLayout_2
        spacerItem_3 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem_3, 5, 1, 1, 1)

        # horizontalLayout_3 --> in verticalLayout_1
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_1.addLayout(self.horizontalLayout_3)

        # tablewidget_pushbutton_list --> in horizontalLayout_3
        self.tablewidget_pushbutton_list = []
        for i in range(8):
            button = QtWidgets.QPushButton(self.verticalLayoutWidget_1)
            button.setObjectName(f"tablewidget_pushbutton_{i}")
            button.setText(f"{i+1}번")
            button.setEnabled(False)
            button.clicked.connect(self.tablewidget_pushbutton_clicked)
            self.horizontalLayout_3.addWidget(button)
            self.tablewidget_pushbutton_list.append(button)

        # tablewidget --> in verticalLayout_1
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setAutoScrollMargin(16)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["링크", "제목"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.itemDoubleClicked.connect(self.openLink)
        self.verticalLayout_1.addWidget(self.tableWidget)

        # etc
        self.captureTool = CaptureTool()
        self.ocrTool = OcrTool()

    def capture_button_clicked(self):
        logging.debug("capture_button_clicked")
        self.ocr_button.setEnabled(False)
        self.captureTool.capturePartyOne()
        if self.raid_8_radiobutton.isChecked():
            logging.debug("raid_8_radiobutton.isChecked")
            self.captureTool.capturePartyTwo()
        self.ocr_button.setEnabled(True)

    def ocr_button_clicked(self):
        logging.debug("ocr_button_clicked")
        self.ocr_button.setEnabled(False)
        partyOneThreshImageFilePathList = self.captureTool.getPartyOneThreshImageFilePath()
        partyOneOrignalImageFilePathList = self.captureTool.getPartyOneOriginalImageFilePath()
        for i in range(len(partyOneThreshImageFilePathList)):
            if self.ocrTool.ImageSearch(partyOneOrignalImageFilePathList[i]) is False:
                exec(f"self.party1_{i+1}_lineedit.setText(self.ocrTool.ocr(partyOneThreshImageFilePathList[{i}]))")
        if self.raid_8_radiobutton.isChecked():
            logging.debug("raid_8_radiobutton.isChecked")
            partyTwoThreshImageFilePathList = self.captureTool.getPartyTwoThreshImageFilePath()
            partyTwoOriginalImageFilePathList = self.captureTool.getPartyTwoOriginalImageFilePath()
            for i in range(len(partyTwoThreshImageFilePathList)):
                if self.ocrTool.ImageSearch(partyTwoOriginalImageFilePathList[i]) is False:
                    exec(f"self.party2_{i+1}_lineedit.setText(self.ocrTool.ocr(partyTwoThreshImageFilePathList[{i}]))")
        self.ocr_button.setEnabled(True)

    def search_button_clicked(self):
        logging.debug("search_button_clicked()")
        logging.info("검색 시작")
        self.search_button.setEnabled(False)
        self.tnrzh_list = {}
        search_list = []
        for i in range(4):
            exec(f"search_list.append(self.party1_{i+1}_lineedit.text())")
            exec(f"search_list.append(self.party2_{i+1}_lineedit.text())")
        for button in self.tablewidget_pushbutton_list:
            button.setEnabled(False)
        self.search_signal.emit(search_list)

    def tablewidget_add_item(self, ls):     # ls: [[link1, title1], [link2, title2], ...]
        for post in ls:
            rowIndex = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowIndex)
            link_item = QtWidgets.QTableWidgetItem(post[0])
            link_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowIndex, 0, link_item)
            title_item = QtWidgets.QTableWidgetItem(post[1])
            title_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowIndex, 1, title_item)

    @QtCore.pyqtSlot(tuple)
    def getTnrzhList(self, tnrzh):
        self.tnrzh_list[tnrzh[0]] = tnrzh[1]
        if len(self.tnrzh_list) == 8:
            logging.info("검색 완료")
            logging.debug(f"self.tnrzh_list: {self.tnrzh_list}")
            self.search_button.setEnabled(True)
            count = 0
            for i in range(1, 9):
                if len(self.tnrzh_list[i]) != 0:
                    logging.info(f"{i}번 게시글 검색됨")
                    count += 1
                    self.tablewidget_pushbutton_list[i-1].setEnabled(True)
            if count == 0:
                logging.info("안전한 공대")

    def tablewidget_pushbutton_clicked(self):
        logging.debug("tablewidget_pushbutton_clicked()")
        sender_idx = int(self.sender().text()[0])
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tablewidget_add_item(self.tnrzh_list[sender_idx])

    def openLink(self, item):
        if item.column() == 0:
            webbrowser.open(item.text())

    def settings_button_clicked(self):
        self.settings_window.exec_()


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.config = configparser.ConfigParser()
        self.config.read("./settings.ini")
        self.ApiKey = self.config['api']['jwt']
        self.search_post_number = self.config['api']['search_post_number']

        self.setWindowIcon(QtGui.QIcon('./image/icon.ico'))
        self.setWindowTitle('설정')
        self.setFixedSize(400, 300)
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(12)
        self.setFont(font)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 90, 70, 30))
        self.label.setText("API Key : ")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 140, 120, 30))
        self.label_2.setText("검색 게시글 수 : ")

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(200, 140, 60, 30))
        self.label_3.setText("만 까지")

        self.quit_button = QtWidgets.QPushButton(self)
        self.quit_button.setGeometry(QtCore.QRect(300, 250, 80, 30))
        self.quit_button.setText("닫기")
        self.quit_button.clicked.connect(self.quit_button_clicked)

        self.apiKey_lineedit = QtWidgets.QLineEdit(self)
        self.apiKey_lineedit.setGeometry(QtCore.QRect(90, 90, 290, 30))
        self.apiKey_lineedit.setText(self.ApiKey)

        self.search_post_number_lineedit = QtWidgets.QLineEdit(self)
        self.search_post_number_lineedit.setGeometry(QtCore.QRect(150, 140, 40, 30))
        self.search_post_number_lineedit.setValidator(QtGui.QIntValidator(2, 10, self))
        self.search_post_number_lineedit.setText(self.search_post_number)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.quit_button_clicked()

    def quit_button_clicked(self):
        self.config['api']['jwt'] = self.apiKey_lineedit.text()
        self.config['api']['search_post_number'] = self.search_post_number_lineedit.text()
        with open("./settings.ini", "w+") as f:
            self.config.write(f)
        self.accept()





























































