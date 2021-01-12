import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from LoginForm import Ui_Form
from ChatRoom import Ui_ChatForm
from First import Ui_First
class First(QDialog):
    def __init__(self):
        super(First, self).__init__()
        self.ui = Ui_First()
        self.ui.setupUi(self)
        #self.ui.PatientButton.clicked.connect(self.login)
        self.ui.DoctorButton.clicked.connect(self.login)
    def login(self):
        Login = loginWindow()
        widget.addWidget(Login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
class loginWindow(QDialog):
    def __init__(self):
        super(loginWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.NextButton.clicked.connect(self.chat)

    def chat(self):
        Chat = chatwindow()
        widget.addWidget(Chat)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class chatwindow(QDialog):
    def __init__(self):
        super(chatwindow, self).__init__()
        self.ui = Ui_ChatForm()
        self.ui.setupUi(self)



app = QApplication(sys.argv)
mainwindow = First()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
app.exec_()
