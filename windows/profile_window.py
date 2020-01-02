from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout
from PyQt5.QtGui import QIcon , QPixmap
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox , QScrollArea , QGroupBox , QFormLayout 
from windows.filmweb_window import FilmwebWindow
from data_objects.user import User
from data_objects.review import Review
from dialogs.app_instance import AppInstance
import os
import sys

class ProfileWindow(FilmwebWindow):
    def __init__(self, switch_window,user, parent = None):
        super().__init__(parent)
        self.switch_window = switch_window
        self.interface()
        self.set_user(user)

    def interface(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def show_main_window(self):
        self.switch_window("Main Window")

    def show_reviews(self):
        mygroupbox = QGroupBox()
        myform = QFormLayout()

        for review in AppInstance.db.get_user_reviews(self.user):
            box_layout = QHBoxLayout()
            movie_label = QLabel(AppInstance.db.get_field("movies","title",review.get_movie_id()))
            director_label = QLabel(AppInstance.db.get_field("movies","director",review.get_movie_id()))
            score_label = QLabel(str(review.get_score()))
            if AppInstance.db.get_field("movies","icon_path",review.get_movie_id()) != 'None':
                pixmap = QPixmap(AppInstance.db.get_field("movies","icon_path",review.get_movie_id())).scaled(20,20)  
            else:
                pixmap = QPixmap(os.path.dirname(sys.argv[0]) + '/icons/user.png').scaled(20,20)
            pic = QLabel()
            pic.setPixmap(pixmap)
            box_layout.addWidget(pic)
            box_layout.addWidget(movie_label)
            box_layout.addWidget(director_label)
            box_layout.addWidget(score_label)
            myform.addRow(box_layout)
            
        
        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True) 
        scroll.setFixedHeight(200)
        self.box_layout_scroll = QHBoxLayout()
        self.box_layout_scroll.addWidget(scroll)
        self.layout.addLayout(self.box_layout_scroll,1,0)

    def set_user(self, user):
        self.user = user
        self.delete_items_of_layout(self.layout)
        if user is not None:
            self.label = QLabel(self.user.get_login())
            self.box_layout = QHBoxLayout()
            self.box_layout.addWidget(self.label)
            self.layout.addLayout(self.box_layout,0,0)
            self.backBtn = QPushButton("&Back",self)
            self.backBtn.clicked.connect(self.show_main_window)
            box_layout = QHBoxLayout()
            box_layout.addStretch()
            box_layout.addWidget(self.backBtn)
            self.layout.addLayout(box_layout,2,0)
            
            self.show_reviews()

    def delete_items_of_layout(self,layout):
     if layout is not None:
         while layout.count():
             item = layout.takeAt(0)
             widget = item.widget()
             if widget is not None:
                 widget.setParent(None)
             else:
                 self.delete_items_of_layout(item.layout())


