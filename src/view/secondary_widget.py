

from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtGui

from view import home_widget
import config


class SecondaryWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        back_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}home.png'), '')      
        back_btn.setFixedWidth(32)
        self._layout.addWidget(back_btn)
        back_btn.released.connect(self.back_home)
        self._central_widget = QtWidgets.QWidget()
        self._layout.addWidget(self._central_widget)
        self.window().setCentralWidget(self) 

    def back_home(self) -> None:
        self.window().setCentralWidget(home_widget.HomeWidget())
        self.window().setWindowTitle('Study and Repeat')
        self.exit()