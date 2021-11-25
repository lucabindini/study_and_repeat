import pickle
import datetime
import collections

from model import card


class Deck:

    def __init__(self, name: str) -> None:
        self._name = name
        self._cards = []
        self._current_id = 0
        self.last_study_day = datetime.date.today()
        self._cards_strengths = {}
        self._queues = []
        self._new_queue = collections.deque()
        self._is_new = True

    def add_card(self, question: str, answer: str) -> None:
        self._cards.append(card.Card(self._current_id, question, answer))
        self._cards_strengths[self._current_id] = 1
        self._new_queue.append(self._cards[-1])
        self._current_id += 1

    def get_card(self) -> card.Card:
        for _ in range(2):
            try:
                return (self._new_queue if self._is_new else self._queues[0])[0]
            except IndexError:
                self._is_new = not self._is_new
        raise EmptyQueuesException()

    def calculate_delay(self, correctness: bool) -> None:
        c = (self._new_queue if self._is_new else self._queues[0]).popleft()
        self._is_new = not self._is_new
        if correctness:
            while len(self._queues) <= self._cards_strengths[c.identifier]:
                self._queues.append(collections.deque())
            self._queues[self._cards_strengths[c.identifier]].append(c)
            self._cards_strengths[c.identifier] *= 2
        else:
            self._cards_strengths[c.identifier] = 1
            self._queues[0].append(c)

    def dump(self):
        with open('decks/'+self._name+'.pickle', 'wb') as f:
            pickle.dump(self, f)


def load_deck(filepath: str) -> Deck:
    with open(filepath, 'rb') as f:
        d: Deck = pickle.load(f)
    n = (datetime.date.today() - d.last_study_day).days
    for i in range(n):
        d._queues[0].extend(d._queues[i+1])
    del d._queues[1:n+1]
    d.last_study_day = datetime.date.today()
    return d


class EmptyQueuesException(Exception):

    def __init__(self) -> None:
        self.message = 'Both queues are empty.'
