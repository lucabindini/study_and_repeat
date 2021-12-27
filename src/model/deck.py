import collections
import datetime
import glob
import os
import pickle
import shutil
import tarfile
import typing

from model import card
import config


DeckT = typing.TypeVar('DeckT', bound='Deck')


class Deck:

    def __init__(self, name: str) -> None:
        self.name = name
        self.cards: list[card.Card] = []
        self.last_study_day = datetime.date.today()
        self._current_id = 0
        self._cards_strengths: dict[int, int] = {}
        self._queues: list[collections.deque[card.Card]] = [
            collections.deque()]
        self._new_queue: collections.deque[card.Card] = collections.deque()
        self._is_new = True
        self._img_id = 0
        os.makedirs(f'{config.DECKS_DIR}{name}/{config.IMG_DIR}')

    @staticmethod
    def load(filepath: str) -> DeckT:
        with open(filepath, 'rb') as f:
            d: Deck = pickle.load(f)
        n = min((datetime.date.today() - d.last_study_day).days,
                len(d._queues)-1)
        for i in range(n):
            d._queues[0].extend(d._queues[i+1])
        del d._queues[1:n+1]
        d.last_study_day = datetime.date.today()
        return d

    def add_card(self, question: str, answer: str) -> None:
        self.cards.append(card.Card(self._current_id,
                          self.name, question, answer))
        self._cards_strengths[self._current_id] = 1
        self._new_queue.append(self.cards[-1])
        self._current_id += 1

    def remove_card(self, index: int) -> None:
        c = self.cards[index]
        for queue in self._queues:
            try:
                queue.remove(c)
            except ValueError:
                pass
            else:
                break
        else:
            self._new_queue.remove(c)
        del self._cards_strengths[c.identifier]
        del self.cards[index]
        for f in glob.iglob(f'{config.DECKS_DIR}{self.name}/'
                            + f'{config.IMG_DIR}{c.identifier}-*'):
            os.remove(f)

    def move_card(self, index: int, up: bool) -> None:
        c = self.cards[index]
        c1 = self.cards[index - (2*up-1)]
        try:
            i = self._new_queue.index(c)
            i1 = self._new_queue.index(c1)
            self._new_queue[i], self._new_queue[i1] \
                = self._new_queue[i1], self._new_queue[i]
        except ValueError:
            pass
        self.cards[index - (2*up-1)], self.cards[index] = \
            self.cards[index],  self.cards[index - (2*up-1)]

    def add_image(self, src: str, index: int) -> str:
        dst = f'{config.DECKS_DIR}{self.name}/{config.IMG_DIR}' \
            + f'{self.cards[index].identifier}-' \
            + f'{self._img_id}-{os.path.basename(src)}'
        shutil.copyfile(src, dst)
        self._img_id += 1
        return dst

    def get_card(self) -> card.Card:
        for _ in range(2):
            try:
                return (self._new_queue if self._is_new else self._queues[0])[0]
            except IndexError:
                self._is_new = not self._is_new
        raise EmptyQueuesException()

    def calculate_delay(self, correctness: bool) -> None:
        c = (self._new_queue if self._is_new else self._queues[0]).popleft()

        # to avoid asking the same question twice in a row
        if self._queues[0]:
            self._is_new = not self._is_new

        if correctness:
            while len(self._queues) <= self._cards_strengths[c.identifier]:
                self._queues.append(collections.deque())
            self._queues[self._cards_strengths[c.identifier]].append(c)
            self._cards_strengths[c.identifier] *= 2
        else:
            self._cards_strengths[c.identifier] = 1
            self._queues[0].append(c)

    def dump(self) -> None:
        with open(f'{config.DECKS_DIR}{self.name}/{config.DECK_FILE}',
                  'wb') as f:
            pickle.dump(self, f)

    def rename(self, name: str) -> None:
        os.rename(f'{config.DECKS_DIR}{self.name}',
                  f'{config.DECKS_DIR}{name}')
        self.name = name
        for c in self.cards:
            c.deck_name = name
        self.dump()

    def reset(self) -> None:
        self._new_queue = collections.deque(self.cards)
        self._queues = [collections.deque()]
        self._cards_strengths = {c.identifier: 1 for c in self.cards}

    def delete(self) -> None:
        shutil.rmtree(f'{config.DECKS_DIR}{self.name}')

    def export(self, file_name: str, reset: bool) -> None:
        if reset:
            self.reset()
            try:
                shutil.rmtree(f'{config.TEMP_DIR}{self.name}')
            except FileNotFoundError:
                pass
            shutil.copytree(f'{config.DECKS_DIR}{self.name}',
                            f'{config.TEMP_DIR}{self.name}')
            with open(f'{config.TEMP_DIR}{self.name}/{config.DECK_FILE}',
                      'wb') as f:
                pickle.dump(self, f)
            tar_dir = config.TEMP_DIR
        else:
            tar_dir = config.DECKS_DIR

        with tarfile.open(file_name, 'w') as tar:
            tar.add(f'{tar_dir}{self.name}', self.name)
        if reset:
            shutil.rmtree(f'{config.TEMP_DIR}{self.name}')

    def new_count(self):
        return len(self._new_queue)

    def today_count(self):
        return len(self._queues[0])


class EmptyQueuesException(Exception):

    def __init__(self) -> None:
        self.message = 'Both queues are empty.'
