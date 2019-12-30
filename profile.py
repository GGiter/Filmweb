from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout

class QProfileLayout(QGridLayout):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.interface()

    def interface(self):
        pass
