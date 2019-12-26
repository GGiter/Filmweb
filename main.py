from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os
from LoginDialog import LoginDialog , RegisterDialog
from database import Database

db = None

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.interface()
    
    def interface(self):

        label1 = QLabel('New movies:', self)

        layout = QGridLayout()
        layout.addWidget(label1,1,1)

        layoutH = QHBoxLayout()

        loginBtn = QPushButton("&Login", self)
        loginBtn.clicked.connect(self.login)
        registerBtn = QPushButton("&Register", self)
        registerBtn.clicked.connect(self.register)

        layoutH.addWidget(loginBtn)
        layoutH.addWidget(registerBtn)

        layout.addLayout(layoutH,2,0,1,3)

        self.setLayout(layout)

        self.setGeometry(3,3,300,100)
        self.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__)) + '/movie.png'))
        self.setWindowTitle('Filmweb')
        self.show()

    
    def closeEvent(self, event):

        answer = QMessageBox.question(self, 'Warning',"Do you really want to leave?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
        if answer == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


    def login(self):
        login, password, ok = LoginDialog.getLoginPassword(self)
        if not ok:
            return

        if not login or not password:
            QMessageBox.warning(self, 'Error',
                                'Empty login or password!', QMessageBox.Ok)
            return

        if not db.loginUser(login,password):
            QMessageBox.warning(self, 'Error',
                                'Wrong login or password!', QMessageBox.Ok)
            return

        QMessageBox.information(self,
            'Information:','Logged succesfully!', QMessageBox.Ok)

    def register(self):
        login, email, password, ok = RegisterDialog.getLoginPassword(self)
        if not ok:
            return

        if not login or not password or not email:
            QMessageBox.warning(self, 'Error',
                                'Empty login or email or password!', QMessageBox.Ok)
            return

        db.registerUser(login,email,password)

        QMessageBox.information(self,
            'Information', 'Registered succesfully !', QMessageBox.Ok)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    db = Database('filmweb.db')
    main_window = MainWindow()
    sys.exit(app.exec_())