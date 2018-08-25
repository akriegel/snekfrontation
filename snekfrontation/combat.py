from enum import Enum, auto
import random
from typing import Callable, Set

from snekfrontation.board import Board, Move, Player
from snekfrontation.players import Fellowship, Sauron, NumberCard


class CombatFlags(Enum):

    FRODO_ATTACKED = auto()
    SAM_ATTACKED = auto()
    FRODO_WITH_SAM = auto()
    SAM_IS_FIVE = auto()
    GIMLI = auto()
    PIPPIN_ATTACK = auto()
    LEGOLAS = auto()
    MERRY = auto()
    GANDALF = auto()
    MR_BOROMIRS_SNIPP_N_RIP = auto()
    ORC_SNIPP = auto()
    ORC_SNIPPED = auto()
    SHELOB = auto()
    SARUMAN = auto()
    WARG = auto()
    CAVE_TROLL = auto()
    END_BEFORE_CARDS = auto()
    SKIP_CARDS = auto()


class ResultFlags(Enum):

    SAURON_RETREAT = auto()
    FELLOW_RETREAT = auto()
    SHELOB_RETREAT = auto()
    NOBLE_SAC = auto()
    ATTACKER_DIES = auto()
    DEFENDER_DIES = auto()
    NO_DEFENDERS = auto()


class Combat:

    def __init__(
            self,
            board: Board,
            move: Move,
            player_atk: Player,
            player_def: Player,
            input_callback: Callable,
        ):
        """
        """
        self.board = board
        self.move = move
        self.player_atk = player_atk
        self.player_def = player_def
        self.flags = set()
        self.defenders = self.board.get_space(move.dst).pieces
        self.attacker = self.move.piece
        self.defender = None

    def add_flags(self):
        if self.attacker.name == 'Warg' or self.defender.name == 'Warg':
            self.flags.add(CombatFlags.WARG)
        if CombatFlags.WARG not in self.flags:
            self.apply_fellowship_flags()
        self.apply_sauron_flags()

    def apply_fellowship_flags(self):
        # variant game: ask for Gwaihir the Windlord
        if self.defender.name == 'Frodo':
            self.flags.add(CombatFlags.FRODO_ATTACKED)
        if self.defender.name == 'Sam':
            self.flags.add(CombatFlags.SAM_ATTACKED)
        if self.defender.name == 'Frodo' or self.defender.name == 'Sam':
            if self.board.is_frodo_with_sam():
                self.flags.add(CombatFlags.FRODO_WITH_SAM)
        if self.attacker.name == 'Gimli' or self.defender.name == 'Gimli':
            self.flags.add(CombatFlags.GIMLI)
        if self.attacker.name == 'Pippin':
            self.flags.add(CombatFlags.PIPPIN_ATTACK)
        if self.attacker.name == 'Legolas' or self.defender.name == 'Legolas':
            self.flags.add(CombatFlags.LEGOLAS)
        if self.attacker.name == 'Merry' or self.defender.name == 'Merry':
            self.flags.add(CombatFlags.MERRY)
        if self.attacker.name == 'Gandalf' or self.defender.name == 'Gandalf':
            self.flags.add(CombatFlags.GANDALF)
        if self.attacker.name == 'Boromir' or self.defender.name == 'Boromir':
            self.flags.add(CombatFlags.MR_BOROMIRS_SNIPP_N_RIP)

    def apply_sauron_flags(self):
        if (
            self.attacker.name == 'Orcs'
            and CombatFlags.ORC_SNIPPED not in self.flags
        ):
            self.flags.add(CombatFlags.ORC_SNIPP)
        if self.attacker.name == 'Shelob' or self.defender.name == 'Shelob':
            self.flags.add(CombatFlags.SHELOB)
        if self.attacker.name == 'Saruman' or self.defender.name == 'Saruman':
            self.flags.add(CombatFlags.SARUMAN)
        if (
            self.attacker.name == 'Cave Troll'
            or self.defender.name == 'Cave Troll'
        ):
            self.flags.add(CombatFlags.CAVE_TROLL)

    def reset_flags_for_round(self):
        new_flags = set()
        # TODO

    def handle_round(self) -> Set[ResultFlags]:
        """
        Resolve a single round of combat between the attacking piece and *one*
        piece in the defending space.
        """
        self.defender = random.choice(self.defenders)
        self.add_flags()

        # Text phase
        # Resolve all the "fast" text now (before cards); fellowship first

        # skip to end?

        sam_can_intervene = (
            self.defender.name == 'Frodo'
            and CombatFlags.FRODO_WITH_SAM in self.flags
        )
        #response = self.input_callback(InputRequest('use sam switch'))
        if sam_can_intervene:
            # allow self.defender = sam
            pass

        # Card selection phase
        # Default to 0 cards, so we can use these if nothing is played
        attacker_card = NumberCard(Player, 0)
        defender_card = NumberCard(Player, 0)
        if CombatFlags.SKIP_CARDS not in self.flags:
            if CombatFlags.GANDALF in self.flags:
                # sauron card first
                # TODO
                pass
            else:
                # cards simultaneously
                # TODO
                pass
        # Copy values out of cards for mutating
        sauron_attacking = self.defender.allegiance == Fellowship
        if sauron_attacking:
            sauron_card_value = attacker_card.value
            sauron_card_text = attacker_card.text
            fellow_card_value = defender_card.value
            fellow_card_text = defender_card.text
        else:
            fellow_card_value = attacker_card.value
            fellow_card_text = attacker_card.text
            sauron_card_value = defender_card.value
            sauron_card_text = defender_card.text

        # Card resolution phase
        result_flags = set()
        # Sauron text
        if sauron_card_text == 'Magic':
            # TODO
            pass
        if sauron_card_text == 'Eye of Sauron':
            fellow_card_text = ''
        if sauron_card_text == 'Retreat':
            # TODO
            # maybe end combat idk
            pass
        # Fellowship text
        if fellow_card_text == 'Magic':
            # TODO
            pass
        if fellow_card_text == 'Retreat':
            # TODO
            # maybe end combat idk
            pass
        if fellow_card_text == 'Noble Sac':
            # TODO
            # very end combat majinD
            result_flags.add(ResultFlags.ATTACKER_DIES)
            result_flags.add(ResultFlags.DEFENDER_DIES)
            pass
        if fellow_card_text == 'Elven Cloak':
            sauron_card_value = 0

        if sauron_attacking:
            attacker_str = self.attacker.strength + sauron_card_value
            defender_str = self.defender.strength + fellow_card_value
        else:
            defender_str = self.attacker.strength + sauron_card_value
            attacker_str = self.defender.strength + fellow_card_value

        # Round resolution phase
        if attacker_str >= defender_str:
            result_flags.add(ResultFlags.DEFENDER_DIES)
        if attacker_str <= defender_str:
            result_flags.add(ResultFlags.ATTACKER_DIES)

        ## FIXME: remove (testing only)
        ## everyone dies majinD
        #result_flags.add(ResultFlags.DEFENDER_DIES)
        #result_flags.add(ResultFlags.ATTACKER_DIES)

        # remove defender from the combat if they died
        if ResultFlags.DEFENDER_DIES in result_flags:
            self.defenders.remove(self.defender)

        if not self.defenders:
            result_flags.add(ResultFlags.NO_DEFENDERS)

        return result_flags
