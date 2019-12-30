from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox , QScrollArea , QGroupBox , QFormLayout 
from filmweb_window import FilmwebWindow

class ProfileWindow(FilmwebWindow):
    def __init__(self, switch_window, parent = None):
        super().__init__(parent)
        self.switch_window = switch_window
        self.interface()

    def interface(self):
        self.layout = QGridLayout()

        self.backBtn = QPushButton("&Back",self)
        self.backBtn.clicked.connect(self.show_main_window)

        self.layout.addWidget(self.backBtn)

        self.setLayout(self.layout)

    def show_main_window(self):
        self.switch_window("Main Window")
