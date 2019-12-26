from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout

class LoginDialog(QDialog):
    """ Login dialog window """

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        # widget elements 
        loginLb = QLabel('Login')
        passwordLb = QLabel('Password')
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        # main layout
        layout = QGridLayout(self)
        layout.addWidget(loginLb, 0, 0)
        layout.addWidget(self.login, 0, 1)
        layout.addWidget(passwordLb, 1, 0)
        layout.addWidget(self.password, 1, 1)
        layout.addWidget(self.buttons, 2, 0, 2, 0)

        # signals and slots 
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # properties of widget 
        self.setModal(True)
        self.setWindowTitle('Login')

    def getLoginAndPassword(self):
        return (self.login.text().strip(),
                self.password.text().strip())

    # static method, creates dialog and returns (login, password, ok)
    @staticmethod
    def getLoginPassword(parent=None):
        dialog = LoginDialog(parent)
        dialog.login.setFocus()
        ok = dialog.exec_()
        login, password = dialog.getLoginAndPassword()
        return (login, password, ok == QDialog.Accepted)



class RegisterDialog(QDialog):
    """ Register dialog window """

    def __init__(self, parent=None):
        super(RegisterDialog, self).__init__(parent)

        # widget elements 
        loginLb = QLabel('Login')
        emailLb = QLabel("Email")
        passwordLb = QLabel('Password')
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.email = QLineEdit()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        # main layout
        layout = QGridLayout(self)
        layout.addWidget(loginLb, 0, 0)
        layout.addWidget(self.login, 0, 1)
        layout.addWidget(emailLb, 1, 0)
        layout.addWidget(self.email, 1, 1)
        layout.addWidget(passwordLb, 2, 0)
        layout.addWidget(self.password, 2, 1)
        layout.addWidget(self.buttons, 3, 0, 3, 0)

        # signals and slots 
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # properties of widget 
        self.setModal(True)
        self.setWindowTitle('Register')

    def get_data(self):
        return (self.login.text().strip(),
                self.email.text().strip(),
                self.password.text().strip())

    # static method, creates dialog and returns (login,email, password, ok)
    @staticmethod
    def getLoginPassword(parent=None):
        dialog = RegisterDialog(parent)
        dialog.login.setFocus()
        ok = dialog.exec_()
        login, email, password = dialog.get_data()
        return (login, email, password, ok == QDialog.Accepted)