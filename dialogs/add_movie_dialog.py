from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit , QRadioButton ,QVBoxLayout ,QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from data_objects.movie import Movie
from dialogs.filmweb_dialog import FilmwebDialog

class AddMovieDialog(FilmwebDialog):
    def __init__(self, movie, parent=None):
        super(AddMovieDialog, self).__init__(parent)

        self.setMaximumWidth(250)
        self.setMaximumHeight(250)
        
        # widget elements 
        self.layout = QVBoxLayout(self)
        self.buttons = QDialogButtonBox(
             QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.show_fields()

        self.layout.addWidget(self.buttons)
        
        # signals and slots 
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # properties of widget 
        self.setModal(True)
        self.setWindowTitle('Details')

        
    def show_fields(self):
        self.line_edits = []
        for field in ["title","director","description","duration","actors","genre"]:
            box_layout = QHBoxLayout()
            label = QLabel(field.capitalize())
            line_edit = QLineEdit()
            self.line_edits.append(line_edit)
            box_layout.addWidget(label)
            box_layout.addWidget(line_edit)
            self.layout.addLayout(box_layout)

    def get_data(self):
        """
        gets data from QLineEdits 
        return Movie object
        """
        data = []
        for line_edit in self.line_edits : 
            data.append(line_edit.text().strip())
        return Movie(*data)


    @staticmethod
    def get_movie_details(parent=None):
        """
        Static method that creates AddMovieDialog and get the input from it
        return input data from the dialog
        """
        dialog = AddMovieDialog(parent)
        ok = dialog.exec_()
        return (dialog.get_data(),ok == QDialog.Accepted)