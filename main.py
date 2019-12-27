from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox , QScrollArea , QGroupBox , QFormLayout 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os
from LoginDialog import LoginDialog , RegisterDialog
from database import Database

db = None
current_user = None

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.interface()
    
    def interface(self):

        label1 = QLabel('New movies:', self)

        self.layout = QGridLayout()
        self.layout.addWidget(label1,1,0)

        self.scroll()

        layoutH = QHBoxLayout()

        self.loginBtn = QPushButton("&Login", self)
        self.loginBtn.clicked.connect(self.login)
        self.registerBtn = QPushButton("&Register", self)
        self.registerBtn.clicked.connect(self.register)
        self.logoutBtn = QPushButton("&Logout",self)
        self.logoutBtn.hide()
        self.logoutBtn.clicked.connect(self.logout)

        layoutH.addWidget(self.loginBtn)
        layoutH.addWidget(self.registerBtn)
        layoutH.addWidget(self.logoutBtn)

        self.layout.addLayout(layoutH,2,0,1,3)

        self.setLayout(self.layout)

        self.setGeometry(20,20,500,500)
        self.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__)) + '/movie.png'))
        self.setWindowTitle('Filmweb')
        self.show()

    def scroll(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()

        title_labels = []
        buttons = []

        for movie in db.getMovies():
            box_layout = QHBoxLayout()
            title_label = QLabel(movie.get_title())
            avg_rate_label = QLabel(str(movie.get_avg_rate()))
            button = QPushButton("&Rate", self)
            button.clicked.connect(lambda: self.rateMovie(movie,avg_rate_label ))
            box_layout.addWidget(title_label)
            box_layout.addWidget(avg_rate_label)
            box_layout.addWidget(button)
            myform.addRow(box_layout)
            title_labels.append(title_label)    
            buttons.append(button)
        
        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True) 
        scroll.setFixedHeight(200)
        self.layout.addWidget(scroll,1,1)


    def rateMovie(self,movie,label):
        movie.rate(5,current_user)
        label.setText(str(movie.get_avg_rate()))

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

        current_user = db.loginUser(login,password)

        if  current_user is None:
            QMessageBox.warning(self, 'Error',
                                'Wrong login or password!', QMessageBox.Ok)
            return

        QMessageBox.information(self,
            'Information:','Logged succesfully!', QMessageBox.Ok)

        self.loginBtn.hide()
        self.registerBtn.hide()
        self.logoutBtn.show()

    def register(self):
        login, email, password, ok = RegisterDialog.getLoginPassword(self)
        if not ok:
            return

        if not login or not password or not email:
            QMessageBox.warning(self, 'Error',
                                'Empty login or email or password!', QMessageBox.Ok)
            return

        current_user = db.registerUser(login,email,password)

        QMessageBox.information(self,
            'Information', 'Registered succesfully !', QMessageBox.Ok)


        self.loginBtn.hide()
        self.registerBtn.hide()
        self.logoutBtn.show()

    def logout(self):
        current_user = None

        self.loginBtn.show()
        self.registerBtn.show()
        self.logoutBtn.hide()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    db = Database('filmweb.db')
    main_window = MainWindow()
    sys.exit(app.exec_())