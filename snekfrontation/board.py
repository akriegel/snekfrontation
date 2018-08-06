from snekfrontation.piece import Piece
from snekfrontation.constants import FELLOWSHIP, SAURON


class Space:
    """
    A single space on the board.
    """

    def __init__(self, name, capacity, occupied_by=None):
        self.name = name
        self.capacity = capacity
        self.occupied_by = occupied_by


class Board:
    """
    Singleton class for the game board.
    """
    
    def __init__(self):
        self.rows = [
            Space('Mordor', 4, SAURON),
            # TODO
        ]
