import os
import re
import tarfile

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
        new_deck_btn.released.connect(self.create_deck)
        outer_layout.addWidget(new_deck_btn)

        self.window().action_new_deck.setVisible(True)
        self.window().action_export_deck.setVisible(True)
        self.window().action_import_deck.setVisible(True)
        self.window().action_reset_deck.setVisible(True)
        self.window().action_delete_deck.setVisible(True)

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
            label = DoubleClickedQLabel(deck_name, frame)
            label.setFixedWidth(400)
            font = label.font()
            font.setPointSize(12)
            label.setFont(font)
            label.setToolTip('Double click to rename')
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
            delete_btn.released.connect(
                lambda d=deck_name: self.delete_deck(d))
            horizontal_layout.addWidget(study_btn)
            horizontal_layout.addWidget(edit_btn)
            horizontal_layout.addWidget(delete_btn)
            self._inner_layout.addWidget(frame)
        self._scroll_area.setWidget(self._scroll_area_widget_contents)

    def create_deck(self) -> None:
        dlg = NameDeckDialog(is_new_deck=True, parent=self.window())
        if dlg.exec():
            d = deck.Deck(dlg.deck_name)
            editor_widget.EditorWidget(d, parent=self.window())

    def edit_deck(self, name: str) -> None:
        d = deck.Deck.load(f'{config.DECKS_DIR}{name}/'
                           + config.DECK_FILE)
        editor_widget.EditorWidget(d, parent=self.window())

    def study_deck(self, name: str) -> None:
        study_widget.StudyWidget(deck.Deck.load(
            f'{config.DECKS_DIR}{name}/{config.DECK_FILE}'),
            parent=self.window())

    def reset_deck(self) -> None:
        dlg = SelectDeckDialog('reset', self)
        deck_name = None
        if dlg.exec():
            deck_name = dlg.deck_name
        if deck_name is None or QtWidgets.QMessageBox.question(
                self.window(), 'Reset deck',
                'Are you sure you want to reset all of the scheduling '
                + f'information for {repr(deck_name)} deck?') \
                == QtWidgets.QMessageBox.No:
            return
        d = deck.Deck.load(
            f'{config.DECKS_DIR}{deck_name}/{config.DECK_FILE}')
        d.reset()
        d.dump()
        # self.populate_list()

    def delete_deck(self, deck_name: str = None) -> None:
        if deck_name is None:
            dlg = SelectDeckDialog('delete', self)
            if dlg.exec():
                deck_name = dlg.deck_name
        if deck_name is None or QtWidgets.QMessageBox.question(
                self.window(), 'Delete deck',
                f'Are you sure you want to delete {repr(deck_name)} deck?') \
                == QtWidgets.QMessageBox.No:
            return
        d = deck.Deck.load(
            f'{config.DECKS_DIR}{deck_name}/{config.DECK_FILE}')
        d.delete()
        self.populate_list()

    def export_deck(self) -> None:
        dialog = SelectDeckDialog('export', self)
        if not dialog.exec():
            return
        deck_name = dialog.deck_name
        directory = QtWidgets.QFileDialog.getExistingDirectory(self.window())
        path = f'{directory}/{deck_name}.tar'
        if os.access(path, os.F_OK) and QtWidgets.QMessageBox.question(
                self.window(), 'File already exists',
                f'A file called "{deck_name}.tar" already exists in the '
                + 'selected directory. Do you want to overwrite it?') \
                == QtWidgets.QMessageBox.No:
            return
        d = deck.Deck.load(
            f'{config.DECKS_DIR}{deck_name}/{config.DECK_FILE}')
        d.export(path)

    def import_deck(self) -> None:
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            parent=self.window(), filter='Archive (*.tar)')[0]
        try:
            with tarfile.open(file_name) as tar:
                if os.access(f'{config.DECKS_DIR}{tar.getnames()[0]}',
                             os.F_OK) \
                    and QtWidgets.QMessageBox.question(
                        self.window(), 'Deck already exists',
                        f'A deck called {repr(tar.getnames()[0])} already '
                        + 'exists. Do you want to overwrite it?') \
                        == QtWidgets.QMessageBox.No:
                    return
                tar.extractall(config.DECKS_DIR)
        except ValueError:
            pass
        else:
            self.populate_list()

    def exit(self) -> None:
        pass


class DoubleClickedQLabel(QtWidgets.QLabel):

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        dlg = NameDeckDialog(parent=self.window())
        if dlg.exec():
            deck.Deck.load(
                f'{config.DECKS_DIR}{self.text()}/{config.DECK_FILE}')\
                .rename(dlg.deck_name)
            self.window().centralWidget().populate_list()


class NameDeckDialog(QtWidgets.QDialog):

    def __init__(self, is_new_deck: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._is_new_deck = is_new_deck
        if self._is_new_deck:
            self.setWindowTitle('Create deck')
        else:
            self.setWindowTitle('Rename deck')
        self.resize(400, 150)
        self.setMinimumSize(self.size())
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self._syntax_error_label = QtWidgets.QLabel(
            'The only permitted characters are a-z, A-Z, 0-9 and _')
        self._syntax_error_label.setStyleSheet("color: #ff0000")
        layout.addWidget(self._syntax_error_label)
        self._syntax_error_label.hide()

        self._exist_error_label = QtWidgets.QLabel(
            'Two decks cannot have the same name')
        self._exist_error_label.setStyleSheet("color: #ff0000")
        layout.addWidget(self._exist_error_label)
        self._exist_error_label.hide()

        self._line_edit = QtWidgets.QLineEdit(self)
        self._line_edit.setPlaceholderText('Insert deck name')
        layout.addWidget(self._line_edit)

        q_btn = QtWidgets.QDialogButtonBox.Ok \
            | QtWidgets.QDialogButtonBox.Cancel
        button_box = QtWidgets.QDialogButtonBox(q_btn, parent=self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self, *args, **kwargs) -> None:
        if re.fullmatch('[a-zA-Z0-9_]+', self._line_edit.text()) is None:
            self._syntax_error_label.show()
        elif os.access(f'{config.DECKS_DIR}{self._line_edit.text()}', os.F_OK):
            self._exist_error_label.show()
        else:
            super().accept()
            self.deck_name = self._line_edit.text()


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

        q_btn = QtWidgets.QDialogButtonBox.Ok \
            | QtWidgets.QDialogButtonBox.Cancel
        button_box = QtWidgets.QDialogButtonBox(q_btn, parent=self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self, *args, **kwargs) -> None:
        super().accept()
        self.deck_name = self._combo_box.currentText()
