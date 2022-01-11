from PyQt5 import QtWidgets, QtCore

from view import secondary_widget


class EndStudyWidget(secondary_widget.SecondaryWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        v_layout = QtWidgets.QVBoxLayout()
        end_study_label = QtWidgets.QLabel(
            f'Congratulations you are done studying {repr(self._deck.name)}'
            ' for today.\nClick the button on the top left'
            ' to get back to the home.')
        end_study_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(end_study_label)

        self._central_widget.setLayout(v_layout)

    def exit(self) -> None:
        pass
