import os
import re

from PyQt5 import QtWidgets, QtGui, QtCore
import qdarkstyle

from view import home_widget, editor_widget
from model import deck
import config


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(config.LOGO_PATH))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.resize(800, 600)
        self.setMinimumSize(self.size()/2)

        menubar = QtWidgets.QMenuBar(self)

        menu_file = QtWidgets.QMenu(menubar)
        self.setMenuBar(menubar)
        self.action_new_deck = QtWidgets.QAction(self)
        action_quit = QtWidgets.QAction(self)
        self.action_import = QtWidgets.QAction(self)
        self.action_export = QtWidgets.QAction(self)
        self.action_delete_deck = QtWidgets.QAction(self)
        menu_file.addAction(self.action_new_deck)
        menu_file.addAction(self.action_export)
        menu_file.addAction(self.action_import)
        menu_file.addAction(self.action_delete_deck)
        menu_file.addAction(action_quit)
        menubar.addAction(menu_file.menuAction())
        # menu_help = QtWidgets.QMenu(menubar)
        # action_about = QtWidgets.QAction(self)
        # menu_help.addAction(action_about)
        # menubar.addAction(menu_help.menuAction())

        menu_file.setTitle(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'File'))
        # menu_help.setTitle(QtCore.QCoreApplication.translate(
        #     'Study and Repeat', 'Help'))
        self.action_new_deck.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'New deck'))
        # action_about.setText(QtCore.QCoreApplication.translate(
        #     'Study and Repeat', 'About'))
        action_quit.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Quit'))
        self.action_import.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Import deck'))
        self.action_export.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Export deck'))
        self.action_delete_deck.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Delete deck'))

        self.action_new_deck.triggered.connect(self.create_deck)
        action_quit.triggered.connect(self.close)
        self.action_delete_deck.triggered.connect(
            lambda: self.centralWidget().delete_deck())
        self.action_export.triggered.connect(
            lambda: self.centralWidget().export_deck())
        self.action_import.triggered.connect(
            lambda: self.centralWidget().import_deck())

        self.setCentralWidget(home_widget.HomeWidget(parent=self))

    def create_deck(self) -> None:
        dlg = NewDeckDialog(self)
        if dlg.exec():
            editor_widget.EditorWidget(dlg.deck, parent=self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.centralWidget().exit()
        return super().closeEvent(a0)


class NewDeckDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Create deck')
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
            self.deck = deck.Deck(self._line_edit.text())
