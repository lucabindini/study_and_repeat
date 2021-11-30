from PyQt5 import QtWidgets, QtGui

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
        add_img_btn = QtWidgets.QPushButton('Add Image')
        v_layout.addWidget(add_img_btn)
        add_img_btn.released.connect(self.add_image)
        next_card_btn = QtWidgets.QPushButton('Next card')
        v_layout.addWidget(next_card_btn)
        next_card_btn.released.connect(self.next_card)

        self.setLayout(v_layout)
        self.window().setCentralWidget(self)

    def next_card(self) -> None:
        self._deck.add_card(self._question_edit.text(),
                            self._answer_edit.toHtml())
        self._question_edit.setText('')
        self._answer_edit.setPlainText('')

    def add_image(self) -> None:
        file_name = QtWidgets.QFileDialog.getOpenFileName()  # TODO add filter
        print(file_name[0])
        path = self._deck.add_image(file_name[0])
        img = QtGui.QImage(path)
        self._answer_edit.textCursor().insertHtml(
            f'<img src="{path}"'
            + f' width={min(self._answer_edit.width()*3/4, img.width())}>')

    def exit(self) -> None:
        self._deck.dump()
