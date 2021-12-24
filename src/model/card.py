import dataclasses

import config


@dataclasses.dataclass
class Card:
    identifier: int
    deck_name: str
    question: str
    _answer: str

    def set_answer(self, answer: str) -> None:
        self._answer = answer.replace(
            f'{config.DECKS_DIR}{self.deck_name}', '<//>')

    def get_answer(self) -> str:
        return self._answer.replace('<//>',
                                    f'{config.DECKS_DIR}{self.deck_name}')
