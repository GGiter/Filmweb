from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout , QStackedLayout
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox , QScrollArea , QGroupBox , QFormLayout , QRadioButton
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon ,QPixmap
from windows.filmweb_window import FilmwebWindow
from dialogs.login_dialog import LoginDialog , RegisterDialog
from dialogs.rate_dialog import RateDialog
from dialogs.add_movie_dialog import AddMovieDialog
from data.database import Database
from app_instance import AppInstance
from dialogs.details_dialog import DetailsDialog
from data_objects.user import User
import os
import sys


class MainWindow(FilmwebWindow):
    """
    Main window of the project that shows latest movies,
    recommended movies , users , search engine for movies
    has login and register buttons
    needs the reference to switch_window function from WidgetManager
    """
    def __init__(self, switch_window, parent = None):
        super().__init__(parent)
        self.switch_window = switch_window
        self.interface()
    
    
    def interface(self):
        # create main layout
        self.layout = QGridLayout()

        self.show_latest()

        layoutMovieH = QHBoxLayout()
        # create main buttons
        latestBtn = QPushButton("&Latest",self)
        latestBtn.clicked.connect(self.show_latest)
        recommendationsBtn = QPushButton("&Recommendations",self)
        recommendationsBtn.clicked.connect(self.show_recommendations)
        usersBtn = QPushButton("&Users",self)
        usersBtn.clicked.connect(self.show_users)
        add_movieBtn = QPushButton("&Add movie",self)
        add_movieBtn.clicked.connect(self.add_movie)

        layoutH = QHBoxLayout()
        self.layoutUserH = QHBoxLayout()
        # create basic search engine
        self.search_line = QLineEdit()
        self.search_line.editingFinished.connect(self.search)
        search_keys_layout = QHBoxLayout()
        radio_buttons = []
        for key in ["title","director","actors","genre"]: # radio buttons
            radio_button = QRadioButton(key)
            radio_button.setChecked(False)
            radio_button.clicked.connect(lambda state , x = key: self.set_search_key(x))
            search_keys_layout.addWidget(radio_button)
            radio_buttons.append(radio_button)

        search_keys_layout.addStretch()
        radio_buttons[0].setChecked(True)    
        self.set_search_key("title")

        # create profile interface
        self.profileBtn = QPushButton("&Profile",self)
        self.profileBtn.clicked.connect(lambda: self.show_profile(AppInstance.current_user))
        self.userLabel = QLabel("User")
        self.layoutUserH.addWidget(self.search_line)
        self.layoutUserH.addStretch()
        self.layoutUserH.addWidget(self.userLabel)
        self.layoutUserH.addWidget(self.profileBtn)
        
        # create user buttons
        self.loginBtn = QPushButton("&Login", self)
        self.loginBtn.clicked.connect(self.login)
        self.registerBtn = QPushButton("&Register", self)
        self.registerBtn.clicked.connect(self.register)
        self.logoutBtn = QPushButton("&Logout",self)
        self.logoutBtn.clicked.connect(self.logout)

        # position layouts
        layoutH.addStretch()
        layoutH.addWidget(self.loginBtn)
        layoutH.addWidget(self.registerBtn)
        layoutH.addWidget(self.logoutBtn)

        layoutMovieH.addWidget(latestBtn)
        layoutMovieH.addWidget(recommendationsBtn)
        layoutMovieH.addWidget(usersBtn)
        layoutMovieH.addStretch()
        layoutMovieH.addWidget(add_movieBtn)

        self.layout.addLayout(self.layoutUserH,0,0)
        self.layout.addLayout(search_keys_layout,1,0)
        self.layout.addLayout(layoutMovieH,2,0)
        self.layout.addLayout(layoutH,4,0)
        self.setLayout(self.layout)

        self.set_is_logged(None)

        self.show()
    
    def show_movies(self,**kwargs):
        mygroupbox = QGroupBox()
        myform = QFormLayout()

        title_labels = []
        buttons = []
        movies = []
        if "key" in kwargs and "value" in kwargs:
            movies = AppInstance.db.get_movies_by_parameter(self.search_key,self.search_line.text().strip())
        elif "sort" in kwargs:
            movies = sorted(AppInstance.db.get_movies(), key = lambda movie: movie.get_avg_rate(),reverse = True)
        else:
            movies = AppInstance.db.get_movies()

        for movie in movies:
            box_layout = QHBoxLayout()
            title_label = QLabel(movie.get_title())
            avg_rate_label = QLabel(str(movie.get_avg_rate()))
            button = QPushButton("&Rate", self)
            button.clicked.connect(lambda state , x = movie , label = avg_rate_label: self.rate_movie(x,label,RateDialog.get_rate(self)))
            details_button = QPushButton("&Details", self)
            details_button.clicked.connect(lambda state , x = movie : DetailsDialog.get_movie_details(x,self))
            if  movie.get_icon_path() != 'None':
                pixmap = QPixmap(movie.get_icon_path()).scaled(20,20) 
            else:
                pixmap = QPixmap(os.path.dirname(sys.argv[0]) + '/icons/movie.png').scaled(20,20)
            pic = QLabel()
            pic.setPixmap(pixmap)
            box_layout.addWidget(pic)
                
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
        self.layout.addLayout(box_layout,3,0)

    def set_search_key(self,key):
        self.search_key = key
        if self.search_line.text().strip() is not "":
            self.search()

    def search(self):
        if self.search_line.text().strip() is not "":
            self.show_movies(key = self.search_key , value = self.search_line.text().strip())
        else:
            self.show_movies()
   
    def show_users(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()

        for user in AppInstance.db.get_users():
            box_layout = QHBoxLayout()
            login_label = QLabel(user.get_login())
            button = QPushButton("&Profile", self)
            button.clicked.connect(lambda state, x = user: self.show_profile(x))
            if user.get_icon_path() != 'None':
                pixmap = QPixmap(user.get_icon_path()).scaled(20,20)  
            else:
                pixmap = QPixmap(os.path.dirname(sys.argv[0]) + '/icons/user.png').scaled(20,20)
            pic = QLabel()
            pic.setPixmap(pixmap)
            box_layout.addWidget(pic)
            box_layout.addWidget(login_label)
            box_layout.addWidget(button)
            myform.addRow(box_layout)
            
        
        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True) 
        scroll.setFixedHeight(200)
        box_layout = QHBoxLayout()
        box_layout.addWidget(scroll)
        self.layout.addLayout(box_layout,3,0)

    def add_movie(self):
        movie, ok = AddMovieDialog.get_movie_details(self)
        if not ok:
            return

        if movie is None:
            QMessageBox.warning(self, 'Error',
                                'Empty movie details', QMessageBox.Ok)
            return

        if AppInstance.db.add_movie(movie) is False:
            QMessageBox.warning(self,'Error',
                                'Invalid movie settings', QMessageBox.Ok)
            return 

        QMessageBox.information(self,
            'Information:','Added movie succesfully!', QMessageBox.Ok)

    def show_profile(self,user):
        self.switch_window("Profile",user = user)

    def show_latest(self):
        self.show_movies()

    def show_recommendations(self):
        self.show_movies(sort = True)

    def rate_movie(self,movie,label,value):
        if AppInstance.current_user:
            print(movie.get_title())
            AppInstance.db.rate_movie(AppInstance.current_user,movie,value)
            label.setText(str(movie.get_avg_rate()))
        else:
            QMessageBox.warning(self, 'Error',
                                'You need to be logged to rate a movie', QMessageBox.Ok)

    def login(self):
        login, password, ok = LoginDialog.get_login_password(self)
        if not ok:
            return

        if not login or not password:
            QMessageBox.warning(self, 'Error',
                                'Empty login or password!', QMessageBox.Ok)
            return

        user = AppInstance.db.login_user(login,password)
        
        if user is None:
            QMessageBox.warning(self, 'Error',
                                'Invalid login or password!', QMessageBox.Ok)
            return

        self.set_is_logged(user)

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

        user = AppInstance.db.register_user(login,email,password)

        if user is None:
            QMessageBox.warning(self, 'Error',
                                'Invalid login or email or password!', QMessageBox.Ok)
            return

        self.set_is_logged(user)

        QMessageBox.information(self,
            'Information', 'Registered succesfully !', QMessageBox.Ok)



    def logout(self):
        AppInstance.current_user = None
        self.set_is_logged(None)

    def set_is_logged(self,user):
        """
        Hide / show buttons , labels based on if the user is valid or not
        """
        if user is not None:
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

