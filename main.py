from PyQt5.QtWidgets import QApplication , QStyleFactory 
from app_instance import AppInstance
from windows.widget_manager import WidgetManager
from data.database import Database
import sys

if __name__ == '__main__':
    app_instance = AppInstance(QApplication(sys.argv),Database('filmweb.db'))
    app_instance.app.setStyle(QStyleFactory.create('Fusion'))
    widget_manager = WidgetManager()
    sys.exit(app_instance.app.exec_())

        