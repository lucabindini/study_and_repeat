from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtGui

from view import home_widget
from model import deck
import config


class SecondaryWidget(QtWidgets.QWidget):

    def __init__(self, d: deck.Deck, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._deck = d
        self.window().setWindowTitle(f'Study and Repeat - {self._deck.name}')

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        back_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}home.png'), '')
        back_btn.setFixedWidth(32)
        back_btn.setToolTip('Back home')
        self._layout.addWidget(back_btn)
        back_btn.released.connect(self.back_home)
        self._central_widget = QtWidgets.QWidget()
        self._layout.addWidget(self._central_widget)

        self.window().setCentralWidget(self)

        self.window().action_new_deck.setVisible(False)
        self.window().action_export_deck.setVisible(False)
        self.window().action_import_deck.setVisible(False)
        self.window().action_reset_deck.setVisible(False)
        self.window().action_delete_deck.setVisible(False)

    def back_home(self) -> None:
        self.window().setCentralWidget(home_widget.HomeWidget(
            parent=self.window()))
        self.exit()
