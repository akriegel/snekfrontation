from abc import ABC, abstractmethod

from snekfrontation.cards import NumberCard


class Player(ABC):

    def __init__(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass


class Sauron:
    """
    Singleton class for the Sauron player.
    """

    def __init__(self, hand=None):
        self.hand = hand or setup_sauron_hand()

    @property
    def name(self):
        return 'Sauron'


class Fellowship:
    """
    Singleton class for the Fellowship player.
    """

    def __init__(self, hand=None):
        self.hand = hand or setup_fellowship_hand()

    @property
    def name(self):
        return 'Fellowship'


def setup_sauron_hand():
    return [NumberCard(0)]


def setup_fellowship_hand():
    return [NumberCard(0)]
