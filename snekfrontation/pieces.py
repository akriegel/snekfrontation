"""
Define the classes for constructing game pieces, as well as some dummy piece
instances for testing.
"""

from abc import ABC, abstractmethod

from snekfrontation.players import Player, Fellowship, Sauron


class Piece(ABC):
    """
    Abstract base class for all game pieces.
    """

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> hash:
        return hash(self.name)

    def __str__(self) -> str:
        return f'{self.name} ({self.strength})'

    @property
    @abstractmethod
    def allegiance(self) -> Player:
        """
        Return whether this piece belongs to Sauron or Fellowship.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the name of this piece, which must be a unique identifier.
        """
        pass

    @property
    @abstractmethod
    def strength(self) -> int:
        """
        Return the strength number on this piece.
        """
        pass

    @property
    @abstractmethod
    def is_revealed(self) -> bool:
        """
        Indicate whether the piece is permanently revealed (by Crebain etc.)
        """
        pass


class SauronPiece(Piece):
    """
    A piece belonging to Sauron.
    """

    def __init__(self, name: str, strength: int):
        self._name = name
        self._strength = strength
        self._is_revealed = False

    @property
    def allegiance(self):
        return Sauron

    @property
    def name(self):
        return self._name

    @property
    def strength(self) -> int:
        return self._strength

    @property
    def is_revealed(self) -> bool:
        return self._is_revealed

    def reveal(self):
        self._is_revealed = True


class FellowshipPiece(Piece):
    """
    A piece belonging to Fellowship.
    """

    def __init__(self, name: str, strength: int):
        self._name = name
        self._strength = strength
        self._is_revealed = False

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

    @property
    def is_revealed(self) -> bool:
        return self._is_revealed

    def reveal(self):
        self._is_revealed = True


DummyFellowshipPiece = FellowshipPiece('Dummy', 1)
DummySauronPiece = SauronPiece('Dummy', 1)
