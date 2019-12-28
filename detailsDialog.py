from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit , QRadioButton ,QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from movie import Movie


class DetailsDialog(QDialog):

    def __init__(self, parent=None):
        super(DetailsDialog, self).__init__(parent)
        # widget elements 
        layout = QHBoxLayout(self)


        layout.addWidget(self.buttons)
        # signals and slots 
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # properties of widget 
        self.setModal(True)
        self.setWindowTitle('Details')


    @staticmethod
    def get_movie_details(movie,parent=None):
        dialog = DetailsDialog(parent)
        dialog.exec_()
        return movie