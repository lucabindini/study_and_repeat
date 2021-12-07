import os
import sys

from PyQt5 import QtWidgets

from view import main_window
import config


if not os.access(config.DECKS_DIR, os.F_OK):
    os.makedirs(config.DECKS_DIR)
app = QtWidgets.QApplication(sys.argv)
window = main_window.self()
window.show()
app.exec()
