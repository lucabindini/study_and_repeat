from PyQt5 import QtWidgets, QtGui

from view import home_widget
import config


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(config.LOGO_PATH))
        self.setCentralWidget(home_widget.HomeWidget())

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.centralWidget().exit()
        return super().closeEvent(a0)
