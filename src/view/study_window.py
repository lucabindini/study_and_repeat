from PyQt5 import QtWidgets

from model import deck


class StudyWindow(QtWidgets.QMainWindow):

    def __init__(self, d: deck.Deck, *argv, **kwarg) -> None:
        super().__init__(*argv, **kwarg)

        self._deck = d
        self._current_card = self._deck.get_card()
        widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout()
        self._question_label = QtWidgets.QLabel(self._current_card.question)
        top_layout.addWidget(self._question_label)
        self._answer_label = QtWidgets.QLabel(self._current_card.answer)
        top_layout.addWidget(self._answer_label)
        self._buttons = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout()
        button_incorrect = QtWidgets.QPushButton('Incorrect')
        button_layout.addWidget(button_incorrect)
        button_incorrect.pressed.connect(self.next_question)
        button_correct = QtWidgets.QPushButton('Correct')
        button_layout.addWidget(button_correct)
        button_correct.pressed.connect(self.next_question)
        self._buttons.setLayout(button_layout)
        self._show_button = QtWidgets.QPushButton('Show answer')
        self._show_button.pressed.connect(self.show_answer)
        top_layout.addWidget(self._show_button)
        top_layout.addWidget(self._buttons)
        self._buttons.hide()
        self._answer_label.hide()
        widget.setLayout(top_layout)
        self.setCentralWidget(widget)

    def show_answer(self) -> None:
        self._show_button.hide()
        self._buttons.show()
        self._answer_label.show()

    def next_question(self) -> None:
        self._buttons.hide()
        self._show_button.show()
        self._answer_label.hide()
        self._current_card = self._deck.get_card()
        self._question_label.setText(self._current_card.question)
        self._answer_label.setText(self._current_card.answer)
