from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QGroupBox, QGridLayout, QListWidget
from PyQt5.QtGui import QFont

class MacrosWidget(QWidget):
    def __init__(self, settingDialog):
        super(MacrosWidget, self).__init__(settingDialog)
        self.settingDialog = settingDialog
        self.isChanged = False
        layout = QGridLayout()
        file = open('setting/MacrosSetting', 'r')
        self.customMacros = QListWidget(self)
        self.loadMacros()
        layout.addWidget(self.customMacros)

        self.setLayout(layout)
        file.close()

    def loadMacros(self):
        pass

    def saveSetting(self):
        if self.isChanged:
            file = open('setting/MacrosSetting', 'w')
            file.truncate()
            file.close()