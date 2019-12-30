from PyQt5.QtWidgets import QApplication , QWidget , QLabel , QGridLayout , QStackedLayout , QMainWindow
from windows.main_window import MainWindow
from windows.profile_window import ProfileWindow
from PyQt5.QtCore import Qt 
from windows.filmweb_window import FilmwebWindow
from dialogs.app_instance import AppInstance
from database import Database
import os

class WidgetManager(FilmwebWindow,QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.stacked_layout = QStackedLayout()

        self.main_window = MainWindow(self.switch_window)
        self.stacked_layout.addWidget(self.main_window)
        self.profile_window = ProfileWindow(self.switch_window)
        self.stacked_layout.addWidget(self.profile_window)

        self.switch_window("Main Window")
       

    def switch_window(self,window_name,**kwargs):
        if window_name == "Main Window":
            self.stacked_layout.setCurrentIndex(0)
        elif 'user' in kwargs:
            self.profile_window.set_user(kwargs['user'])
            self.stacked_layout.setCurrentIndex(1)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    AppInstance.db = Database('filmweb.db')
    widget_manager = WidgetManager()
  
    sys.exit(app.exec_())
        