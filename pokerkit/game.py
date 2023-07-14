from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from random import shuffle

from pokerkit.hands import (
    AceToFiveLowballHand,
    DeuceToSevenLowballHand,
    LowEightOrBetterHand,
    OmahaHoldemHand,
    OmahaLowEightOrBetterHand,
    StandardHand,
)
from pokerkit.state import BettingStructure, Dealing, Opening, State, Street
from pokerkit.utilities import Deck


@dataclass
class Game:
    """The class for games."""

    _state: State

    @classmethod
    def create_fixed_limit_texas_holdem(
            cls,
            antes: Iterable[int],
            blinds_or_straddles: Iterable[int],
            small_bet: int,
            big_bet: int,
            starting_stacks: Iterable[int],
    ) -> Game:
        """Create a fixed-limit Texas hold'em game.

        :return: The poker game.
        """
        deck = deque(Deck.STANDARD)

        shuffle(deck)

        return cls(
            State(
                (StandardHand,),
                (
                    Street(
                        Dealing(False, (False,) * 2, 0, False),
                        Opening.POSITION,
                        small_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (), 3, False),
                        Opening.POSITION,
                        small_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (), 1, False),
                        Opening.POSITION,
                        big_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (), 1, False),
                        Opening.POSITION,
                        big_bet,
                        4,
                    ),
                ),
                BettingStructure.FIXED_LIMIT,
                tuple(antes),
                tuple(blinds_or_straddles),
                0,
                tuple(starting_stacks),
                deck,
            ),
        )

    @classmethod
    def create_no_limit_texas_holdem(
            cls,
            antes: Iterable[int],
            blinds_or_straddles: Iterable[int],
            min_bet_or_raise_amount: int,
            starting_stacks: Iterable[int],
    ) -> Game:
        """Create a no-limit Texas hold'em game.

        :return: The poker game.
        """
        deck = deque(Deck.STANDARD)

        shuffle(deck)

        return cls(
            State(
                (StandardHand,),
                (
                    Street(
                        Dealing(False, (False,) * 2, 0, False),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 3, False),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 1, False),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 1, False),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                ),
                BettingStructure.NO_LIMIT,
                tuple(antes),
                tuple(blinds_or_straddles),
                0,
                tuple(starting_stacks),
                deck,
            ),
        )

    @classmethod
    def create_pot_limit_omaha_holdem(
            cls,
            antes: Iterable[int],
            blinds_or_straddles: Iterable[int],
            min_bet_or_raise_amount: int,
            starting_stacks: Iterable[int],
    ) -> Game:
        """Create a no-limit Texas hold'em game.

        :return: The poker game.
        """
        deck = deque(Deck.STANDARD)

        shuffle(deck)

        return cls(
            State(
                (OmahaHoldemHand,),
                (
                    Street(
                        Dealing(False, (False,) * 4, 0, False),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 3, False),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 1, False),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 1, False),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                ),
                BettingStructure.POT_LIMIT,
                tuple(antes),
                tuple(blinds_or_straddles),
                0,
                tuple(starting_stacks),
                deck,
            ),
        )

    @classmethod
    def create_fixed_limit_seven_card_stud(
            cls,
            antes: Iterable[int],
            bring_in: int,
            small_bet: int,
            big_bet: int,
            starting_stacks: Iterable[int],
    ) -> Game:
        """Create a fixed-limit seven card stud game.

        :return: The poker game.
        """
        antes = tuple(antes)
        blinds_or_straddles = (0,) * len(antes)
        deck = deque(Deck.STANDARD)

        shuffle(deck)

        return cls(
            State(
                (StandardHand,),
                (
                    Street(
                        Dealing(False, (False, False, True), 0, False),
                        Opening.LOW_CARD,
                        small_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (True,), 0, False),
                        Opening.HIGH_HAND,
                        small_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (True,), 0, False),
                        Opening.HIGH_HAND,
                        big_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (True,), 0, False),
                        Opening.HIGH_HAND,
                        big_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (False,), 0, False),
                        Opening.HIGH_HAND,
                        big_bet,
                        4,
                    ),
                ),
                BettingStructure.FIXED_LIMIT,
                antes,
                blinds_or_straddles,
                bring_in,
                tuple(starting_stacks),
                deck,
            ),
        )

    @classmethod
    def create_fixed_limit_seven_card_stud_high_low_split_eight_or_better(
            cls,
            antes: Iterable[int],
            bring_in: int,
            small_bet: int,
            big_bet: int,
            starting_stacks: Iterable[int],
    ) -> Game:
        """Create a fixed-limit seven card stud high-low split-eight or
        better game.

        :return: The poker game.
        """
        antes = tuple(antes)
        blinds_or_straddles = (0,) * len(antes)
        deck = deque(Deck.STANDARD)

        shuffle(deck)

        return cls(
            State(
                (StandardHand, LowEightOrBetterHand),
                (
                    Street(
                        Dealing(False, (False, False, True), 0, False),
                        Opening.LOW_CARD,
                        small_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (True,), 0, False),
                        Opening.HIGH_HAND,
                        small_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (True,), 0, False),
                        Opening.HIGH_HAND,
                        big_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (True,), 0, False),
                        Opening.HIGH_HAND,
                        big_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (False,), 0, False),
                        Opening.HIGH_HAND,
                        big_bet,
                        4,
                    ),
                ),
                BettingStructure.FIXED_LIMIT,
                antes,
                blinds_or_straddles,
                bring_in,
                tuple(starting_stacks),
                deck,
            ),
        )

    @classmethod
    def create_fixed_limit_razz(
            cls,
            antes: Iterable[int],
            bring_in: int,
            small_bet: int,
            big_bet: int,
            starting_stacks: Iterable[int],
    ) -> Game:
        """Create a fixed-limit razz game.

        :return: The poker game.
        """
        antes = tuple(antes)
        blinds_or_straddles = (0,) * len(antes)
        deck = deque(Deck.STANDARD)

        shuffle(deck)

        return cls(
            State(
                (AceToFiveLowballHand,),
                (
                    Street(
                        Dealing(False, (False, False, True), 0, False),
                        Opening.HIGH_CARD,
                        small_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (True,), 0, False),
                        Opening.LOW_HAND,
                        small_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (True,), 0, False),
                        Opening.LOW_HAND,
                        big_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (True,), 0, False),
                        Opening.LOW_HAND,
                        big_bet,
                        4,
                    ),
                    Street(
                        Dealing(True, (False,), 0, False),
                        Opening.LOW_HAND,
                        big_bet,
                        4,
                    ),
                ),
                BettingStructure.FIXED_LIMIT,
                antes,
                blinds_or_straddles,
                bring_in,
                tuple(starting_stacks),
                deck,
            ),
        )

    @classmethod
    def create_fixed_limit_omaha_holdem_high_low_split_eight_or_better(
            cls,
            antes: Iterable[int],
            blinds_or_straddles: Iterable[int],
            small_bet: int,
            big_bet: int,
            starting_stacks: Iterable[int],
    ) -> Game:
        """Create a fixed-limit Omaha hold'em high-low split-eight or
        better.

        :return: The poker game.
        """
        deck = deque(Deck.STANDARD)

        shuffle(deck)

        return cls(
            State(
                (OmahaHoldemHand, OmahaLowEightOrBetterHand),
                (
                    Street(
                        Dealing(False, (False,) * 4, 0, False),
                        Opening.POSITION,
                        small_bet,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 3, False),
                        Opening.POSITION,
                        small_bet,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 1, False),
                        Opening.POSITION,
                        big_bet,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 1, False),
                        Opening.POSITION,
                        big_bet,
                        None,
                    ),
                ),
                BettingStructure.FIXED_LIMIT,
                tuple(antes),
                tuple(blinds_or_straddles),
                0,
                tuple(starting_stacks),
                deck,
            ),
        )

    @classmethod
    def create_no_limit_deuce_to_seven_lowball_single_draw(
            cls,
            antes: Iterable[int],
            blinds_or_straddles: Iterable[int],
            min_bet_or_raise_amount: int,
            starting_stacks: Iterable[int],
    ) -> Game:
        """Create a no-limit deuce-to-seven lowball single draw game.

        :return: The poker game.
        """
        deck = deque(Deck.STANDARD)

        shuffle(deck)

        return cls(
            State(
                (DeuceToSevenLowballHand,),
                (
                    Street(
                        Dealing(False, (False,) * 5, 0, False),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 0, True),
                        Opening.POSITION,
                        min_bet_or_raise_amount,
                        None,
                    ),
                ),
                BettingStructure.NO_LIMIT,
                tuple(antes),
                tuple(blinds_or_straddles),
                0,
                tuple(starting_stacks),
                deck,
            ),
        )

    @classmethod
    def create_fixed_limit_deuce_to_seven_lowball_triple_draw(
            cls,
            antes: Iterable[int],
            blinds_or_straddles: Iterable[int],
            small_bet: int,
            big_bet: int,
            starting_stacks: Iterable[int],
    ) -> Game:
        """Create a fixed-limit deuce-to-seven lowball triple draw game.

        :return: The poker game.
        """
        deck = deque(Deck.STANDARD)

        shuffle(deck)

        return cls(
            State(
                (DeuceToSevenLowballHand,),
                (
                    Street(
                        Dealing(False, (False,) * 5, 0, False),
                        Opening.POSITION,
                        small_bet,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 0, True),
                        Opening.POSITION,
                        small_bet,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 0, True),
                        Opening.POSITION,
                        big_bet,
                        None,
                    ),
                    Street(
                        Dealing(True, (), 0, True),
                        Opening.POSITION,
                        big_bet,
                        None,
                    ),
                ),
                BettingStructure.FIXED_LIMIT,
                tuple(antes),
                tuple(blinds_or_straddles),
                0,
                tuple(starting_stacks),
                deck,
            ),
        )
