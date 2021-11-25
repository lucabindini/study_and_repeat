from PyQt5 import QtWidgets

from view import main_window


app = QtWidgets.QApplication([])
win = main_window.MainWindow()
win.show()
app.exec()
