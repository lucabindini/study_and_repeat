from PyQt5 import QtWidgets, QtGui

from view import create_widget, study_widget
from model import deck


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *argv, **kwarg) -> None:
        super().__init__(*argv, **kwarg)

        widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout()
        deck_label = QtWidgets.QLabel('Deck name:')
        v_layout.addWidget(deck_label)
        self._deck_edit = QtWidgets.QLineEdit()
        v_layout.addWidget(self._deck_edit)
        create_btn = QtWidgets.QPushButton('Create deck')
        v_layout.addWidget(create_btn)
        create_btn.pressed.connect(self.create_deck)
        open_btn = QtWidgets.QPushButton('Open deck')
        v_layout.addWidget(open_btn)
        open_btn.pressed.connect(self.open_deck)
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

    def create_deck(self) -> None:
        self._deck = deck.Deck(self._deck_edit.text())
        widget = create_widget.CreateWidget(self._deck)
        self.setCentralWidget(widget)

    def open_deck(self) -> None:
        self._deck = deck.load_deck(self._deck_edit.text())
        widget = study_widget.StudyWidget(self._deck)
        self.setCentralWidget(widget)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self._deck.dump()
        return super().closeEvent(a0)




