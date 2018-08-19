import pytest

from snekfrontation.board import Move


def test_valid_moves(game):
    """
    Test checking for valid moves on the board.
    """
    # Sauron has 2 moves with the single dummy piece
    valid_moves = list(game.board.valid_moves_from(
        game.sauron,
        (0, 0),
        game.board.spaces[0][0].pieces[0],
    ))
    assert len(valid_moves) == 2
    for move in valid_moves:
        # both moves should go from row 0 to row 1
        assert move.src[0] == 0
        assert move.dst[0] == 1
    # Fellowship has 2 moves with the single dummy piece
    valid_moves = list(game.board.valid_moves_from(
        game.fellowship,
        (6, 0),
        game.board.spaces[6][0].pieces[0],
    ))
    assert len(valid_moves) == 2
    for move in valid_moves:
        # both moves should go from row 6 to row 5
        assert move.src[0] == 6
        assert move.dst[0] == 5


def test_valid_moves_wrong_player(game):
    """
    Test that trying to move pieces with the wrong player returns no valid
    moves.
    """
    valid_moves = list(game.board.valid_moves_from(
        game.fellowship,
        (0, 0),
        game.board.spaces[0][0].pieces[0],
    ))
    assert not valid_moves


def test_do_move(game):
    """
    Test performing basic moves.
    """
    src = (0, 0)
    dst = (1, 0)
    piece = game.board.get_space(src).pieces[0]
    move = Move(game.sauron, piece, src, dst)
    game.handle_move(move)
    # Make sure the piece actually moved
    assert not game.board.get_space(src).pieces
    assert piece in game.board.get_space(dst).pieces


def test_try_move_wrong_player(game):
    """
    Test that attempting to move a piece belonging to the wrong player raises
    an error.
    """
    src = (0, 0)
    dst = (1, 0)
    piece = game.board.get_space(src).pieces[0]
    # try to move Sauron piece with Fellowship
    move = Move(game.fellowship, piece, src, dst)
    with pytest.raises(ValueError):
        game.handle_move(move)
