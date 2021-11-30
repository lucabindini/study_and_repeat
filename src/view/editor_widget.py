from pickle import TRUE
from PyQt5 import QtWidgets, QtCore

from model import deck


class EditorWidget(QtWidgets.QWidget):

    def __init__(self, d: deck.Deck, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._deck = d
        h_layout = QtWidgets.QHBoxLayout()

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout()
        self._cards_list = QtWidgets.QListWidget()
        self._cards_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self._cards_list.setMovement(QtWidgets.QListView.Snap)
        self._cards_list.itemSelectionChanged.connect(self.show_card)
        left_layout.addWidget(self._cards_list)
        create_remove_widget = QtWidgets.QWidget()
        create_remove_layout = QtWidgets.QHBoxLayout()
        remove_btn = QtWidgets.QPushButton('Remove card')
        create_remove_layout.addWidget(remove_btn)
        remove_btn.released.connect(self.remove_card)
        create_btn = QtWidgets.QPushButton('Create card')
        create_remove_layout.addWidget(create_btn)
        create_btn.released.connect(self.create_card)
        create_remove_widget.setLayout(create_remove_layout)
        left_layout.addWidget(create_remove_widget)
        left_widget.setLayout(left_layout)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout()
        question_label = QtWidgets.QLabel('Question:')
        right_layout.addWidget(question_label)
        self._question_edit = QtWidgets.QLineEdit()
        right_layout.addWidget(self._question_edit)
        answer_label = QtWidgets.QLabel('Answer:')
        right_layout.addWidget(answer_label)
        self._answer_edit = QtWidgets.QTextEdit()
        right_layout.addWidget(self._answer_edit)
        self._add_img_btn = QtWidgets.QPushButton('Add image')
        right_layout.addWidget(self._add_img_btn)
        self._add_img_btn.released.connect(self.add_image)
        right_widget.setLayout(right_layout)

        h_layout.addWidget(left_widget, 100//4)
        h_layout.addWidget(right_widget, 100*3//4)
        self.setLayout(h_layout)
        self.window().setCentralWidget(self)

        self.disable_right()
        self.refresh_list()

    def remove_card(self):
        current_row = self._cards_list.currentRow()
        self._cards_list.clearSelection()
        self._deck.remove_card(current_row)
        self.disable_right()
        self.refresh_list()

    def create_card(self) -> None:
        self._deck.add_card('', '')
        self.refresh_list()
        self._cards_list.setCurrentRow(self._cards_list.count() - 1)

    def refresh_list(self) -> None:
        self._cards_list.clear()
        self._cards_list.addItems(c.question for c in self._deck.cards)

    def show_card(self) -> None:
        try:
            self._deck.cards[self._old_select].question = self._question_edit.text()
            self._deck.cards[self._old_select].answer = self._answer_edit.toHtml()
            self._cards_list.item(self._old_select).setText(
                self._deck.cards[self._old_select].question)
        except TypeError:
            self._question_edit.setEnabled(True)
            self._answer_edit.setEnabled(True)
            self._add_img_btn.setEnabled(True)
        self._question_edit.setText(
            self._deck.cards[self._cards_list.currentRow()].question)
        self._answer_edit.setText(
            self._deck.cards[self._cards_list.currentRow()].answer)
        self._old_select = self._cards_list.currentRow()

    def add_image(self) -> None:
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            filter='Images (*.png *.jpeg *.jpg)')
        try:
            path = self._deck.add_image(file_name[0])
            self._answer_edit.textCursor().insertImage(path)
        except FileNotFoundError:
            pass

    def disable_right(self) -> None:
        self._old_select = None
        self._question_edit.setText('')
        self._question_edit.setDisabled(True)
        self._answer_edit.setText('')
        self._answer_edit.setDisabled(True)
        self._add_img_btn.setDisabled(True)

    def exit(self) -> None:
        self.show_card()
        self._deck.dump()
