from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *argv, **kwarg):
        super().__init__(*argv, **kwarg)

        widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addWidget(QtWidgets.QLabel('question'))
        self._answer_label = QtWidgets.QLabel('answer')
        top_layout.addWidget(self._answer_label)
        self._buttons = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout()
        button_incorrect = QtWidgets.QPushButton('Incorrect')
        button_layout.addWidget(button_incorrect)
        button_incorrect.pressed.connect(self.next_question)
        button_correct = QtWidgets.QPushButton('Correct')
        button_layout.addWidget(button_correct)
        button_correct.pressed.connect(self.next_question)
        self._buttons.setLayout(button_layout)
        self._show_button = QtWidgets.QPushButton('Show answer')
        self._show_button.pressed.connect(self.show_answer)
        top_layout.addWidget(self._show_button)
        top_layout.addWidget(self._buttons)
        self._buttons.hide()
        self._answer_label.hide()
        widget.setLayout(top_layout)
        self.setCentralWidget(widget)

    def show_answer(self):
        self._show_button.hide()
        self._buttons.show()
        self._answer_label.show()

    def next_question(self):
        self._buttons.hide()
        self._show_button.show()
        self._answer_label.hide()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
