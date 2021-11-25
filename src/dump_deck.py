import datetime

from PyQt5 import QtWidgets

from model import deck
from view import study_window


d = deck.Deck('testing_deck')
d.add_card(question='first question', answer='first answer')
d.add_card(question='second question', answer='second answer')

app = QtWidgets.QApplication([])
win = study_window.StudyWindow(d)
win.show()
app.exec()

d.last_study_day = (datetime.date.today() - datetime.timedelta(1))
d.dump()
