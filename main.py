from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox , QScrollArea , QGroupBox , QFormLayout 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os
from LoginDialog import LoginDialog , RegisterDialog
from database import Database
from rateDialog import RateDialog
from detailsDialog import DetailsDialog

db = None


class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.current_user = None
        self.interface()
    
    def interface(self):

        label1 = QLabel('New movies:', self)

        self.layout = QGridLayout()
        self.layout.addWidget(label1,1,0)

        self.show_latest()

        layoutMovieH = QHBoxLayout()

        latestBtn = QPushButton("&Latest",self)
        latestBtn.clicked.connect(self.show_latest)
        recommendationsBtn = QPushButton("&Recommendations",self)
        recommendationsBtn.clicked.connect(self.show_recommendations)

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

        layoutMovieH.addWidget(latestBtn)
        layoutMovieH.addWidget(recommendationsBtn)

        self.layout.addLayout(layoutMovieH,0,0,1,3)
        self.layout.addLayout(layoutH,2,0,1,3)

        self.setLayout(self.layout)

        self.setGeometry(20,20,500,500)
        self.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__)) + '/movie.png'))
        self.setWindowTitle('Filmweb')
        self.show()

    def show_latest(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()

        title_labels = []
        buttons = []

        for movie in db.getMovies():
            box_layout = QHBoxLayout()
            title_label = QLabel(movie.get_title())
            avg_rate_label = QLabel(str(movie.get_avg_rate()))
            button = QPushButton("&Rate", self)
            button.clicked.connect(lambda: self.rateMovie(movie,avg_rate_label,RateDialog.getRate(self)))
            details_button = QPushButton("&Details", self)
            details_button.clicked.connect(lambda: DetailsDialog.get_movie_details(movie,self))
            box_layout.addWidget(title_label)
            box_layout.addWidget(avg_rate_label)
            box_layout.addWidget(details_button)
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

    def show_recommendations(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()

        title_labels = []
        buttons = []

        for movie in sorted(db.getMovies(), key = lambda movie: movie.get_avg_rate()):
            box_layout = QHBoxLayout()
            title_label = QLabel(movie.get_title())
            avg_rate_label = QLabel(str(movie.get_avg_rate()))
            button = QPushButton("&Rate", self)
            button.clicked.connect(lambda: self.rateMovie(movie,avg_rate_label,RateDialog.getRate(self)))
            details_button = QPushButton("&Details", self)
            details_button.clicked.connect(lambda: DetailsDialog.get_movie_details(movie,self))
            box_layout.addWidget(title_label)
            box_layout.addWidget(avg_rate_label)
            box_layout.addWidget(details_button)
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

    def rateMovie(self,movie,label,value):
        movie.rate(value,self.current_user)
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

        self.current_user = db.loginUser(login,password)

        if  self.current_user is None:
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

        self.current_user = db.registerUser(login,email,password)

        QMessageBox.information(self,
            'Information', 'Registered succesfully !', QMessageBox.Ok)


        self.loginBtn.hide()
        self.registerBtn.hide()
        self.logoutBtn.show()

    def logout(self):
        self.current_user = None

        self.loginBtn.show()
        self.registerBtn.show()
        self.logoutBtn.hide()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    db = Database('filmweb.db')
    main_window = MainWindow()
    sys.exit(app.exec_())