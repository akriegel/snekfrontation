from enum import Enum, auto
import random

from snekfrontation.players import Fellowship, Sauron


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

    # TODO: break out combat logic into new class to mutate defender in case of
    # sam

    def resolve_combat(self, player, src, attacker, dst):
        flags = set()

        defending_space = self.board.get_space(dst)
        defender = random.choice(defending_space.pieces)

        if attacker.name == 'Warg':
            flags.add(CombatFlags.WARG)

        if not CombatFlags.WARG in flags:
            flags.update(apply_fellowship_text(attacker, defender))
        flags.update(apply_sauron_text(attacker, defender))

        if CombatFlags.GANDALF:
            # sauron card first
            # TODO
            pass
        else:
            # cards simultaneously
            # TODO
            pass


    def apply_fellowship_text(self, attacker, defender):
        flags = set()
        if attacker.name == 'Gandalf' or defender.name == 'Gandalf':
            flags.add(CombatFlags.GANDALF)
        if attacker.name == 'Pippin':
            # retreat allowed
            end = get_pippin_input()
            if end:
                flags.add(CombatFlags.END_BEFORE_CARDS)
        if defender.name == 'Frodo' or defender.name == 'Sam':
            if self.board.is_frodo_with_sam():
                # TODO
                pass
        # TODO: lots more fellowship stuff
        return flags

    def apply_sauron_text(self, attacker, defender):
        pass


class CombatFlags(Enum):

    WARG = auto()
    GANDALF = auto()
    END_BEFORE_CARDS = auto()
