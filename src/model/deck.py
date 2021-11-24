import pickle

from model import card


class Deck:

    def __init__(self, name: str) -> None:
        self._name = name
        self._cards = []
        self._index = -1

    def add_card(self, card: card.Card) -> None:
        self._cards.append(card)

    def get_card(self) -> card.Card:
        if self._cards:
            self._index += 1
            return self._cards[self._index]
        else:
            raise IndexError()

    def dump(self):
        with open('decks/'+self._name+'.pickle', 'wb') as f:
            pickle.dump(self, f)


def load_deck(filepath: str) -> Deck:
    with open(filepath, 'rb') as f:
        return pickle.load(f)
