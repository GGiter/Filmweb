from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox , QScrollArea , QGroupBox , QFormLayout 
from filmweb_window import FilmwebWindow
from user import User
from review import Review
from dialogs.app_instance import AppInstance

class ProfileWindow(FilmwebWindow):
    def __init__(self, switch_window, parent = None):
        super().__init__(parent)
        self.switch_window = switch_window
        self.interface()
        self.user = None

    def interface(self):
        self.layout = QGridLayout()

        self.backBtn = QPushButton("&Back",self)
        self.backBtn.clicked.connect(self.show_main_window)

        box_layout = QHBoxLayout()
        box_layout.addWidget(self.backBtn)
        self.layout.addLayout(box_layout,0,0)

        self.setLayout(self.layout)

    def show_main_window(self):
        self.switch_window("Main Window")

    def show_reviews(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()

        for review in AppInstance.db.get_user_reviews(self.user):
            box_layout = QHBoxLayout()
            movie_label = QLabel(AppInstance.db.get_field("movies","title",review.get_movie_id()))
            score_label = QLabel(str(review.get_score()))
            box_layout.addWidget(movie_label)
            box_layout.addWidget(score_label)
            myform.addRow(box_layout)
            
        
        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True) 
        scroll.setFixedHeight(200)
        box_layout = QHBoxLayout()
        box_layout.addWidget(scroll)
        self.layout.addLayout(box_layout,1,0)

    def set_user(self, user):
        self.user = user
        self.label = QLabel(user.get_login())
        box_layout = QHBoxLayout()
        box_layout.addWidget(self.label)
        self.layout.addLayout(box_layout,2,0)
        self.show_reviews()
