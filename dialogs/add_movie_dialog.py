from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit , QRadioButton ,QVBoxLayout ,QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from movie import Movie

class AddMovieDialog(QDialog):
    def __init__(self, movie, parent=None):
        super(AddMovieDialog, self).__init__(parent)
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
        for field in ["title","director","description","actors","genre"]:
            box_layout = QHBoxLayout()
            label = QLabel(field)
            line_edit = QLineEdit()
            self.line_edits.append(line_edit)
            box_layout.addWidget(label)
            box_layout.addWidget(line_edit)
            self.layout.addLayout(box_layout)

    def get_data(self):
        data = []
        for line_edit in self.line_edits : 
            data.append(line_edit.text().strip())
        return Movie(*data)


    @staticmethod
    def get_movie_details(parent=None):
        dialog = AddMovieDialog(parent)
        ok = dialog.exec_()
        return (dialog.get_data(),ok == QDialog.Accepted)