import os

from PyQt5 import QtWidgets, QtCore, QtGui

from model import deck
from view import editor_widget, study_widget
import config


class HomeWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.window().setWindowTitle('Study and Repeat')
        outer_layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel('Your decks')
        label.setAlignment(QtCore.Qt.AlignCenter)
        font = label.font()
        font.setBold(True)
        font.setPointSize(24)
        label.setFont(font)
        outer_layout.addWidget(label)

        self._scroll_area = QtWidgets.QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self.populate_list()
        outer_layout.addWidget(self._scroll_area)

        new_deck_btn = QtWidgets.QPushButton(
                QtGui.QIcon(f'{config.ICONS_DIR}plus.png'), 'Create new deck')
        new_deck_btn.released.connect(self.window().create_deck)
        outer_layout.addWidget(new_deck_btn)

        self.window().action_new_deck.setVisible(True)

    def populate_list(self) -> None:
        self._scroll_area_widget_contents = QtWidgets.QWidget()
        self._inner_layout = QtWidgets.QVBoxLayout(
            self._scroll_area_widget_contents)
        self._inner_layout.setAlignment(QtCore.Qt.AlignCenter)
        for deck_name in sorted(os.listdir(config.DECKS_DIR)):
            if deck_name.startswith('.'):
                continue
            frame = QtWidgets.QFrame(self._scroll_area_widget_contents)
            frame.setFrameStyle(QtWidgets.QFrame.Box)
            horizontal_layout = QtWidgets.QHBoxLayout(frame)
            horizontal_layout.setAlignment(QtCore.Qt.AlignCenter)
            label = QtWidgets.QLabel(deck_name, frame)
            label.setFixedWidth(400)
            font = label.font()
            font.setPointSize(12)
            label.setFont(font)
            horizontal_layout.addWidget(label)
            study_btn = QtWidgets.QPushButton(
                QtGui.QIcon(f'{config.ICONS_DIR}book-open.png'), '')
            study_btn.setFixedWidth(32)
            study_btn.setToolTip('Study deck')
            study_btn.released.connect(lambda d=deck_name: self.study_deck(d))
            horizontal_layout.addWidget(study_btn)
            edit_btn = QtWidgets.QPushButton(
                QtGui.QIcon(f'{config.ICONS_DIR}pencil.png'), '')
            edit_btn.setFixedWidth(32)
            edit_btn.setToolTip('Edit deck')
            edit_btn.released.connect(lambda d=deck_name: self.edit_deck(d))
            delete_btn = QtWidgets.QPushButton(
                QtGui.QIcon(f'{config.ICONS_DIR}cross.png'), '')
            delete_btn.setFixedWidth(32)
            delete_btn.setToolTip('Delete deck')
            delete_btn.released.connect(lambda d=deck_name: self.delete_deck(d))
            horizontal_layout.addWidget(study_btn)
            horizontal_layout.addWidget(edit_btn)
            horizontal_layout.addWidget(delete_btn)
            self._inner_layout.addWidget(frame)
        self._scroll_area.setWidget(self._scroll_area_widget_contents)

    def edit_deck(self, name: str) -> None:
        d = deck.load_deck(f'{config.DECKS_DIR}{name}/'
                           + config.DECK_FILE)
        editor_widget.EditorWidget(d, parent=self.window())

    def study_deck(self, name: str) -> None:
        study_widget.StudyWidget(deck.load_deck(
            f'{config.DECKS_DIR}{name}/{config.DECK_FILE}'),
            parent=self.window())

    def delete_deck(self, deck_name: str = None) -> None:
        if deck_name is None:
            dlg = SelectDeckDialog('delete', self)
            if dlg.exec():
                deck_name = dlg.deck_name
        if deck_name is not None:
            dialog = QtWidgets.QMessageBox(parent=self.window())
            dialog.setText(f'Are you sure you want delete {deck_name} deck?')
            dialog.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            if dialog.exec() == QtWidgets.QMessageBox.Ok:
                d = deck.load_deck(
                    f'{config.DECKS_DIR}{deck_name}/'
                    + config.DECK_FILE)
                d.delete()
            self.populate_list()

    def exit(self) -> None:
        pass


class SelectDeckDialog(QtWidgets.QDialog):

    def __init__(self, action: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle(f'Select deck to {action}')
        self.resize(400, 150)
        self.setMinimumSize(self.size())
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self._combo_box = QtWidgets.QComboBox()
        for deck_name in sorted(os.listdir(config.DECKS_DIR)):
            if deck_name.startswith('.'):
                continue
            self._combo_box.addItem(deck_name)
        layout.addWidget(self._combo_box)

        q_btn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        button_box = QtWidgets.QDialogButtonBox(q_btn, parent=self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self, *args, **kwargs) -> None:
        super().accept()
        self.deck_name = self._combo_box.currentText()
