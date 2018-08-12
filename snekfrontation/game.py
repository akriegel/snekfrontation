from typing import Tuple

from snekfrontation.board import Board
from snekfrontation.cards import DummyFellowshipCard, DummySauronCard
from snekfrontation.combat import Combat, ResultFlags
from snekfrontation.players import Player, Fellowship, Sauron


class Game:
    """
    Singleton class for tracking the whole game state.
    """

    def __init__(self):
        self.board = Board()
        self.sauron = Sauron()
        self.fellowship = Fellowship()
        self.current_player = self.sauron

    def other_player(self, player):
        if isinstance(self.current_player, Sauron):
            return self.fellowship
        else:
            return self.sauron

    def switch_current_player(self):
        self.current_player = self.other_player(self.current_player)

    def handle_move(
            self,
            player: Player,
            src: Tuple[int, int],
            piece_number: int,
            dst: Tuple[int, int],
        ):
        """
        TODO
        """
        is_attacking = self.board.is_move_valid(player, src, piece_number, dst)
        moving_piece = self.board.spaces[src[0]][src[1]].pieces[piece_number]
        while is_attacking and moving_piece.is_alive():
            # is_attacking should be true as long as there are hostile pieces
            # in the destination
            is_attacking = resolve_combat(player, src, moving_piece, dst)
        if moving_piece.is_alive():
            self.board.do_passive_move(src, piece_number, dst)
        self.switch_current_player()

    def resolve_combat(self, move):
        # TODO: check if ringbearer attacks mordor (gg)

        # TODO
        dummy_input = {
            'sam_switch': False,
            'sauron_card': DummySauronCard,
            'fellow_card': DummyFellowshipCard,
        }
        input_callback = lambda _: dummy_input

        combat = Combat(
            self.board,
            move,
            self.current_player,
            self.other_player(self.current_player),
            input_callback,
        )

        stop_combat = False
        while not stop_combat:
            results = combat.handle_round()

            if ResultFlags.ATTACKER_DIES in results:
                # TODO
                pass
            if ResultFlags.DEFENDER_DIES in results:
                # TODO
                pass

            stop_combat = (
                ResultFlags.ATTACKER_DIES in results
                or (
                    self.current_player == Sauron
                    and ResultFlags.SAURON_RETREAT in results
                )
                or (
                    self.current_player == Fellowship
                    and ResultFlags.FELLOW_RETREAT in results
                )
                or ResultFlags.NO_DEFENDERS in results
                or ResultFlags.SHELOB_RETREAT in results
            )
