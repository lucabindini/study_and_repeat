from PyQt5 import QtWidgets, QtGui, QtCore
import qdarkstyle

from view import home_widget
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
        self.action_create_deck = QtWidgets.QAction(self)
        self.action_export_deck = QtWidgets.QAction(self)
        self.action_import_deck = QtWidgets.QAction(self)
        self.action_reset_deck = QtWidgets.QAction(self)
        self.action_delete_deck = QtWidgets.QAction(self)
        action_quit = QtWidgets.QAction(self)
        menu_file.addAction(self.action_create_deck)
        menu_file.addAction(self.action_export_deck)
        menu_file.addAction(self.action_import_deck)
        menu_file.addAction(self.action_reset_deck)
        menu_file.addAction(self.action_delete_deck)
        menu_file.addAction(action_quit)
        menubar.addAction(menu_file.menuAction())
        menu_help = QtWidgets.QMenu(menubar)
        action_about = QtWidgets.QAction(self)
        menu_help.addAction(action_about)
        menubar.addAction(menu_help.menuAction())

        menu_file.setTitle(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'File'))
        menu_help.setTitle(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Help'))
        self.action_create_deck.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Create deck'))
        action_about.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'About'))
        self.action_export_deck.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Export deck'))
        self.action_import_deck.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Import deck'))
        self.action_reset_deck.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Reset deck'))
        self.action_delete_deck.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Delete deck'))
        action_quit.setText(QtCore.QCoreApplication.translate(
            'Study and Repeat', 'Quit'))

        self.action_create_deck.triggered.connect(
            lambda: self.centralWidget().create_deck())
        self.action_export_deck.triggered.connect(
            lambda: self.centralWidget().export_deck())
        self.action_import_deck.triggered.connect(
            lambda: self.centralWidget().import_deck())
        self.action_reset_deck.triggered.connect(
            lambda: self.centralWidget().reset_deck())
        self.action_delete_deck.triggered.connect(
            lambda: self.centralWidget().delete_deck())
        action_quit.triggered.connect(self.close)
        action_about.triggered.connect(self.about)

        self.setCentralWidget(home_widget.HomeWidget(parent=self))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.centralWidget().exit()
        return super().closeEvent(a0)

    def about(self) -> None:
        QtWidgets.QMessageBox.about(
            self, 'About Study and Repeat',
            '<h2>Study and Repeat</h2>'
            '<p>Version 1.0</p>'
            '<p>Study and Repeat is an application aimed at improving the '
            'quality of the study, through the technique of spaced repetition.'
            '</p>'
            '<p>Study and Repeat is free software licensed under '
            '<a href="https://www.gnu.org/licenses/gpl-3.0.html">GPLv3</a>.</p>'
            '<p>You can find all of the source code for the application on '
            '<a href="https://github.com/lucabindini/study_and_repeat">'
            'GitHub</a>.</p>'
            '<p>Creators: '
            '<a href="https://github.com/marcobenelli">Marco Benelli</a>, '
            '<a href="https://github.com/lucabindini">Luca Bindini</a></p>')
