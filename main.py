from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout , QStackedLayout
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox , QScrollArea , QGroupBox , QFormLayout 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from dialogs.login_dialog import LoginDialog , RegisterDialog
from dialogs.rate_dialog import RateDialog
from database import Database
from dialogs.app_instance import AppInstance
from dialogs.details_dialog import DetailsDialog
from profile import QProfileLayout
import os



class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.interface()
    
    
    def interface(self):
        self.main_layout = QStackedLayout()
        self.layout = QGridLayout()

        self.show_latest()

        layoutMovieH = QHBoxLayout()

        latestBtn = QPushButton("&Latest",self)
        latestBtn.clicked.connect(self.show_latest)
        recommendationsBtn = QPushButton("&Recommendations",self)
        recommendationsBtn.clicked.connect(self.show_recommendations)

        layoutH = QHBoxLayout()
        self.layoutUserH = QHBoxLayout()

        self.profileBtn = QPushButton("&Profile",self)
        self.profileBtn.clicked.connect(self.show_profile)
        self.userLabel = QLabel("User")
        self.layoutUserH.addStretch()
        self.layoutUserH.addWidget(self.userLabel)
        self.layoutUserH.addWidget(self.profileBtn)
        

        self.loginBtn = QPushButton("&Login", self)
        self.loginBtn.clicked.connect(self.login)
        self.registerBtn = QPushButton("&Register", self)
        self.registerBtn.clicked.connect(self.register)
        self.logoutBtn = QPushButton("&Logout",self)
        self.logoutBtn.clicked.connect(self.logout)

        layoutH.addStretch()
        layoutH.addWidget(self.loginBtn)
        layoutH.addWidget(self.registerBtn)
        layoutH.addWidget(self.logoutBtn)

        layoutMovieH.addWidget(latestBtn)
        layoutMovieH.addWidget(recommendationsBtn)
        layoutMovieH.addStretch()

        self.layout.addLayout(self.layoutUserH,0,0)
        self.layout.addLayout(layoutMovieH,1,0)
        self.layout.addLayout(layoutH,3,0)
        self.setLayout(self.layout)

        self.setGeometry(100,100,500,350)
        self.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__)) + '/movie.png'))
        self.setWindowTitle('Filmweb')

        self.set_is_logged(None)

        self.show()

    def show_profile(self):
        self.setLayout(QProfileLayout())

    def show_latest(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()

        title_labels = []
        buttons = []

        for movie in AppInstance.db.get_movies():
            box_layout = QHBoxLayout()
            title_label = QLabel(movie.get_title())
            avg_rate_label = QLabel(str(movie.get_avg_rate()))
            button = QPushButton("&Rate", self)
            button.clicked.connect(lambda: self.rateMovie(movie,avg_rate_label,RateDialog.get_rate(self)))
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
        box_layout = QHBoxLayout()
        box_layout.addWidget(scroll)
        self.layout.addLayout(box_layout,2,0)

    def show_recommendations(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()

        title_labels = []
        buttons = []

        for movie in sorted(AppInstance.db.get_movies(), key = lambda movie: movie.get_avg_rate()):
            box_layout = QHBoxLayout()
            title_label = QLabel(movie.get_title())
            avg_rate_label = QLabel(str(movie.get_avg_rate()))
            button = QPushButton("&Rate", self)
            button.clicked.connect(lambda: self.rateMovie(movie,avg_rate_label,RateDialog.get_rate(self)))
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
        box_layout = QHBoxLayout()
        box_layout.addWidget(scroll)
        self.layout.addLayout(box_layout,2,0)

    def rateMovie(self,movie,label,value):
        movie.rate(value,AppInstance.current_user)
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
        login, password, ok = LoginDialog.get_login_password(self)
        if not ok:
            return

        if not login or not password:
            QMessageBox.warning(self, 'Error',
                                'Empty login or password!', QMessageBox.Ok)
            return

        self.set_is_logged(AppInstance.db.login_user(login,password))

        if  AppInstance.current_user is None:
            QMessageBox.warning(self, 'Error',
                                'Wrong login or password!', QMessageBox.Ok)
            return

        QMessageBox.information(self,
            'Information:','Logged succesfully!', QMessageBox.Ok)

    def register(self):
        login, email, password, ok = RegisterDialog.get_login_password(self)
        if not ok:
            return

        if not login or not password or not email:
            QMessageBox.warning(self, 'Error',
                                'Empty login or email or password!', QMessageBox.Ok)
            return

        self.set_is_logged(AppInstance.db.register_user(login,email,password))

        QMessageBox.information(self,
            'Information', 'Registered succesfully !', QMessageBox.Ok)



    def logout(self):
        AppInstance.current_user = None
        self.set_is_logged(None)

    def set_is_logged(self,user):
        if user :
            AppInstance.current_user = user  
            self.loginBtn.hide()
            self.registerBtn.hide()
            self.logoutBtn.show()
            self.userLabel.setText(user.get_login())
            self.userLabel.show()
            self.profileBtn.show()
        else:
            AppInstance.current_user = None
            self.loginBtn.show()
            self.registerBtn.show()
            self.logoutBtn.hide()
            self.userLabel.hide()
            self.profileBtn.hide()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    AppInstance.db = Database('filmweb.db')
    main_window = MainWindow()
    sys.exit(app.exec_())