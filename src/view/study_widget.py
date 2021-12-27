from PyQt5 import QtWidgets, QtGui, QtCore

from model import deck
from view import home_widget, secondary_widget
import config


class StudyWidget(secondary_widget.SecondaryWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        font = self.font()
        font.setPointSize(12)

        v_layout = QtWidgets.QVBoxLayout()
        question_label = QtWidgets.QLabel('Question')
        label_font = question_label.font()
        label_font.setPointSize(12)
        label_font.setBold(True)
        question_label.setFont(label_font)
        v_layout.addWidget(question_label)
        self._question_text = QtWidgets.QLineEdit()
        self._question_text.setFont(font)
        self._question_text.setReadOnly(True)
        self._question_text.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(self._question_text)
        answer_label = QtWidgets.QLabel('Answer')
        v_layout.addWidget(answer_label)
        answer_label.setFont(label_font)
        self._answer_text = QtWidgets.QTextEdit()
        self._answer_text.setReadOnly(True)
        self._answer_text.setFont(font)
        v_layout.addWidget(self._answer_text)
        self._correctness_btns = QtWidgets.QWidget()
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        incorrect_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}cross.png'), 'Incorrect')
        btn_layout.addWidget(incorrect_btn)
        incorrect_btn.released.connect(lambda: self.next_question(False))
        correct_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}tick.png'), 'Correct')
        btn_layout.addWidget(correct_btn)
        correct_btn.released.connect(lambda: self.next_question(True))
        btn_layout.addStretch()
        self._correctness_btns.setLayout(btn_layout)
        v_layout.addWidget(self._correctness_btns)

        self._show_widget = QtWidgets.QWidget()
        show_layout = QtWidgets.QHBoxLayout()
        show_layout.addStretch()
        show_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}eye.png'), 'Show answer')
        show_btn.released.connect(self.show_answer)
        show_layout.addWidget(show_btn)
        show_layout.addStretch()
        self._show_widget.setLayout(show_layout)
        v_layout.addWidget(self._show_widget)

        self._correctness_btns.hide()

        self._central_widget.setLayout(v_layout)
        self.show_question()

        correct_btn.setMinimumWidth(128)
        incorrect_btn.setMinimumWidth(128)
        show_btn.setMinimumWidth(128)

    def show_question(self) -> None:
        try:
            self._current_card = self._deck.get_card()
        except deck.EmptyQueuesException:
            self._deck.dump()
            self.window().setCentralWidget(home_widget.HomeWidget(
                parent=self.window()))
        else:
            self._question_text.setText(self._current_card.question)
            self._answer_text.setDisabled(True)
            self._answer_text.setText('')
            self._answer_text.setPlaceholderText(
                'Click "Show answer" once you have thought of an answer')

    def show_answer(self) -> None:
        self._show_widget.hide()
        self._correctness_btns.show()
        self._answer_text.setText(self._current_card.get_answer())
        self._answer_text.setEnabled(True)

    def next_question(self, correctness) -> None:
        self._correctness_btns.hide()
        self._show_widget.show()
        self._deck.calculate_delay(correctness)
        self.show_question()

    def exit(self) -> None:
        self._deck.dump()
