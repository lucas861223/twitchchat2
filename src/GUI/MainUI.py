from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MyStockratios(object):

    def setupUi(self, MyStockratios):
        MyStockratios.setObjectName("MyStockratios")
        MyStockratios.resize(950, 529)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MyStockratios.sizePolicy().hasHeightForWidth())
        MyStockratios.setSizePolicy(sizePolicy)
        MyStockratios.setMinimumSize(QtCore.QSize(800, 0))
        MyStockratios.setMaximumSize(QtCore.QSize(950, 529))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        MyStockratios.setFont(font)
        MyStockratios.setStyleSheet("QMainWindow#MyStockratios {\n"
"        \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0.44335 rgba(31, 38, 66, 255), stop:0.629139 rgba(29, 43, 66, 255));\n"
"    background-image: url(:/BG.png)\n"
"}\n"
"")
        MyStockratios.setIconSize(QtCore.QSize(300, 300))
        self.centralwidget = QtWidgets.QWidget(MyStockratios)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 130))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setItalic(False)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(90)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(500, 100))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro")
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(239, 239, 239);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/Title.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.frame)
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem, 0, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem1, 0, 0, 1, 1)
        self.ticker2_label = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(16)
        self.ticker2_label.setFont(font)
        self.ticker2_label.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.ticker2_label.setAutoFillBackground(False)
        self.ticker2_label.setStyleSheet("QLineEdit#ticker2_label {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0.44335 rgba(31, 38, 66, 0));\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"")
        self.ticker2_label.setObjectName("ticker2_label")
        self.gridLayout_13.addWidget(self.ticker2_label, 0, 3, 1, 1)
        self.ticker1_label = QtWidgets.QLineEdit(self.centralwidget)
        self.ticker1_label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(16)
        self.ticker1_label.setFont(font)
        self.ticker1_label.setStyleSheet("QLineEdit#ticker1_label {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0.44335 rgba(31, 38, 66, 0));\n"
"    border: none;\n"
"}\n"
"\n"
"QLineEdit#ticker1_label:focus {\n"
"    outline: none !important;\n"
"}\n"
"\n"
"")
        self.ticker1_label.setObjectName("ticker1_label")
        self.gridLayout_13.addWidget(self.ticker1_label, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem2, 0, 2, 1, 1)
        self.line_ticker1 = QtWidgets.QFrame(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.line_ticker1.setPalette(palette)
        self.line_ticker1.setStyleSheet("")
        self.line_ticker1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_ticker1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_ticker1.setObjectName("line_ticker1")
        self.gridLayout_13.addWidget(self.line_ticker1, 1, 1, 1, 1)
        self.line_ticker2 = QtWidgets.QFrame(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 90))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 90))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 90))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 90))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 90))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 90))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.line_ticker2.setPalette(palette)
        self.line_ticker2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_ticker2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_ticker2.setObjectName("line_ticker2")
        self.gridLayout_13.addWidget(self.line_ticker2, 1, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_13)
        spacerItem3 = QtWidgets.QSpacerItem(80, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.show_me_btn = QtWidgets.QPushButton(self.centralwidget)
        self.show_me_btn.setMinimumSize(QtCore.QSize(172, 0))
        self.show_me_btn.setMaximumSize(QtCore.QSize(175, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.show_me_btn.setFont(font)
        self.show_me_btn.setAutoFillBackground(False)
        self.show_me_btn.setStyleSheet("QPushButton {\n"
"\n"
"        \n"
"    background-color: rgb(40, 230, 168);\n"
"    border-radius: 10px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover {    \n"
"    \n"
"    background-color: rgb(145, 230, 186);\n"
"}\n"
"\n"
"QPushButton:pressed {    \n"
"    \n"
"    \n"
"    \n"
"    background-color: rgb(113, 123, 159);\n"
"}\n"
"")
        self.show_me_btn.setObjectName("show_me_btn")
        self.gridLayout.addWidget(self.show_me_btn, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem4)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("QTabBar::tab {\n"
"    \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    \n"
"    background-color: rgb(99, 110, 176);\n"
"    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    min-width: 25ex;\n"
"    padding: 12px;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    \n"
"    background-color: rgb(122, 132, 160);\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}")
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_balance_sheet = QtWidgets.QWidget()
        self.tab_balance_sheet.setObjectName("tab_balance_sheet")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_balance_sheet)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab_balance_sheet)
        font = QtGui.QFont()
        font.setFamily("Myriad Pro")
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("color: rgb(255, 255, 255);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_working_capital_avg_ticker1 = QtWidgets.QLabel(self.groupBox)
        self.label_working_capital_avg_ticker1.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.label_working_capital_avg_ticker1.setPalette(palette)
        self.label_working_capital_avg_ticker1.setObjectName("label_working_capital_avg_ticker1")
        self.gridLayout_3.addWidget(self.label_working_capital_avg_ticker1, 0, 1, 1, 1)
        self.label_working_capital = QtWidgets.QLabel(self.groupBox)
        self.label_working_capital.setMinimumSize(QtCore.QSize(200, 0))
        self.label_working_capital.setMaximumSize(QtCore.QSize(320, 16777215))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro")
        font.setPointSize(15)
        self.label_working_capital.setFont(font)
        self.label_working_capital.setStatusTip("")
        self.label_working_capital.setStyleSheet("color: rgb(214, 215, 214);")

        self.label_working_capital.setPixmap(QtGui.QPixmap(":/working_cap.png"))
        self.label_working_capital.setObjectName("label_working_capital")
        self.gridLayout_3.addWidget(self.label_working_capital, 0, 0, 1, 1)
        self.label_working_capital_avg_ticker2 = QtWidgets.QLabel(self.groupBox)
        self.label_working_capital_avg_ticker2.setEnabled(True)
        self.label_working_capital_avg_ticker2.setObjectName("label_working_capital_avg_ticker2")
        self.gridLayout_3.addWidget(self.label_working_capital_avg_ticker2, 0, 2, 1, 1)
        self.working_capital_button = QtWidgets.QPushButton(self.groupBox)
        self.working_capital_button.setEnabled(False)
        self.working_capital_button.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.working_capital_button.setFont(font)
        self.working_capital_button.setStyleSheet("QPushButton#working_capital_button {\n"
"\n"
"    color: rgb(255, 255, 255);        \n"
"    background-color: rgb(40, 230, 168);\n"
"    border-radius: 10px;\n"
"    min-width: 5em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton#working_capital_button:hover {    \n"
"    \n"
"    \n"
"    background-color: rgb(145, 230, 186);\n"
"}\n"
"\n"
"QPushButton#working_capital_button:pressed {    \n"
"    \n"
"        background-color: rgb(113, 123, 159);\n"
"\n"
"}\n"
"\n"
"QPushButton#working_capital_button:disabled {\n"
"    \n"
"                    \n"
"    background-color: rgba(255, 255, 255, 176);\n"
"}")
        self.working_capital_button.setObjectName("working_capital_button")
        self.gridLayout_3.addWidget(self.working_capital_button, 0, 3, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_3)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_balance_sheet, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addWidget(self.label_working_capital_avg_ticker1)
        self.horizontalLayout_2.addWidget(self.label_working_capital_avg_ticker2)
        MyStockratios.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MyStockratios)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 950, 22))
        self.menubar.setObjectName("menubar")
        MyStockratios.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MyStockratios)
        self.statusbar.setObjectName("statusbar")
        MyStockratios.setStatusBar(self.statusbar)

        self.retranslateUi(MyStockratios)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MyStockratios)
        MyStockratios.setTabOrder(self.ticker1_label, self.ticker2_label)
        MyStockratios.setTabOrder(self.ticker2_label, self.show_me_btn)
        MyStockratios.setTabOrder(self.show_me_btn, self.working_capital_button)
        MyStockratios.setTabOrder(self.working_capital_button, self.tabWidget)

    def retranslateUi(self, MyStockratios):
        _translate = QtCore.QCoreApplication.translate
        MyStockratios.setWindowTitle(_translate("MyStockratios", "My Stock Ratios"))
        self.ticker2_label.setPlaceholderText(_translate("MyStockratios", "Enter 2nd ticker here"))
        self.ticker1_label.setPlaceholderText(_translate("MyStockratios", "Enter 1st ticker here"))
        self.show_me_btn.setStatusTip(_translate("MyStockratios", "Show averages for the last ten years"))
        self.show_me_btn.setText(_translate("MyStockratios", "Go!"))
        self.show_me_btn.setShortcut(_translate("MyStockratios", "Return"))
        self.label_working_capital_avg_ticker1.setText(_translate("MyStockratios", "N/A"))
        self.label_working_capital.setToolTip(_translate("MyStockratios", "The <b>Working Capital</b> indicates whether a company has enough short term assets to cover its short term debt. Anything below 1 indicates negative W/C (working capital). While anything over 2 means that the company is not investing excess assets.<br><br>Working Capital = Current Assets - Current Liabilities<br><br><i>Source:  www.investopedia.com</i>"))
        self.label_working_capital.setText(_translate("MyStockratios", "Working Capital"))
        self.label_working_capital_avg_ticker2.setText(_translate("MyStockratios", "N/A"))
        self.working_capital_button.setStatusTip(_translate("MyStockratios", "Show graph for Working Capital ratio"))
        self.working_capital_button.setText(_translate("MyStockratios", "See Graph"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_balance_sheet), _translate("MyStockratios", "Balance sheet ratios"))