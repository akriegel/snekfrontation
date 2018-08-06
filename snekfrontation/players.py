from abc import ABC, abstractmethod


class Player(ABC):

    def __init__(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

class Sauron(ABC):
    """
    Singleton class for the Sauron player.
    """

    def __init__(self):
        pass

    @property
    def name(self):
        return 'Sauron'


class Fellowship:
    """
    Singleton class for the Fellowship player.
    """

    def __init__(self):
        pass

    @property
    def name(self):
        return 'Fellowship'
