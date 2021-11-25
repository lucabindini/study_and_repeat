from PyQt5 import QtWidgets

from model import deck


class StudyWidget(QtWidgets.QWidget):

    def __init__(self, d: deck.Deck, *argv, **kwarg) -> None:
        super().__init__(*argv, **kwarg)

        self._deck = d
        self._current_card = self._deck.get_card()
        v_layout = QtWidgets.QVBoxLayout()
        self._question_label = QtWidgets.QLabel(self._current_card.question)
        v_layout.addWidget(self._question_label)
        self._answer_label = QtWidgets.QLabel(self._current_card.answer)
        v_layout.addWidget(self._answer_label)
        self._correctness_btns = QtWidgets.QWidget()
        btn_layout = QtWidgets.QHBoxLayout()
        incorrect_btn = QtWidgets.QPushButton('Incorrect')
        btn_layout.addWidget(incorrect_btn)
        incorrect_btn.pressed.connect(lambda: self.next_question(False))
        correct_btn = QtWidgets.QPushButton('Correct')
        btn_layout.addWidget(correct_btn)
        correct_btn.pressed.connect(lambda: self.next_question(True))
        self._correctness_btns.setLayout(btn_layout)
        self._show_btn = QtWidgets.QPushButton('Show answer')
        self._show_btn.pressed.connect(self.show_answer)
        v_layout.addWidget(self._show_btn)
        v_layout.addWidget(self._correctness_btns)
        self._correctness_btns.hide()
        self._answer_label.hide()
        self.setLayout(v_layout)

    def show_answer(self) -> None:
        self._show_btn.hide()
        self._correctness_btns.show()
        self._answer_label.show()

    def next_question(self, correctness) -> None:
        self._correctness_btns.hide()
        self._show_btn.show()
        self._answer_label.hide()
        self._deck.calculate_delay(correctness)
        self._current_card = self._deck.get_card()
        self._question_label.setText(self._current_card.question)
        self._answer_label.setText(self._current_card.answer)
