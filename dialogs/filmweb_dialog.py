from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
import sys
import os


class FilmwebDialog(QDialog):
    """
    Dialog window that is parent to all dialog windows
    """
    def __init__(self, movie, parent=None):
        super(FilmwebDialog, self).__init__(parent)
        self.setWindowIcon(QIcon(
                           os.path.dirname(sys.argv[0]) + '/icons/movie.png'))
