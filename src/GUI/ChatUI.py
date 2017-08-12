from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit, QWidget, QHBoxLayout, QVBoxLayout
from ChatScreen import ChatScreen
from PyQt5.QtCore import Qt

class ChatUI(QWidget):
    def __init__(self, parent):
        super(ChatUI, self).__init__(parent)
        self.centralWidget = parent
        layout = QHBoxLayout()
        chatScreen = ChatScreen(self)
        self.chatScreen = chatScreen
        layout.addWidget(chatScreen)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)
