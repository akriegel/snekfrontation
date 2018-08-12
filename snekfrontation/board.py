from typing import List, Tuple

from snekfrontation.piece import Piece
from snekfrontation.players import Player


Coordinate = Tuple[int, int]


class Space:
    """
    A single space on the board.

    Args:
        name: name for display purposes (static)
        capacity: piece capacity (static)
        player (Player): player currently controlling space
    """

    def __init__(self, name, capacity, pieces=None):
        self.name = name
        self.capacity = capacity
        self.pieces = pieces or []

    @property
    def player(self):
        if not self.pieces:
            return None
        return self.pieces[0].player

    @property
    def population(self):
        return len(self.pieces)

    def is_full(self):
        return self.population == self.capacity


class Move:
    """
    Args:
        player (Player): player initiating move
        src (Tuple[int, int]): coordinates for starting the move
        dst (Tuple[int, int]): coordinates for ending the move
    """

    def __init__(
        self,
        player: Player,
        piece: Piece,
        src: Coordinate,
        dst: Coordinate,
    ):
        self.player = player
        self.piece = piece
        self.src = src
        self.dst = dst


class Board:
    """
    Singleton class for the game board.
    """

    def __init__(self):
        self.spaces = [
            [Space('Mordor', 4)],
            [
                Space('Dagorlad', 2),
                Space('Gondor', 2)
            ],
            [
                Space('Mirkwood', 2),
                Space('Fangorn', 2),
                Space('Rohan', 2),
            ],
            [
                Space('Hoher Pass', 1),
                Space('Misty Mountains', 1),
                Space('Caradhorse (Moria)', 1),
                Space('Gap of Rohan', 1),
            ],
            [
                Space('Rhudaur', 2),
                Space('Eregoin', 2),
                Space('Enedwaith', 2),
            ],
            [
                Space('Arthedain', 2),
                Space('Cardolan', 2),
            ],
            [Space('Alienland', 2)],
        ]

    def get_space(self, coordinates):
        return self.board[coordinates[0]][coordinates[1]]

    def is_move_valid(self, move):
        """
        Return:
            bool: if move is an attack
        """
        if move.src[0] < 0 or move.src[0] > 7:
            raise ValueError('starting index off the board')
        if move.src[1] > (4 - abs(move.src[0] - 3)):
            raise ValueError('starting index off the board')
        if move.dst[0] < 0 or move.dst[0] > 7:
            raise ValueError('destination index off the board')
        if move.dst[1] > (4 - abs(move.dst[0] - 3)):
            raise ValueError('destination index off the board')

        move.src_space = self.spaces[move.src[0]][move.src[1]]
        if piece_number >= move.src_space.population or piece_number < 0:
            raise ValueError('wrong piece number')

        piece = space_pieces[piece_number]
        if type(piece.player) != type(player):
            raise ValueError('wrong player')
        if not piece.is_alive():
            raise ValueError('piece is dead')

        move.dst_space = self.spaces[move.dst[0]][move.dst[1]]
        is_attacking = (
            move.dst_space.player
            and player != move.dst_space.player
        )
        if not is_attacking and move.dst_space.is_full():
            raise ValueError('destination is full')

        if is_special_case_for_piece(piece):
            # TODO
            raise NotImplementedError('')

        if is_special_case_for_move(player, move.src, move.dst):
            # TODO
            raise NotImplementedError('')

        if isinstance(player, Sauron):
            if move.src[0] >= move.dst[0]:
                raise ValueError('not moving forward')
            if move.dst[0] - move.src[0] != 1:
                raise ValueError('moving more than one space')
            if move.src[0] < 3:
                if not (move.src[1] <= move.dst[1] <= move.src[1] + 1):
                    raise ValueError('moving too far laterally')
            else:
                if not (move.src[1] - 1 <= move.dst[1] <= move.src[1]):
                    raise ValueError('moving too far laterally')
        else:  # is Fellowship
            if move.dst[0] >= move.src[0]:
                raise ValueError('not moving forward')
            if move.src[0] - move.dst[0] != 1:
                raise ValueError('moving more than one space')
            if move.src[0] > 3:
                if not (move.src[1] <= move.dst[1] <= move.src[1] + 1):
                    raise ValueError('moving too far laterally')
            else:
                if not (move.src[1] - 1 <= move.dst[1] <= move.src[1]):
                    raise ValueError('moving too far laterally')

        return is_attacking

    def valid_moves(
            self, 
            player: Player,
            src: Coordinate,
            piece_number: int,
        ) -> List[Move]:
        """
        TODO: documentation
        """
        valid_moves = []
        #candidate_destinations = [
        #    (i, j)
        #    for i in range(7)
        #    for j in range(4)
        #]
        #for dst in candidate_destinations:
        #    try:
        #        self.is_move_valid(player, src, piece_number, dst)
        #    except ValueError:
        #        continue
        #    valid_moves.append(dst)
        return valid_moves

    def apply_move(self, src, piece_number, dst):
        piece = self.spaces[src[0]][src[1]].pieces.pop(piece_number)
        self.spaces[dst[0]][dst[1]].pieces.append(piece)

    def is_frodo_with_sam(self) -> bool:
        # TODO
        return False


def is_special_case_for_piece(piece):
    """
    TODO
    """
    raise NotImplementedError('')


def is_special_case_for_move(player, src, dst):
    """
    TODO
    """
    raise NotImplementedError('')
