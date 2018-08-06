from abc import ABC, abstractmethod


class Piece(ABC):

    @abstractmethod
    def name(self):
        pass
