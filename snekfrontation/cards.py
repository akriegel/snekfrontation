from abc import ABC, abstractmethod

from snekfrontation.players import Player, Fellowship, Sauron


class Card(ABC):

    @property
    @abstractmethod
    def value(self) -> int:
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @property
    @abstractmethod
    def allegiance(self) -> Player:
        pass


class NumberCard(Card):

    def __init__(self, allegiance: Player, value: int):
        self._allegiance = allegiance
        self._value = value

    @property
    def allegiance(self) -> Player:
        return self._allegiance

    @property
    def value(self) -> int:
        return self.value

    @property
    def text(self) -> str:
        return ''


class TextCard(Card):

    def __init__(self, allegiance: Player, text: str):
        self._allegiance = allegiance
        self._text = text

    @property
    def allegiance(self) -> Player:
        return self._allegiance

    @property
    def value(self) -> int:
        return 0

    @property
    def text(self) -> str:
        return self._text


DummyFellowshipCard = NumberCard(Fellowship, 0)
DummySauronCard = NumberCard(Sauron, 0)
