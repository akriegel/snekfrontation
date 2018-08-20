from abc import ABC, abstractmethod


class Player(ABC):

    def __init__(self):
        pass

    def __str__(self) -> str:
        return self.name

    @property
    @abstractmethod
    def name(self):
        pass


class Sauron(Player):
    """
    Singleton class for the Sauron player.
    """

    def __init__(self, hand=None):
        self.hand = hand or setup_sauron_hand()

    @property
    def name(self):
        return 'Sauron'


class Fellowship(Player):
    """
    Singleton class for the Fellowship player.
    """

    def __init__(self, hand=None):
        self.hand = hand or setup_fellowship_hand()

    @property
    def name(self):
        return 'Fellowship'


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

    def __str__(self) -> str:
        return f'{self.value} ({self.allegiance.name})'

    @property
    def allegiance(self) -> Player:
        return self._allegiance

    @property
    def value(self) -> int:
        return self._value

    @property
    def text(self) -> str:
        return ''


class TextCard(Card):

    def __init__(self, allegiance: Player, text: str):
        self._allegiance = allegiance
        self._text = text

    def __str__(self) -> str:
        return f'{self.text} ({self.allegiance.name})'

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


def setup_sauron_hand():
    return [NumberCard(Sauron, 0)]


def setup_fellowship_hand():
    return [NumberCard(Fellowship, 0)]
