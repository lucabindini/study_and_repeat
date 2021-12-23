import dataclasses

from PyQt5 import QtCore


@dataclasses.dataclass
class Card:
    identifier: int
    question: str
    _answer: str

    def set_answer(self, answer: str) -> None:
        self._answer = answer.replace(QtCore.QStandardPaths.writableLocation(
            QtCore.QStandardPaths.AppDataLocation), '<//>')

    def get_answer(self) -> str:
        return self._answer.replace('<//>',
                                    QtCore.QStandardPaths.writableLocation(
                                        QtCore.QStandardPaths.AppDataLocation))
