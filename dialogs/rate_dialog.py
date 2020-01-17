from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit , QRadioButton ,QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from dialogs.filmweb_dialog import FilmwebDialog

class RateDialog(FilmwebDialog):
    """
    Rate dialog window
    """
    def __init__(self, parent=None):
        super(RateDialog, self).__init__(parent)
        self.set_rate(1)
        self.setMaximumWidth(500)
        self.setMaximumHeight(100)

        # widget elements 
        layout = QHBoxLayout(self)
        for i in range(1,11):
            self.radio_button = QRadioButton(f"{i}")
            self.radio_button.setChecked(True if i == 1 else False)
            self.radio_button.toggled.connect(lambda state, x = i :self.set_rate(x))
            layout.addWidget(self.radio_button)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        layout.addWidget(self.buttons)
        # signals and slots 
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # properties of widget 
        self.setModal(True)
        self.setWindowTitle('Rate')


    def set_rate(self,value):
        self.rate = value

    @staticmethod
    def get_rate(parent=None):
        """
        Static method that creates RateDialog and gets data from it 
        return rate from 1 to 10
        """
        dialog = RateDialog(parent)
        dialog.exec_()
        rate = dialog.rate
        return rate