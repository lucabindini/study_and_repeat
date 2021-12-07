import os

from PyQt5 import QtWidgets, QtCore, QtGui

from model import deck
from view import editor_widget, study_widget
import config


class HomeWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        horizontal_layout = QtWidgets.QHBoxLayout(self)
        self._scroll_area = QtWidgets.QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area_widget_contents = QtWidgets.QWidget()
        self._vertical_layout = QtWidgets.QVBoxLayout(
            self._scroll_area_widget_contents)
        self._vertical_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.populate_list()
        horizontal_layout.addWidget(self._scroll_area)

    def populate_list(self) -> None:
        for deck_name in sorted(os.listdir(config.DECKS_DIR)):
            widget = QtWidgets.QWidget(self._scroll_area_widget_contents)
            horizontal_layout = QtWidgets.QHBoxLayout(widget)
            horizontal_layout.setAlignment(QtCore.Qt.AlignCenter)
            line_edit = QtWidgets.QLineEdit(deck_name, widget)
            line_edit.setReadOnly(True)
            line_edit.setMaximumWidth(400)
            horizontal_layout.addWidget(line_edit)
            study_btn = QtWidgets.QPushButton(
                QtGui.QIcon(f'{config.ICONS_DIR}book-open.png'), '')
            study_btn.setFixedWidth(32)
            study_btn.released.connect(lambda d=deck_name: self.study_deck(d))
            horizontal_layout.addWidget(study_btn)
            edit_btn = QtWidgets.QPushButton(
                QtGui.QIcon(f'{config.ICONS_DIR}pencil.png'), '')
            edit_btn.setFixedWidth(32)
            edit_btn.released.connect(lambda d=deck_name: self.edit_deck(d))
            horizontal_layout.addWidget(edit_btn)
            self._vertical_layout.addWidget(widget)
        self._scroll_area.setWidget(self._scroll_area_widget_contents)

    def edit_deck(self, name: str) -> None:
        d = deck.load_deck(f'{config.DECKS_DIR}{name}/'
                           + config.DECK_FILE)
        editor_widget.EditorWidget(d, parent=self.window())

    def study_deck(self, name: str) -> None:
        study_widget.StudyWidget(deck.load_deck(
            f'{config.DECKS_DIR}{name}/{config.DECK_FILE}'),
            parent=self.window())

    def exit(self) -> None:
        pass
