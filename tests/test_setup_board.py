def test_initialize_game(game):
    assert game
    # TODO: actually test anything?


def test_space_string(mordor_space):
    """
    Test the string serialization for a space.
    """
    try:
        assert str(mordor_space)
    except Exception as e:
        raise AssertionError(f"space serialization failed: {e}")
