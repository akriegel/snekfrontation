"""
Define the ``Board`` class to represent the board state in a game.
"""

import copy
from typing import Dict, Generator, List, Optional, Tuple

from snekfrontation.pieces import Piece
from snekfrontation.players import Player, Sauron


Coordinate = Tuple[int, int]
Layout = Dict[Piece, str]


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

    def __iter__(self):
        return iter(self.pieces)

    def __str__(self) -> str:
        pieces_str = ', '.join(map(str, self.pieces))
        return f'{self.name} [{pieces_str}]'

    @property
    def allegiance(self) -> Optional[type]:
        """
        Return the player currently controlling this space, or ``None`` if
        there are no pieces in this space.
        """
        if not self.pieces:
            return None
        return self.pieces[0].allegiance

    @property
    def population(self) -> int:
        """
        Return the number of pieces currently in the space.
        """
        return len(self.pieces)

    def is_full(self) -> bool:
        """
        Indicate whether the space already contains the maximum number of
        pieces it is allowed to contain.
        """
        return self.population == self.capacity

    def get_piece_named(self, piece_name) -> Optional[Piece]:
        try:
            return next(
                piece
                for piece in self.pieces
                if piece.name == piece_name
            )
        except StopIteration:
            return None


DEFAULT_BOARD_SPACES = [
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
        Space('Moria', 1),
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


spaces = DEFAULT_BOARD_SPACES


class Move:
    """
    Class for storing data about a move on the board.

    Args:
        player (Player): player initiating move
        piece (Piece): piece to move
        src (Coordinate): coordinates for starting the move
        dst (Coordinate): coordinates for ending the move
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

    def __str__(self) -> str:
        return f'move {self.player} {self.piece}: {self.src} -> {self.dst}'


class Board:
    """
    Singleton class for the game board.
    """

    def __init__(self, spaces=None):
        self.spaces = spaces
        if not self.spaces:
            self.spaces = copy.deepcopy(DEFAULT_BOARD_SPACES)

    @staticmethod
    def valid_starting_layout(layout: Layout):
        # TODO: do real checking
        # TODO: make sure no duplicate pieces
        return True

    def setup_board(self, layout: Layout):
        if not self.valid_starting_layout(layout):
            raise ValueError('invalid starting layout')
        for piece, space_name in layout.items():
            space = self.get_space_named(space_name)
            space.pieces.append(piece)

    def get_space(self, coordinates: Coordinate) -> Optional[Space]:
        """
        Return the space on the board specified by these coordinatees, or
        None if the coordinates are off the board.
        """
        try:
            return self.spaces[coordinates[0]][coordinates[1]]
        except IndexError:
            return None

    def get_space_named(self, space_name: str) -> Optional[Space]:
        try:
            return next(
                space
                for row in self.spaces
                for space in row
                if space.name == space_name

            )
        except StopIteration:
            return None

    def is_move_valid(self, move: Move) -> Tuple[bool, str]:
        """
        Return:
            bool: if move is an attack
        """
        # Make sure move starts on the board.
        if not self.get_space(move.src):
            return False, f'starting index {move.src} off the board'
        # Make sure move ends on the board.
        if not self.get_space(move.dst):
            return False, f'destination index {move.dst} off the board'

        # Make sure piece to move is in the starting space.
        src_space = self.get_space(move.src)
        if move.piece not in src_space.pieces:
            return False, 'moved piece not in starting space'

        # Make sure piece belongs to the moving player.
        if not isinstance(move.player, move.piece.allegiance):
            return False, 'wrong player'

        dst_space = self.get_space(move.dst)

        # If the move is not an attack, make sure the destination has room.
        if not self.is_move_attack(move) and dst_space.is_full():
            return False, 'destination is full'

        if is_special_case_for_piece(move.piece):
            # TODO
            return False, 'not implemented'

        if is_special_case_for_move(move):
            # TODO
            return False, 'not implemented'

        # TODO: clean up using error classmethods
        if isinstance(move.player, Sauron):
            if move.src[0] >= move.dst[0]:
                return False, 'not moving forward'
            if move.dst[0] - move.src[0] != 1:
                return False, 'moving more than one space'
            if move.src[0] < 3:
                if not (move.src[1] <= move.dst[1] <= move.src[1] + 1):
                    return False, 'moving too far laterally'
            else:
                if not (move.src[1] - 1 <= move.dst[1] <= move.src[1]):
                    return False, 'moving too far laterally'
        else:  # is Fellowship
            if move.dst[0] >= move.src[0]:
                return False, 'not moving forward'
            if move.src[0] - move.dst[0] != 1:
                return False, 'moving more than one space'
            if move.src[0] > 3:
                if not (move.src[1] <= move.dst[1] <= move.src[1] + 1):
                    return False, 'moving too far laterally'
            else:
                if not (move.src[1] - 1 <= move.dst[1] <= move.src[1]):
                    return False, 'moving too far laterally'
        return True, 'valid move'

    def is_move_attack(self, move: Move) -> bool:
        """Indicate whether the given move is an attack."""
        dst_space = self.get_space(move.dst)
        return (
            dst_space.allegiance
            and not isinstance(move.player, dst_space.allegiance)
        )

    def valid_moves_from(
            self,
            player: Player,
            src: Coordinate,
            piece: Piece,
        ) -> Generator[Move, None, None]:
        """
        Return a list of all the allowed moves
        """
        if piece not in self.get_space(src).pieces:
            return False, f'piece {piece} not in source space'
        # Set up a generator of every imaginable move for this player and
        # piece, regardless of whether it's allowed.
        all_moves = (
            Move(player=player, piece=piece, src=src, dst=(i, j))
            for i in range(7)
            for j in range(4)
        )
        # Yield the valid moves.
        for move in all_moves:
            valid, msg = self.is_move_valid(move)
            if valid:
                yield move

    def apply_move(self, move: Move):
        """
        Apply the move to the board and move the given piece from the source to
        the destination.
        """
        if not self.is_move_valid(move):
            return ValueError(f"can't apply invalid move: {move}")
        self.get_space(move.src).pieces.remove(move.piece)
        self.get_space(move.dst).pieces.append(move.piece)

    def is_frodo_with_sam(self) -> bool:
        # TODO
        return False

    def find_space_for_piece(
            self,
            piece_name: str
        ) -> Optional[Space]:
        """
        Return the space and piece for a piece with the name, or None if it's
        not on the board.
        """
        flat_spaces = (space for row in self.spaces for space in row)
        for space in flat_spaces:
            for piece in space:
                if piece.name == piece_name:
                    return space
        return None

    def remove_piece(self, piece: Piece):
        self.remove_piece_by_name(piece.name)

    def remove_piece_by_name(self, piece_name: str):
        space = self.find_space_for_piece(piece_name)
        if space:
            piece = space.get_piece_named(piece_name)
            space.pieces.remove(piece)


def is_special_case_for_piece(piece: Piece) -> bool:
    """
    Indicate whether the given piece may have a special case for its movement.
    If returning false, the piece must follow ordinary movement rules.
    """
    # TODO
    return False


def is_special_case_for_move(move: Move) -> bool:
    """
    Indicate whether this move may be some special case causing it to be
    allowed when it would otherwise not (river, moria, etc.). If returning
    false, these must be coordinates for a normal move (one space forward, and
    one left or right).
    """
    # TODO
    return False
