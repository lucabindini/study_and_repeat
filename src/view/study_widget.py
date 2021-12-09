from PyQt5 import QtWidgets, QtGui

from model import deck
from view import home_widget, secondary_widget
import config


class StudyWidget(secondary_widget.SecondaryWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        v_layout = QtWidgets.QVBoxLayout()
        self._question_text = QtWidgets.QLineEdit()
        self._question_text.setReadOnly(True)
        v_layout.addWidget(self._question_text)
        self._answer_text = QtWidgets.QTextEdit()
        self._answer_text.setReadOnly(True)
        v_layout.addWidget(self._answer_text)
        self._correctness_btns = QtWidgets.QWidget()
        btn_layout = QtWidgets.QHBoxLayout()
        incorrect_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}cross.png'), 'Incorrect')
        btn_layout.addWidget(incorrect_btn)
        incorrect_btn.released.connect(lambda: self.next_question(False))
        correct_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}tick.png'), 'Correct')
        btn_layout.addWidget(correct_btn)
        correct_btn.released.connect(lambda: self.next_question(True))
        self._correctness_btns.setLayout(btn_layout)
        self._show_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}eye.png'), 'Show answer')
        self._show_btn.released.connect(self.show_answer)
        v_layout.addWidget(self._show_btn)
        v_layout.addWidget(self._correctness_btns)
        self._correctness_btns.hide()
        self._answer_text.hide()

        self._central_widget.setLayout(v_layout)
        self.show_question()

    def show_question(self) -> None:
        try:
            self._current_card = self._deck.get_card()
        except deck.EmptyQueuesException:
            self._deck.dump()
            self.window().setCentralWidget(home_widget.HomeWidget())
        else:
            self._question_text.setText(self._current_card.question)
            self._answer_text.setText(self._current_card.answer)

    def show_answer(self) -> None:
        self._show_btn.hide()
        self._correctness_btns.show()
        self._answer_text.show()

    def next_question(self, correctness) -> None:
        self._correctness_btns.hide()
        self._show_btn.show()
        self._answer_text.hide()
        self._deck.calculate_delay(correctness)
        self.show_question()

    def exit(self) -> None:
        self._deck.dump()
