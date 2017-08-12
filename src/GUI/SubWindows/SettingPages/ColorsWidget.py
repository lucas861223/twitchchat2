from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QGroupBox


class ColorsWidget(QWidget):
    def __init__(self, settingDialog):
        super(ColorsWidget, self).__init__(settingDialog)
        self.isChanged = False
        self.settingDialog = settingDialog

        layout = QVBoxLayout()

        groupBox = QGroupBox(self)
        groupBox.setTitle("Customize Colors")
        layout.addWidget(groupBox)

        self.setLayout(layout)

    def saveSetting(self):
        print("what")
        pass