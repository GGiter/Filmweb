from PyQt5.QtWidgets import QApplication , QWidget,QStyleFactory 
from dialogs.app_instance import AppInstance
from windows.widget_manager import WidgetManager
from database import Database

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    AppInstance.db = Database('filmweb.db')
    app.setStyle(QStyleFactory.create('Fusion'))
    widget_manager = WidgetManager()
    
    sys.exit(app.exec_())
        