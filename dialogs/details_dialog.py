from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit , QRadioButton ,QVBoxLayout
from PyQt5.QtWidgets import QGridLayout
from app_instance import AppInstance

class DetailsDialog(QDialog):
    """
    Dialog window that hosts informations about given movie
    """
    def __init__(self, movie, parent=None):
        super(DetailsDialog, self).__init__(parent)
        # widget elements 
        self.layout = QVBoxLayout(self)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok,
            Qt.Horizontal, self)

        self.get_details(movie)
        self.layout.addWidget(self.buttons)
        # signals and slots 
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # properties of widget 
        self.setModal(True)
        self.setWindowTitle('Details')

        
    def get_details(self,movie):
        """
        Get details about movie
        """
        for field in ["title","director","description","duration","actors","genre"]:
            label = QLabel(field + ": " + AppInstance.db.get_field("movies",field,movie.get_id()))
            self.layout.addWidget(label)

    @staticmethod
    def get_movie_details(movie,parent=None):
        """
        Static method , which creates DetailsDialog about specified movie
        """
        dialog = DetailsDialog(movie,parent)
        ok = dialog.exec_()
        return ok