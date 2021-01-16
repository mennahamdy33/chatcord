import sys
import socket
import errno
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QApplication
from LoginForm import Ui_Form
from ChatRoom import Ui_ChatForm
from First import Ui_FirstForm
from Questions import Ui_QuestionForm
import time
IP = "127.0.0.1"
PORT = 1234
HEADERSIZE= 10
# start connection 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))


class FirstForm(QDialog):
    def __init__(self):
        super(FirstForm, self).__init__()
        # call FirstForm UI
        self.ui = Ui_FirstForm()
        self.ui.setupUi(self)
        # connect Patient Button to questions function
        self.ui.PatientButton.clicked.connect(self.questions)
        # connect Doctor Button To login Function 
        self.ui.DoctorButton.clicked.connect(self.login)
    def login(self):
        # call loginWindow Class
        Login = loginWindow()
        widget.addWidget(Login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def questions(self):
        # call question Class
        Questions = questionsWindow()
        widget.addWidget(Questions)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class questionsWindow(QDialog):
    def __init__(self):
        super(questionsWindow, self).__init__()
        # get the QuestionForm UI
        self.ui = Ui_QuestionForm()
        self.ui.setupUi(self)
        # connect Result button with model Function
        self.ui.Result.clicked.connect(self.model)
        # connect TalkToDoctor button to Patient Info Function 
        self.ui.TalkToDoctor.clicked.connect(self.patientInfo)
        self.ui.Done.clicked.connect(self.done)

    def done(self):
        client_socket.close()
        sys.exit()
    def model(self):
        # get data from User Interface
        data = {
            'name': self.ui.NameText.text()
            , 'age': self.ui.AgeText.text()
            , 'bp': self.ui.BloodPressureText.text()
            , 'bgr': self.ui.GlucoseText.text()
            , 'bu': self.ui.BloodUreaText.text()
            , 'sc': self.ui.SerumText.text()
            , 'hemo': self.ui.HemoglobinText.text()
            , 'htn': self.IsCheckBoxChecked(self.ui.Hypertension)
            , 'dm': self.IsCheckBoxChecked(self.ui.Diabetes)
            , 'cad': self.IsCheckBoxChecked(self.ui.Coronary)
            , 'appet': self.ui.comboBox_3.currentIndex() - 1
            , 'ane': self.IsCheckBoxChecked(self.ui.Anemia)
            , 'al': self.ui.AlbuminComboBox.currentIndex() - 1
            , 'su': self.ui.SugarComboBox.currentIndex() - 1
            , 'ba': self.IsCheckBoxChecked(self.ui.Bacteria)
        }
        data = str(data)
        # encode the msg
        msg = data.encode('utf-8')
        # set header
        message_header = f"{len(msg):<{HEADERSIZE}}".encode('utf-8')
        # send data to the server
        client_socket.send(message_header + msg)
        # call Result Function 
        self.result()

    def result(self):
       # get Result from Server after applying the RanhomForest Model
        message_header = client_socket.recv(HEADERSIZE)
        message_length = int(message_header.decode('utf-8').strip())
        message = client_socket.recv(message_length).decode('utf-8')
        # Show Result To the User 
        self.ui.ResultText.setText(message)

    def IsCheckBoxChecked(self,checkBox):
        # Because the IsChecked return False and True and we need the data to be integar to enter the model without cause any kind of errors
        # so we assign the int values manually
        if (checkBox.isChecked()):
            return(1)
        else:
            return(0)
    
    def patientInfo(self):
        # Get User Name
        name = self.ui.NameText.text()
        # Call Chat Function 
        chat(name)

class loginWindow(QDialog):
    def __init__(self):
        super(loginWindow, self).__init__()
        # call UI of the Login Form 
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        # connect Next Button with doctorInfo Function
        self.ui.NextButton.clicked.connect(self.doctorInfo)
        
    def doctorInfo(self):
        # take the information from UI and Save it
        userName = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        # then go to Chat Function
        chat(userName)

class chatwindow(QDialog):
    def __init__(self,username):
        super(chatwindow, self).__init__()
        # get the UI of Chat Form
        self.ui = Ui_ChatForm()
        self.ui.setupUi(self)
        self.username = username
        self.HEADER_LENGTH = 10
        #connect Send Button to send function
        self.ui.SendButton.clicked.connect(self.send)
        self.message = ''
        client_socket.setblocking(False)
        # use timer to check if there is any new message or no
        timer = QTimer(self)
        # after 1 sec go to function receive
        timer.timeout.connect(self.receive)
        timer.start(1000)
        # we want to send the user name only at the start of the chat
        # so we encode it 
        self.myusername = self.username.encode('utf-8')
        # encode header
        self.username_header = f"{len(self.myusername):<{self.HEADER_LENGTH}}".encode('utf-8')
        # sent it to server 
        client_socket.send(self.username_header + self.myusername)
        # set the user name at the top of the chat
        self.ui.Name.setText(self.username)

    def send(self):
        # get message 
        self.message = self.ui.message.text()
        # add username at the label on the top of the chat 
        self.ui.Chat.addItem(self.username + ': ' + self.message)
        # if there is a message to send
        if self.message:
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            self.mymessage = self.message.encode('utf-8')
            self.message_header = f"{len(self.mymessage):<{self.HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(self.message_header + self.mymessage)
        # clear the message text box after sending it through the server 
        self.ui.message.clear()

    def receive(self):
        try:
            username_header = client_socket.recv(self.HEADER_LENGTH)
            # If we received no data, server gracefully closed a connection.
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            # if there is any new msg so send to the server get username of the client who sent the msg and get msg data 
            # we have to decode the data 
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            message_header = client_socket.recv(self.HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            # write in the chat the received username and msg 
            self.ui.Chat.addItem(f'{username}: {message}')

        except IOError as e:
            # This is normal on non blocking connections - when there
            # are no incoming data, error is going to be raised
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
    # call ChatWindow Class
    Chat = chatwindow(username)
    widget.addWidget(Chat)
    widget.setCurrentIndex(widget.currentIndex() + 1)



app = QApplication(sys.argv)
# Start by calling FirstForm Class 
mainwindow = FirstForm()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
app.exec_()



