from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox , QScrollArea , QGroupBox , QFormLayout 
import os
import sys

class FilmwebWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setGeometry(100,100,500,350)
        self.setFixedSize(500,350)
        self.setWindowIcon(QIcon(os.path.dirname(sys.argv[0]) + '/icons/movie.png'))
        self.setWindowTitle('Filmweb')

    def closeEvent(self, event):

        answer = QMessageBox.question(self, 'Warning',"Do you really want to leave?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
        if answer == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()