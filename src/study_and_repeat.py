import os
import sys

from PyQt5 import QtWidgets

from view import main_window
from model import deck


if not os.access(deck.DECKS_DIR, os.F_OK):
    os.makedirs(deck.DECKS_DIR)
app = QtWidgets.QApplication(sys.argv)
win = main_window.MainWindow()
win.show()
app.exec()
