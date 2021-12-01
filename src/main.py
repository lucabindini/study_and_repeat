import os

from PyQt5 import QtWidgets

from view import main_window


if not os.access('decks', os.F_OK):
    os.mkdir('decks')
app = QtWidgets.QApplication([])
win = main_window.MainWindow()
win.show()
app.exec()
