from typing import Tuple

from snekfrontation.board import Board, Move
from snekfrontation.combat import Combat, ResultFlags
from snekfrontation.pieces import FellowshipPiece
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

    def other_player(self, player: Player) -> Player:
        if isinstance(self.current_player, Sauron):
            return self.fellowship
        else:
            return self.sauron

    def switch_current_player(self):
        self.current_player = self.other_player(self.current_player)

    def player_wins(self, player):
        # TODO
        print(f'{player} wonnered')

    def handle_move(self, move: Move):
        """
        TODO
        """
        if self.current_player != move.player:
            raise ValueError(f'invalid move (not current player): {move}')
        if not self.board.is_move_valid(move):
            raise ValueError(f'invalid move: {move}')

        # Fellowship wins if the ringbearer moves to Mordor.
        move_to_mordor = self.board.get_space(move.dst).name == 'Mordor'
        ringbearer_to_mordor = (
            isinstance(move.piece, FellowshipPiece)
            and move.piece.has_ring
            and move_to_mordor
        )
        if ringbearer_to_mordor:
            self.player_wins(self.current_player)

        combat_result = None
        if self.board.is_move_attack(move):
            combat_result = self.resolve_combat(move)

        if combat_result:
            # Attacker might have died.
            space = self.board.find_space_for_piece(move.piece.name)
            sauron_retreat = ResultFlags.SAURON_RETREAT in combat_result
            fellow_retreat = ResultFlags.FELLOW_RETREAT in combat_result
            attacker_retreated = (
                isinstance(self.current_player, Sauron) and sauron_retreat
                or (
                    isinstance(self.current_player, Fellowship)
                    and fellow_retreat
                )
            )
            if space and not attacker_retreated:
                self.board.apply_move(move)
        else:
            self.board.apply_move(move)

        self.switch_current_player()

    def resolve_combat(self, move):

        # TODO: get real input
        #dummy_input = {
        #    'sam_switch': False,
        #    'sauron_card': DummySauronCard,
        #    'fellow_card': DummyFellowshipCard,
        #}
        #input_callback = lambda _: dummy_input

        # Set up a combat
        combat = Combat(
            self.board,
            move,
            self.current_player,
            self.other_player(self.current_player),
            lambda: None,  # FIXME
        )

        # Hash it out until it's all ogre
        stop_combat = False
        while not stop_combat:
            results = combat.handle_round()

            # Remove dead pieces
            if ResultFlags.ATTACKER_DIES in results:
                self.board.remove_piece(move.piece)
            if ResultFlags.DEFENDER_DIES in results:
                self.board.remove_piece(combat.defender)

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

            if ResultFlags.SHELOB_RETREAT in results:
                # handle shelob retreat
                # TODO
                pass

        return results
