from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox, QGroupBox, QFormLayout
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QScrollArea
from app_instance import AppInstance
from dialogs.filmweb_dialog import FilmwebDialog


class DetailsDialog(FilmwebDialog):
    """
    Dialog window that hosts informations about given movie
    """
    def __init__(self, movie, parent=None):
        super(DetailsDialog, self).__init__(parent)
        self.setMaximumWidth(250)
        self.setMaximumHeight(250)
        # widget elements
        self.layout = QVBoxLayout(self)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok,
            Qt.Horizontal, self)

        self.get_details(movie)
        self.get_ratings(movie)
        self.layout.addWidget(self.buttons)
        # signals and slots
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # properties of widget
        self.setModal(True)
        self.setWindowTitle('Details')

    def get_details(self, movie):
        """
        Get details about movie
        """
        movie_id = movie.get_id()
        db = AppInstance.db
        for field in ["title", "director", "description",
                      "duration", "actors", "genre"]:
            label = (QLabel(field.capitalize() + ": " +
                     str(db.get_field_by_id("movies", field, movie_id))))
            self.layout.addWidget(label)

    def get_ratings(self, movie):
        """
        Get user ratings for a movie
        """
        mygroupbox = QGroupBox()
        myform = QFormLayout()
        db = AppInstance.db

        reviews = AppInstance.db.get_movie_reviews(movie)
        for review in reviews:
            user_id = review.get_user_id()
            box_layout = QHBoxLayout()
            user_label = QLabel(str(
                         db.get_field_by_id("users", "login", user_id)))
            rate_label = QLabel(str(review.get_score()))
            box_layout.addWidget(user_label)
            box_layout.addWidget(rate_label)
            myform.addRow(box_layout)

        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        box_layout = QHBoxLayout()
        box_layout.addWidget(scroll)
        self.layout.addLayout(box_layout)

    @staticmethod
    def get_movie_details(movie, parent=None):
        """
        Static method , which creates DetailsDialog about specified movie
        """
        dialog = DetailsDialog(movie, parent)
        ok = dialog.exec_()
        return ok
