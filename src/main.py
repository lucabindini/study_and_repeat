from PyQt5 import QtWidgets

from model import card, deck
from view import study_window


d = deck.Deck('testing_deck')
d.add_card(card.Card('first question', 'first answer'))
d.add_card(card.Card('second question', 'second answer'))
d.dump()
d_copy = deck.load_deck('decks/testing_deck.pickle')
app = QtWidgets.QApplication([])
win = study_window.StudyWindow(d_copy)
win.show()
app.exec()
