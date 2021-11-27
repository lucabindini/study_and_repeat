from PyQt5 import QtWidgets

from model import deck
from view import editor_widget, study_widget


class HomeWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        v_layout = QtWidgets.QVBoxLayout()
        deck_label = QtWidgets.QLabel('Deck name:')
        v_layout.addWidget(deck_label)
        self._deck_edit = QtWidgets.QLineEdit()
        v_layout.addWidget(self._deck_edit)
        create_btn = QtWidgets.QPushButton('Edit deck')
        v_layout.addWidget(create_btn)
        create_btn.released.connect(self.create_deck)
        open_btn = QtWidgets.QPushButton('Open deck')
        v_layout.addWidget(open_btn)
        open_btn.released.connect(self.study_deck)
        self.setLayout(v_layout)

    def create_deck(self) -> None:
        try:
            d = deck.load_deck('decks/'+self._deck_edit.text()+'.pickle')
        except FileNotFoundError:
            d = deck.Deck(self._deck_edit.text())
        editor_widget.EditorWidget(d, parent=self.window())

    def study_deck(self) -> None:
        study_widget.StudyWidget(deck.load_deck(
            'decks/'+self._deck_edit.text()+'.pickle'), parent=self.window())

    def exit(self) -> None:
        pass
