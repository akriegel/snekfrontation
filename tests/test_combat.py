from snekfrontation.board import Move
from snekfrontation.pieces import SauronPiece


def test_simple_combat(basic_combat_game):
    """
    Test out a simple combat with dummy pieces.
    """
    # Sauron piece is stronger (2 vs 1)
    src = (2, 1)
    dst = (3, 2)
    piece = basic_combat_game.board.get_space(src).pieces[0]
    move = Move(basic_combat_game.sauron, piece, src, dst)
    basic_combat_game.handle_move(move)
    # The Sauron piece should have moved out of the source.
    assert not basic_combat_game.board.get_space(src).pieces
    # Now, there should be one Sauron piece in the destination (Moria).
    assert len(basic_combat_game.board.get_space(dst).pieces) == 1
    remaining_piece = basic_combat_game.board.get_space(dst).pieces[0]
    assert isinstance(remaining_piece, SauronPiece)
