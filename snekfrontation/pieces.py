from abc import ABC, abstractmethod

from snekfrontation.players import Fellowship, Sauron


class Piece(ABC):

    @property
    @abstractmethod
    def allegiance(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def strength(self) -> int:
        pass


class SauronPiece(Piece):

    def __init__(self, name: str, strength: int):
        self._name = name
        self._strength = strength

    @property
    def allegiance(self):
        return Sauron

    @property
    def name(self):
        return self._name

    @property
    def strength(self) -> int:
        return self._strength


class FellowshipPiece(Piece):

    def __init__(self, name: str, strength: int):
        self._name = name
        self._strength = strength

    @property
    def allegiance(self):
        return Fellowship

    @property
    def name(self):
        return self._name

    @property
    def strength(self) -> int:
        return self._strength

    @property
    def has_ring(self):
        pass


DummyFellowshipPiece = FellowshipPiece('Dummy', 1)
DummySauronPiece = SauronPiece('Dummy', 1)
