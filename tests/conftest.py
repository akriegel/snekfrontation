"""
Setup basic pytest fixtures (board, game, etc.)
"""

import pytest

from snekfrontation.board import Board
from snekfrontation.game import Game
from snekfrontation.pieces import FellowshipPiece, SauronPiece


@pytest.fixture(scope="function")
def basic_test_board():
    """
    Return an empty board with the default spaces.
    """
    return Board()


@pytest.fixture(scope="function")
def mordor_space(basic_test_board):
    return basic_test_board.get_space_named("Mordor")


@pytest.fixture(scope="function")
def dummy_sauron_piece():
    return SauronPiece("Dummy S", 2)


@pytest.fixture(scope="function")
def dummy_fellow_piece():
    return FellowshipPiece("Dummy F", 1)


@pytest.fixture(scope="function")
def dummy_layout(dummy_fellow_piece, dummy_sauron_piece):
    return {dummy_fellow_piece: "Alienland", dummy_sauron_piece: "Mordor"}


@pytest.fixture(scope="function")
def combat_ready_layout(dummy_fellow_piece, dummy_sauron_piece):
    """
    Return a piece layout where one move can trigger combat.
    """
    return {
        dummy_fellow_piece: "Moria",  # (3, 2)
        dummy_sauron_piece: "Fangorn",  # (2, 1)
    }


@pytest.fixture(scope="function")
def game(basic_test_board, dummy_layout):
    """
    Return a test game at the very beginning.
    """
    game = Game()
    game.board = basic_test_board
    game.board.setup_board(dummy_layout)
    return game


@pytest.fixture(scope="function")
def basic_combat_game(basic_test_board, combat_ready_layout):
    """
    Set up a game ready for a combat in Moria.
    """
    game = Game()
    game.board = basic_test_board
    game.board.setup_board(combat_ready_layout)
    return game
