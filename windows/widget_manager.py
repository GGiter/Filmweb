from PyQt5.QtWidgets import QStackedLayout , QMainWindow
from windows.main_window import MainWindow
from windows.profile_window import ProfileWindow
from windows.filmweb_window import FilmwebWindow
from app_instance import AppInstance
from data.database import Database
import os

class WidgetManager(FilmwebWindow,QMainWindow):
    """
    class that controls changing between filmweb windows
    """
    def __init__(self, parent = None):
        super().__init__(parent)
        self.stacked_layout = QStackedLayout()

        self.main_window = MainWindow(self.switch_window)
        self.stacked_layout.addWidget(self.main_window)
        self.profile_window = ProfileWindow(self.switch_window,AppInstance.current_user)
        self.stacked_layout.addWidget(self.profile_window)

        self.switch_window("Main Window")
       

    def switch_window(self,window_name,**kwargs):
        """
        switch to Main Window or Profile window
        takes user variable in **kwargs for Profile window
        """
        if window_name == "Main Window":
            self.stacked_layout.setCurrentIndex(0)
        elif 'user' in kwargs:
            self.profile_window.set_user(kwargs['user'])
            self.stacked_layout.setCurrentIndex(1)


        