import sys
import socket
import select
import errno
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QApplication
from LoginForm import Ui_Form
from ChatRoom import Ui_ChatForm
from First import Ui_FirstForm
from Questions import Ui_QuestionForm
import pickle
import time
IP = "127.0.0.1"
PORT = 1234
HEADERSIZE= 10
class FirstForm(QDialog):
    def __init__(self):
        super(FirstForm, self).__init__()
        self.ui = Ui_FirstForm()
        self.ui.setupUi(self)
        self.ui.PatientButton.clicked.connect(self.questions)
        self.ui.DoctorButton.clicked.connect(self.login)
    def login(self):
        Login = loginWindow()
        widget.addWidget(Login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def questions(self):
        Questions = questionsWindow()
        widget.addWidget(Questions)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class questionsWindow(QDialog):
    def __init__(self):
        super(questionsWindow, self).__init__()
        self.ui = Ui_QuestionForm()
        self.ui.setupUi(self)
        self.ui.Result.clicked.connect(self.model)
        self.ui.TalkToDoctor.clicked.connect(self.patientInfo)
        self.ui.Done.clicked.connect(app.quit)

    def model(self):
        data = {'age': self.ui.AgeText.text()
                ,'bu': self.ui.BloodUreaText.text()
                ,'bgr': self.ui.GlucoseText.text()
                ,'sc': self.ui.SerumText.text()
                ,'bp': self.ui.BloodPressureText.text()
                ,'hemo': self.ui.HemoglobinText.text()
                ,'htn':self.IsCheckBoxChecked(self.ui.Hypertension)
                ,'dm':self.IsCheckBoxChecked(self.ui.Diabetes)
                ,'cad':self.IsCheckBoxChecked(self.ui.Coronary)
                ,'appet':self.ui.comboBox_3.currentIndex()-1
                ,'ane':self.IsCheckBoxChecked(self.ui.Anemia)
                ,'al':self.ui.AlbuminComboBox.currentIndex()-1
                ,'su':self.ui.SugarComboBox.currentIndex()-1
                ,'ba':self.IsCheckBoxChecked(self.ui.Bacteria)
                }
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((IP, PORT))
        msg = pickle.dumps(data)      
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
        self.clientsocket.send(msg)
        time.sleep(5)
        self.result()

    def result(self):
        # username_header = self.clientsocket.recv(HEADERSIZE)
        # # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        # if not len(username_header):
        #     print('Connection closed by the server')
        #     sys.exit()
       
        message_header = self.clientsocket.recv(HEADERSIZE)
        message_length = int(message_header.decode('utf-8').strip())
        message = self.clientsocket.recv(message_length).decode('utf-8')
        print(message)
        self.ui.ResultText.setText(message)

    def IsCheckBoxChecked(self,checkBox):
        if (checkBox.isChecked()):
            return(1)
        else:
            return(0)
    
    def patientInfo(self):
        name = self.ui.NameText.text()
        chat(name)

class loginWindow(QDialog):
    def __init__(self):
        super(loginWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.NextButton.clicked.connect(self.doctorInfo)
        
    def doctorInfo(self):
        userName = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        print(userName,password)
        chat(userName)

class chatwindow(QDialog):
    def __init__(self,username):
        super(chatwindow, self).__init__()
        self.ui = Ui_ChatForm()
        self.ui.setupUi(self)
        self.username = username
        self.HEADER_LENGTH = 10
        self.ui.SendButton.clicked.connect(self.send)
        self.message = ''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))
        self.client_socket.setblocking(False)
        timer = QTimer(self)
        timer.timeout.connect(self.receive)
        timer.start(1000)
        self.myusername = self.username.encode('utf-8')
        self.username_header = f"{len(self.myusername):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(self.username_header + self.myusername)

    def send(self):

        self.message = self.ui.message.text()
        self.ui.Chat.addItem(self.username + ': ' + self.message)

        if self.message:
            print(type(self.message))
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            self.mymessage = self.message.encode('utf-8')
            self.message_header = f"{len(self.mymessage):<{self.HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(self.message_header + self.mymessage)
        self.ui.message.clear()

    def receive(self):
        try:

            print('hola')
            username_header = self.client_socket.recv(self.HEADER_LENGTH)
            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = self.client_socket.recv(username_length).decode('utf-8')
            message_header = self.client_socket.recv(self.HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = self.client_socket.recv(message_length).decode('utf-8')
            self.ui.Chat.addItem(f'{username}: {message}')

        except IOError as e:
            # This is normal on non blocking connections - when there
            # are no incoming data, error is going to be raised
            # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
            # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
            # If we got different error code - something happened
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(e)))
            sys.exit()


def chat(username):
    Chat = chatwindow(username)
    widget.addWidget(Chat)
    widget.setCurrentIndex(widget.currentIndex() + 1)



app = QApplication(sys.argv)
mainwindow = FirstForm()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
app.exec_()
