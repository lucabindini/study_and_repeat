from PyQt5 import QtWidgets, QtGui

from view import secondary_widget
import config


class EditorWidget(secondary_widget.SecondaryWidget):

    question_prefix = '- '
    proportion = 6

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        h_layout = QtWidgets.QHBoxLayout()

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout()
        self._cards_list = QtWidgets.QListWidget()
        self._cards_list.currentRowChanged.connect(self.show_card)
        self._cards_list.itemPressed.connect(self.show_card)
        left_layout.addWidget(self._cards_list)
        create_remove_widget = QtWidgets.QWidget()
        create_remove_layout = QtWidgets.QGridLayout()
        create_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}plus.png'), 'New')
        create_remove_layout.addWidget(create_btn, 0, 0)
        create_btn.released.connect(self.create_card)
        self._remove_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}minus.png'), 'Remove')
        create_remove_layout.addWidget(self._remove_btn, 1, 0)
        self._remove_btn.released.connect(self.remove_card)
        self._up_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}arrow-090.png'), '')
        self._up_btn.setToolTip('Move up selected card')
        create_remove_layout.addWidget(self._up_btn, 0, 1)
        self._up_btn.released.connect(lambda: self.move_card(True))
        self._down_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}arrow-270.png'), '')
        self._down_btn.setToolTip('Move down selected card')
        create_remove_layout.addWidget(self._down_btn, 1, 1)
        self._down_btn.released.connect(lambda: self.move_card(False))
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
        self._add_img_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{config.ICONS_DIR}picture.png'), 'Add image')
        right_layout.addWidget(self._add_img_btn)
        self._add_img_btn.released.connect(self.add_image)
        right_widget.setLayout(right_layout)

        h_layout.addWidget(left_widget, 100//self.proportion)
        h_layout.addWidget(right_widget,
                           100 * (self.proportion-1) // self.proportion)
        self._central_widget.setLayout(h_layout)

        self.disable()
        self._cards_list.addItems(
            self.question_prefix + c.question
            for i, c in enumerate(self._deck.cards))

    def remove_card(self) -> None:
        current_row = self._cards_list.currentRow()
        self._cards_list.takeItem(current_row)
        self._cards_list.setCurrentRow(self._cards_list.currentRow())
        self._cards_list.clearSelection()
        self._deck.remove_card(current_row)
        self._cards_list.setCurrentRow(
            min(current_row, self._cards_list.count() - 1))
        self._old_select = self._cards_list.currentRow()
        if self._cards_list.count() == 0:
            self.disable()
        else:
            if self._cards_list.currentRow() == self._cards_list.count() - 1:
                self._down_btn.setDisabled(True)
            if self._cards_list.currentRow() == 0:
                self._up_btn.setDisabled(True)

    def create_card(self) -> None:
        self._deck.add_card('', '')
        self._cards_list.addItem(self.question_prefix)
        self._cards_list.setCurrentRow(self._cards_list.count() - 1)
        if self._cards_list.currentRow() > 0:
            self._up_btn.setEnabled(True)
        self._down_btn.setDisabled(True)

    def move_card(self, up: bool) -> None:
        current_row = self._cards_list.currentRow()
        self._deck.move_card(current_row, up)
        item = self._cards_list.takeItem(current_row - (2*up-1))
        self._cards_list.insertItem(self._cards_list.currentRow() + up, item)
        self._old_select = self._cards_list.currentRow()
        if up:
            self._down_btn.setEnabled(True)
            if self._cards_list.currentRow() == 0:
                self._up_btn.setDisabled(True)
        else:
            self._up_btn.setEnabled(True)
            if self._cards_list.currentRow() == self._cards_list.count() - 1:
                self._down_btn.setDisabled(True)

    def show_card(self) -> None:
        try:
            self._deck.cards[self._old_select].question\
                = self._question_edit.text()
            self._deck.cards[self._old_select].answer\
                = self._answer_edit.toHtml()
            self._cards_list.item(self._old_select).setText(
                self.question_prefix
                + self._deck.cards[self._old_select].question)
        except TypeError:
            self._question_edit.setEnabled(True)
            self._answer_edit.setEnabled(True)
            self._add_img_btn.setEnabled(True)
            self._remove_btn.setEnabled(True)
        if self._cards_list.currentRow() > 0:
            self._up_btn.setEnabled(True)
        else:
            self._up_btn.setDisabled(True)
        if self._cards_list.currentRow() < self._cards_list.count() - 1:
            self._down_btn.setEnabled(True)
        else:
            self._down_btn.setDisabled(True)
        self._question_edit.setText(
            self._deck.cards[self._cards_list.currentRow()].question)
        self._answer_edit.setText(
            self._deck.cards[self._cards_list.currentRow()].answer)
        self._old_select = self._cards_list.currentRow()

    def add_image(self) -> None:
        file_name = QtWidgets.QFileDialog.getOpenFileName(parent=self.window(),
            filter='Images (*.png *.jpeg *.jpg)')
        try:
            path = self._deck.add_image(
                file_name[0], self._cards_list.currentRow())
            self._answer_edit.textCursor().insertImage(path)
        except FileNotFoundError:
            pass

    def disable(self) -> None:
        self._old_select = None
        self._question_edit.setText('')
        self._question_edit.setDisabled(True)
        self._answer_edit.setText('')
        self._answer_edit.setDisabled(True)
        self._add_img_btn.setDisabled(True)
        self._remove_btn.setDisabled(True)
        self._up_btn.setDisabled(True)
        self._down_btn.setDisabled(True)

    def exit(self) -> None:
        try:
            self._deck.cards[self._old_select].question\
                = self._question_edit.text()
            self._deck.cards[self._old_select].answer\
                = self._answer_edit.toHtml()
        except TypeError:
            pass
        self._deck.dump()
