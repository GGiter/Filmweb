from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit , QRadioButton ,QHBoxLayout
from PyQt5.QtWidgets import QGridLayout


class RateDialog(QDialog):

    def __init__(self, parent=None):
        super(RateDialog, self).__init__(parent)

        self.rate = 1

        # widget elements 
        layout = QHBoxLayout(self)
        self.b1 = QRadioButton("1")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.setRate(1))
        layout.addWidget(self.b1)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.b2 = QRadioButton("2")
        self.b2.setChecked(False)
        self.b2.toggled.connect(lambda:self.setRate(2))
        layout.addWidget(self.b2)

        self.b3 = QRadioButton("3")
        self.b3.setChecked(False)
        self.b3.toggled.connect(lambda:self.setRate(3))
        layout.addWidget(self.b3)


        self.b4 = QRadioButton("4")
        self.b4.setChecked(False)
        self.b4.toggled.connect(lambda:self.setRate(4))
        layout.addWidget(self.b4)

        self.b5 = QRadioButton("5")
        self.b5.setChecked(False)
        self.b5.toggled.connect(lambda:self.setRate(5))
        layout.addWidget(self.b5)

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
        dialog = RateDialog(parent)
        dialog.exec_()
        rate = dialog.rate
        return rate