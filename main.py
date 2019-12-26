from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout
from PyQt5.QtWidgets import QLineEdit , QPushButton , QHBoxLayout ,QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.interface()
    
    def interface(self):

        label1 = QLabel('New movies:', self)

        layout = QGridLayout()
        layout.addWidget(label1,1,1)

        layoutH = QHBoxLayout()

        loginBtn = QPushButton("&Login", self)
        registerBtn = QPushButton("&Register", self)

        layoutH.addWidget(loginBtn)
        layoutH.addWidget(registerBtn)

        layout.addLayout(layoutH,2,0,1,3)

        self.setLayout(layout)

        self.setGeometry(3,3,300,100)
        self.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__)) + '/movie.png'))
        self.setWindowTitle('Filmweb')
        self.show()

    
    def closeEvent(self, event):

        answer = QMessageBox.question(self, 'Question',"Do you really want to leave?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
        if answer == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())