import os

from PyQt5 import QtWidgets

from view import main_window
from model import deck


if not os.access(deck.DECKS_DIR, os.F_OK):
    os.mkdir(deck.DECKS_DIR)
app = QtWidgets.QApplication([])
win = main_window.MainWindow()
win.show()
app.exec()
