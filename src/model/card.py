import dataclasses


@dataclasses.dataclass
class Card:
    identifier: int
    question: str
    answer: str
