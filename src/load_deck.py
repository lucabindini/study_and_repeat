from PyQt5 import QtWidgets

from model import deck
from view import study_window


d = deck.load_deck('decks/testing_deck.pickle')

app = QtWidgets.QApplication([])
win = study_window.StudyWindow(d)
win.show()
app.exec()
