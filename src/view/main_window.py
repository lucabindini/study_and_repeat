import re

from PyQt5 import QtWidgets, QtGui, QtCore

from view import home_widget, editor_widget
from model import deck
import config


class self(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(config.LOGO_PATH))
        self.setWindowTitle('Study and Repeat')
        self.resize(800, 600)
        self.setMinimumSize(self.size())
        self.setCentralWidget(home_widget.HomeWidget())

        menubar = QtWidgets.QMenuBar(self)

        menu_file = QtWidgets.QMenu(menubar)
        # menu_export_deck = QtWidgets.QMenu(menu_file)
        self.setMenuBar(menubar)
        self.action_new_deck = QtWidgets.QAction(self)
        action_quit = QtWidgets.QAction(self)
        # action_import_deck = QtWidgets.QAction(self)
        # action_local_export = QtWidgets.QAction(self)
        # action_remote_export = QtWidgets.QAction(self)
        action_delete_deck = QtWidgets.QAction(self)
        # menu_export_deck.addAction(action_local_export)
        # menu_export_deck.addAction(action_remote_export)
        menu_file.addAction(self.action_new_deck)
        # menu_file.addAction(action_import_deck)
        # menu_file.addAction(menu_export_deck.menuAction())
        menu_file.addAction(action_delete_deck)
        menu_file.addAction(action_quit)
        menubar.addAction(menu_file.menuAction())
        # menu_help = QtWidgets.QMenu(menubar)
        # action_about = QtWidgets.QAction(self)
        # menu_help.addAction(action_about)
        # menubar.addAction(menu_help.menuAction())

        menu_file.setTitle(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'File'))
        # menu_export_deck.setTitle(QtCore.QCoreApplication.translate(
        #     'Study and Repeat', 'Export deck'))
        # menu_help.setTitle(QtCore.QCoreApplication.translate(
        #     'Study and Repeat', 'Help'))
        self.action_new_deck.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'New deck'))
        # action_about.setText(QtCore.QCoreApplication.translate(
        #     'Study and Repeat', 'About'))
        action_quit.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Quit'))
        # action_import_deck.setText(QtCore.QCoreApplication.translate(
        #     'Study and Repeat', 'Import deck'))
        # action_local_export.setText(QtCore.QCoreApplication.translate(
        #     'Study and Repeat', 'Local export'))
        # action_remote_export.setText(QtCore.QCoreApplication.translate(
        #     'Study and Repeat', 'Remote export'))
        action_delete_deck.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Delete deck'))

        self.action_new_deck.triggered.connect(self.create_deck)
        action_quit.triggered.connect(self.close)
        action_delete_deck.triggered.connect(
            lambda: self.centralWidget().delete_deck())

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

        self._error_label = QtWidgets.QLabel('The only permitted characters are '
                                             + 'a-z, A-Z, 0-9 and _')
        self._error_label.setStyleSheet("color: #ff0000")
        layout.addWidget(self._error_label)
        self._error_label.hide()

        self._line_edit = QtWidgets.QLineEdit(self)
        self._line_edit.setPlaceholderText('Insert deck name')
        layout.addWidget(self._line_edit)

        q_btn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        button_box = QtWidgets.QDialogButtonBox(q_btn, parent=self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self, *args, **kwargs) -> None:
        if re.fullmatch('[a-zA-Z0-9_]+', self._line_edit.text()) is None:
            self._error_label.show()
        else:
            super().accept()
            self.deck = deck.Deck(self._line_edit.text())
