from PyQt5 import QtWidgets

from model import deck


class EditorWidget(QtWidgets.QWidget):

    def __init__(self, d: deck.Deck, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._deck = d
        v_layout = QtWidgets.QVBoxLayout()
        question_label = QtWidgets.QLabel('Question:')
        v_layout.addWidget(question_label)
        self._question_edit = QtWidgets.QLineEdit()
        v_layout.addWidget(self._question_edit)
        answer_label = QtWidgets.QLabel('Answer:')
        v_layout.addWidget(answer_label)
        self._answer_edit = QtWidgets.QTextEdit()
        v_layout.addWidget(self._answer_edit)
        next_card_btn = QtWidgets.QPushButton('Next card')
        v_layout.addWidget(next_card_btn)
        next_card_btn.released.connect(self.next_card)
        self.setLayout(v_layout)

        self.window().setCentralWidget(self)

    def next_card(self) -> None:
        self._deck.add_card(self._question_edit.text(),
                            self._answer_edit.toPlainText())
        self._question_edit.setText('')
        self._answer_edit.setText('')

    def exit(self) -> None:
        self._deck.dump()
