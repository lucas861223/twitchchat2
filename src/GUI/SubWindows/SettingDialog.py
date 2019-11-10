from PyQt5.QtWidgets import QDialog, QHBoxLayout, QStackedLayout, QListWidget, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from GUI.SubWindows.SettingPages.ColorsWidget import ColorsWidget
from GUI.SubWindows.SettingPages.MainWidget import MainWidget
from GUI.SubWindows.SettingPages.MacrosWidget import MacrosWidget
from GUI.SubWindows.SettingPages.NotificationWidget import  NotificationWidget

class SettingDialog(QDialog):
    def __init__(self, mainWindow):
        super(SettingDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.mainWindow = mainWindow
        self.setWindowTitle('Settings')
        position = self.mainWindow.getPopUpPosition(600, 510)
        self.setGeometry(position.x(), position.y(), 600, 510)
        self.setFixedHeight(510)
        self.setFixedWidth(600)
        verticalLayout = QVBoxLayout()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.settingList = QListWidget()
        layout.addWidget(self.settingList, 1)
        settingContent = QWidget(self)
        self.layout = QStackedLayout()
        settingContent.setLayout(self.layout)
        self.setUpPages()
        self.settingList.itemSelectionChanged.connect(self.switchSettingPage)

        horizontalButtonLayout = QHBoxLayout()
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)
        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveAll)
        horizontalButtonLayout.addWidget(saveButton)
        horizontalButtonLayout.addWidget(cancelButton)

        verticalLayout.addLayout(layout)
        verticalLayout.addLayout(horizontalButtonLayout)
        layout.addWidget(settingContent, 9)
        self.setLayout(verticalLayout)
        self.exec()

    def setUpPages(self):
        self.settingList.addItem("Main")
        self.layout.addWidget(MainWidget(self))
        self.settingList.addItem("Colors")
        self.layout.addWidget(ColorsWidget(self))
        self.settingList.addItem("Macros")
        self.layout.addWidget(MacrosWidget(self))
        self.settingList.addItem("Notification")
        self.layout.addWidget(NotificationWidget(self))


    def switchSettingPage(self):
        self.layout.setCurrentIndex(self.settingList.currentRow())

    def saveAll(self):
        for i in range(self.layout.count()-1, -1, -1):
            self.layout.widget(i).saveSetting()
        self.accept()