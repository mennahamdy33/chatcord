from PyQt5.QtWidgets import *
app = QApplication([])
layout = QVBoxLayout()
layout.addWidget(QTextEdit())
layout.addWidget(QLineEdit())
window = QWidget()
window.setLayout(layout)
window.show()
app.exec_()