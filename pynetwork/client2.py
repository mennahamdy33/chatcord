import sys
import socket
import select
import errno


from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt,QTimer
from GUI import Ui_MainWindow

IP = "127.0.0.1"
PORT = 1234

class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pen = (145, 0, 145)
        self.ui.lineEdit.setText('Username: ')
        self.username =''
        self.HEADER_LENGTH = 10
        self.ui.pushButton.clicked.connect(self.send)
        self.message = ''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))
        self.client_socket.setblocking(False)
        timer = QTimer(self)
        timer.timeout.connect(self.receive)
        timer.start(1000)

    def send(self):
        self.message = self.ui.lineEdit.text()
        print('menna')
        print(type(self.message))
        if self.username == '' :
            self.message = self.ui.lineEdit.text().replace('Username: ','')
            print('yarab ')
            print( type(self.message))
            self.username = self.message
            print(self.username)
            self.myusername = self.username.encode('utf-8')
            self.username_header = f"{len(self.myusername):<{self.HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(self.username_header + self.myusername)

        else:

            self.ui.listWidget.addItem(self.username + ': ' + self.message)
            if self.message:
                print(type(self.message))
                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                self.mymessage = self.message.encode('utf-8')
                self.message_header = f"{len(self.mymessage):<{self.HEADER_LENGTH}}".encode('utf-8')
                self.client_socket.send(self.message_header + self.mymessage)
        self.ui.lineEdit.clear()

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

            self.ui.listWidget.addItem(f'{username}: {message}')

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





def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
