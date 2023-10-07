Poker Simulation
================

The functionalities of PokerKit primarily fall into two categories: game
simulations and hand evaluations. Game simulations encompass creating an
environment where poker games can be played out programmatically, simulating
real-world scenarios with high fidelity. On the other hand, hand evaluations are
concerned with determining the strength of particular poker hands.

Introduction
------------

PokerKit is a very powerful tool you can use to simulate games. It's
customizability allow users to define and utilize almost every poker variant
that exists.

Each poker variant often introduces unique game rules and hand types not seen in
other variants. The versatility of PokerKit allows for the customization of
poker variants, allowing users to define their own unique games, adapt an
existing variant, or implement a variant not currently supported by PokerKit out
of the box. This flexibility is achieved without compromising the robustness of
the implementation, backed by extensive unit tests and doctests to ensure
error-free operations. Naturally, common variants are already defined out of the
box, so, for most use cases, users will not have to define their own variants.

PokerKit stands out with its ability to cater to an assortment of use cases,
offering varying degrees of control over the game state. For instance, in use
cases for poker AI agent development, where the agents' focus lies primarily
in action selection during betting rounds, minute details such as showdown
order, posting blinds, posting antes, and bet collection may not be pertinent.
On the other hand, an online poker casino requires granular control over each
game aspect. These include dealing hole cards one by one, burning cards,
deciding to muck or show during the showdown (even when unnecessary), killing
hands after the showdown, pushing chips to the winner's stack, and even the
winner collecting the chips into their stack. PokerKit rises to this challenge,
providing users with varying levels of automation tailored to their specific
needs.

State Initialization
--------------------

PokerKit offers virtually unlimited poker variants to be played. However,
defining poker variants can be quite an overwhelming task for a new user. We
offer pre-defined poker variants where user can just supply arguments such as
antes, blinds, starting stacks, et cetera, which are as follows:

- Fixed-limit badugi: :class:`pokerkit.games.FixedLimitBadugi`
- Fixed-limit deuce-to-seven lowball triple draw:
  :class:`pokerkit.games.FixedLimitDeuceToSevenLowballTripleDraw`
- Fixed-limit Omaha hold'em hi-low split-eight or better low:
  :class:`pokerkit.games.FixedLimitOmahaHoldemHighLowSplitEightOrBetter`
- Fixed-limit razz: :class:`pokerkit.games.FixedLimitRazz`
- Fixed-limit seven card stud: :class:`pokerkit.games.FixedLimitSevenCardStud`
- Fixed-limit seven card stud hi-low split-eight or better low:
  :class:`pokerkit.games.FixedLimitSevenCardStudHighLowSplitEightOrBetter`
- Fixed-limit Texas hold'em: :class:`pokerkit.games.FixedLimitTexasHoldem`
- No-limit deuce-to-seven single draw:
  :class:`pokerkit.games.NoLimitDeuceToSevenLowballSingleDraw`
- No-limit short-deck hold'em: :class:`pokerkit.games.NoLimitShortDeckHoldem`
- No-limit Texas hold'em: :class:`pokerkit.games.NoLimitTexasHoldem`
- Pot-limit Omaha hold'em: :class:`pokerkit.games.PotLimitOmahaHoldem`

These pre-defined games can be used as shown below:

.. code-block:: python

   from pokerkit import (
        Automation,
        FixedLimitDeuceToSevenLowballTripleDraw,
        NoLimitTexasHoldem,
   )

   state = FixedLimitDeuceToSevenLowballTripleDraw.create_state(
       # automations
       (
           Automation.ANTE_POSTING,
           Automation.BET_COLLECTION,
           Automation.BLIND_OR_STRADDLE_POSTING,
           Automation.CARD_BURNING,
           Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
           Automation.HAND_KILLING,
           Automation.CHIPS_PUSHING,
           Automation.CHIPS_PULLING,
       ),
       True,  # False for big blind ante, True otherwise
       None,  # ante
       (75000, 150000),  # blinds or straddles
       150000,  # small bet
       300000,  # big bet
       (1180000, 4340000, 5910000, 10765000),  # starting stacks
       4,  # number of players
   )

   state = NoLimitTexasHoldem.create_state(
       # automations
       (
           Automation.ANTE_POSTING,
           Automation.BET_COLLECTION,
           Automation.BLIND_OR_STRADDLE_POSTING,
           Automation.CARD_BURNING,
           Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
           Automation.HAND_KILLING,
           Automation.CHIPS_PUSHING,
           Automation.CHIPS_PULLING,
       ),
       True,  # False for big blind ante, True otherwise
       500,  # ante
       (1000, 2000),  # blinds or straddles
       2000,  # min bet
       (1125600, 2000000, 553500),  # starting stacks
       3,  # number of players
   )

What exactly is a variant then? These are described by various definitions:

- **Deck**: Most variants use a 52-card deck.
- **Hand Types**: Most variants have one, but high/low-split games have two.
- **Streets**: Each specifies whether to burn a card, deal the board, deal the
  players, draw cards, the opener, the minimum bet, and the maximum number of
  bets or raises.
- **Betting Structure**: Betting limits such as no-limit, pot- limit, or
  fixed-limit.

In addition to the parameters related to the variants, users can supply
additional values such as antes (uniform antes or non-uniform antes such as
big blind antes), blinds/straddles, bring-ins, and starting stacks as is the
case for pre-defined variants. Below is a Kuhn poker variant:

.. code-block:: python

   from pokerkit import (
        Automation,
        BettingStructure,
        Deck,
        KuhnPokerHand,
        Opening,
        State,
        Street,
   )

   state = State(
       # automations
       (
           Automation.ANTE_POSTING,
           Automation.BET_COLLECTION,
           Automation.BLIND_OR_STRADDLE_POSTING,
           Automation.CARD_BURNING,
           Automation.HOLE_DEALING,
           Automation.BOARD_DEALING,
           Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
           Automation.HAND_KILLING,
           Automation.CHIPS_PUSHING,
           Automation.CHIPS_PULLING,
       ),
       Deck.KUHN_POKER,  # deck
       (KuhnPokerHand,),  # hand types (high/low-split will have two types)
       # streets
       (
           Street(
               False,  # card burning
               (False,),  # hole card dealing statuses (False for face-down)
               0,  # board dealing card
               False,  # standing pat or discarding
               Opening.POSITION,  # who opens the betting?
               1,  # min bet
               None,  # maximum number of completions/bettings/raisings
           ),
       ),
       BettingStructure.FIXED_LIMIT,  # betting structure
       True,  # ``False`` for big blind ante, otherwise ``True``
       (1,) * 2,  # ante
       (0,) * 2,  # blind or straddles
       0,  # bring-in
       (2,) * 2,  # starting stacks
       2,  # number of players
   )

There is a lot to specify and you will have to experiment to get it right.

State Attributes
----------------

PokerKit's poker simulations are architected around the concept of states,
encapsulating all the vital information about the current game through its
attributes.

- **Cards in deck**: :attr:`pokerkit.state.State.deck_cards`
- **Community cards**: :attr:`pokerkit.state.State.board_cards`
- **Cards in muck**: :attr:`pokerkit.state.State.mucked_cards`
- **Burn cards (if user wants to, they can also deal burnt cards)**:
  :attr:`pokerkit.state.State.burn_cards`
- **Player statuses (are they still in?)**: :attr:`pokerkit.state.State.statuses`
- **Bets**: :attr:`pokerkit.state.State.bets`
- **Stacks**: :attr:`pokerkit.state.State.stacks`
- **Hole cards**: :attr:`pokerkit.state.State.hole_cards`
- **Hole card statuses (up or down?)**:
  :attr:`pokerkit.state.State.hole_card_statuses`
- **Street index**: :attr:`pokerkit.state.State.street_index`
- **Status (is the game over?)**: :attr:`pokerkit.state.State.status`
- **Total pot amount**: :attr:`pokerkit.state.State.total_pot_amount`
- **Pots (main + all sides)**: :attr:`pokerkit.state.State.pots`
- And more...

There are more, such as the initial game parameters and attributes that keep
track of who is in turn, what phase the game is in, and et cetera. You can look
at :class:`pokerkit.state.State` for a complete list.

State Phases
------------

PokerKit structures the game flow into distinct phases, each supporting a
different set of operations. Depending on the game state, each phase may be
skipped. For instance, if the user has specified no antes, the ante posting
phase will be omitted. Likewise, if no bets were placed during the betting
phase, the bet collection phase will be bypassed. A phase transition occurs upon
the completion of a phase. This transition is internally managed by the game
framework, facilitating a seamless game flow to the end user. During each phase
of PokerKit’s game simulation, the user can invoke various methods to execute
operations. Each operation belongs to a specific phase and can only be enacted
when the corresponding phase is active.

1. **Ante Posting**: During the ante posting phase, each player has the option
   to execute an ante-posting operation. The parameters supplied to the state
   during its creation may dictate no antes, uniform antes, or non-uniform
   antes, such as big blind antes. If no player is due to post an ante, this
   phase is bypassed.
2. **Bet Collection**: The collection of bets on the table occurs after any phase
   that allow players to bet. If any bet is present, the bet collection
   operation must be performed before proceeding to the subsequent phase. This
   phase only occurs after ante posting or betting. When no bets are pending
   collection, this phase is skipped.
3. **Blind or Straddle Posting**: Forced bets like blinds or straddles must be
   posted before the start of the first street. PokerKit accommodates a variety
   of blind or straddle config- urations, ranging from small and big blinds, to
   button blinds, or even no blind at all. If the state is configured to exclude
   any forced bets, this phase is skipped.
4. **Dealing**: The dealing phase precedes a betting phase. During this phase,
   the user can deal board or hole cards, contingent upon the state's
   configuration. Options to burn a card or discard and draw cards are also
   available when applicable. This phase is bypassed if only one player remains
   in the hand.
5. **Betting**: During betting, players can execute the actions such as folding,
   checking, calling, posting a bring-in, completing, betting, or raising.
   During state creation, the user must specify how to select the first player
   to act and the betting limits. This phase is bypassed if all players are
   all-in or if only one player remains in the hand.
6. **Showdown**: During the showdown, players reveal or muck their hands in
   accordance with the showdown order. The first to show is typically the last
   aggressor in the final street. If no one bet, the player who was the first
   to act in the final betting round must show first. Players can opt to show a
   losing hand or muck a winning hand, even though this is often
   disadvantageous. When dealing with all-in pots, players are obligated to show
   their hands in order to prevent chip-dumping. If this is the case, or if only
   one player remains in the pot, the showdown phase is bypassed.
7. **Hand Killing**: The dealer is responsible for "killing," or discarding,
   hands that cannot win any portion of the pot. If no hand should be killed,
   this phase is bypassed.
8. **Chips Pushing**: The dealer is charged with pushing the chips to the
   winners. In poker games, the pot size is always non-zero due to the mandatory
   presence of antes, forced bets, or bring-ins (as enforced by PokerKit). Thus,
   this phase is always carried out.
9. **Chips Pulling**: Players may incorporate the chips they've won back into
   their stack. In poker, at least one player is guaranteed to win the pot.
   Consequently, this phase is never skipped.

Note that, depending on the number of betting rounds, the **Dealing**,
**Betting**, and **Bet Collection** phases may be repeated.

Depending on the use cases, many of these phases can be automated without any
user input, as user can specify which operations they want to be manual and
automatic.

For example, if you are trying to create a poker AI, you are not worried about
mucking the best hand or showing the worse hand, burning a card, pushing the
chips to the winners, collecting chips a player won, collecting bets after each
street, et cetera. But, you want to handle user actions like fold, check, call,
bring-in, complete, bet, and raise. Also, you might want to control what cards
are dealt to each player and to the board.

However, if you are trying to create an online poker room, you need all these
fine changes to create smooth user experience. Although, you might not be
concerned about exactly what cards are dealt. You would be happy with cards
being dealt at random (hopefully).

PokerKit allow you to specify what you are worried about, and what you are not
worried about. :class:`pokerkit.state.Automation` describes operations that can
be automated.

Sample automations:

.. code-block:: python

   from pokerkit import Automation

   # automate everything except actions
   automations = (
       Automation.ANTE_POSTING,
       Automation.BET_COLLECTION,
       Automation.BLIND_OR_STRADDLE_POSTING,
       Automation.CARD_BURNING,
       Automation.HOLE_DEALING,
       Automation.BOARD_DEALING,
       Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
       Automation.HAND_KILLING,
       Automation.CHIPS_PUSHING,
       Automation.CHIPS_PULLING,
   )

   # Automate everything except actions and dealings
   automations = (
       Automation.ANTE_POSTING,
       Automation.BET_COLLECTION,
       Automation.BLIND_OR_STRADDLE_POSTING,
       Automation.CARD_BURNING,
       Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
       Automation.HAND_KILLING,
       Automation.CHIPS_PUSHING,
       Automation.CHIPS_PULLING,
   )

   # Automate nothing
   automations = ()


State Operations
----------------

Each operation is coupled with two associated methods: a verification method and
an action query. The verification method validates if a move can be executed
within the rules, considering the current game state and the variant in play. It
raises an error if any discrepancy is detected. Users can directly invoke this
or use a corresponding action query method (with optional arguments), which
simply checks if the verification method triggers an error and returns a boolean
value indicating the validity of the action. The method that performs the
operation initially runs the verification method, executing the operation only
if no errors are raised. If the verification fails, the state remains unchanged.

Below list all the operations supported by PokerKit. Depending on your use case,
many of these operations will not be of concern and can be automated.

- Ante posting: :meth:`pokerkit.state.State.post_ante`
- Bet collection: :meth:`pokerkit.state.State.collect_bets`
- Blind/straddle posting: :meth:`pokerkit.state.State.post_blind_or_straddle`
- Card burning: :meth:`pokerkit.state.State.burn_card`
- Hole dealing: :meth:`pokerkit.state.State.deal_hole`
- Board dealing: :meth:`pokerkit.state.State.deal_board`
- Standing pat/discarding: :meth:`pokerkit.state.State.stand_pat_or_discard`
- Folding: :meth:`pokerkit.state.State.fold`
- Checking/calling: :meth:`pokerkit.state.State.check_or_call`
- Bring-in posting: :meth:`pokerkit.state.State.post_bring_in`
- Completion/betting/raising to:
  :meth:`pokerkit.state.State.complete_bet_or_raise_to`
- Hole cards showing/mucking:
  :meth:`pokerkit.state.State.show_or_muck_hole_cards`
- Hand killing: :meth:`pokerkit.state.State.kill_hand`
- Chips pushing: :meth:`pokerkit.state.State.push_chips`
- Chips pulling: :meth:`pokerkit.state.State.pull_chips`

Now, let's say you know what operations you should worry about. How do you know
when to invoke them? PokerKit has handy methods to query whether you can perform
an operation:

- Ante posting?: :meth:`pokerkit.state.State.can_post_ante`
- Bet collection?: :meth:`pokerkit.state.State.can_collect_bets`
- Blind/straddle posting?: :meth:`pokerkit.state.State.can_post_blind_or_straddle`
- Card burning?: :meth:`pokerkit.state.State.can_burn_card`
- Hole dealing?: :meth:`pokerkit.state.State.can_deal_hole`
- Board dealing?: :meth:`pokerkit.state.State.can_deal_board`
- Standing pat/discarding?: :meth:`pokerkit.state.State.can_stand_pat_or_discard`
- Folding?: :meth:`pokerkit.state.State.can_fold`
- Checking/calling?: :meth:`pokerkit.state.State.can_check_or_call`
- Bring-in posting?: :meth:`pokerkit.state.State.can_post_bring_in`
- Completion/betting/raising to?:
  :meth:`pokerkit.state.State.can_complete_bet_or_raise_to`
- Hole cards showing/mucking?:
  :meth:`pokerkit.state.State.can_show_or_muck_hole_cards`
- Hand killing?: :meth:`pokerkit.state.State.can_kill_hand`
- Chips pushing?: :meth:`pokerkit.state.State.can_push_chips`
- Chips pulling?: :meth:`pokerkit.state.State.can_pull_chips`

These methods return ``True`` if you can perform such an operation (with
specified arguments, if any) or ``False`` if otherwise.

Most of the operations can optionally accept arguments. Some are more important
than others. Let's see what we can specify for each action.

- Ante posting: player_index, defaults to first player who did not post ante
- Bet collection: N/A
- Blind/straddle posting: player_index, defaults to first player who did not
  post the blind or straddle
- Card burning: card, defaults to randomly drawing from the deck
- Hole dealing: cards, defaults to randomly drawing a single card from the deck
- Board dealing: cards, defaults to randomly drawing required cards from the deck
- Standing pat/discarding: cards, defaults to standing pat
- Folding: N/A
- Checking/calling: N/A
- Bring-in posting: N/A
- Completion/betting/raising to: amount, defaults to completion, min-bet, or
  min-raise
- Hole cards showing/mucking: status, defaults to showing only when no-one else
  has shown a better hand
- Hand killing: player_index, defaults to the first player who cannot win any
  portion of the pot
- Chips pushing: N/A
- Chips pulling: player_index, defaults to the first player who won a portion of
  the pot

How do you know what the minimum bets are? How do you know to whom the hole card
will be dealt next? How do you know the call amount? Whose action is it?

You can access all these information through the following methods or properties:

- Effective ante: :meth:`poker.state.State.get_effective_ante`
- Ante poster indices: :attr:`poker.state.State.ante_poster_indices`
- Effective blind/straddle:
  :meth:`poker.state.State.get_effective_blind_or_straddle`
- Blind/straddle poster indices:
  :attr:`poker.state.State.blind_or_straddle_poster_indices`
- Available cards to be dealt: :attr:`poker.state.State.available_cards`
- Next default hole dealee: :attr:`poker.state.State.hole_dealee_index`
- Next stander pat or discarder:
  :attr:`poker.state.State.stander_pat_or_discarder_index`
- Next actor (fold, check, ...): :attr:`poker.state.State.actor_index`
- Effective stack: :attr:`poker.state.State.get_effective_stack`
- Checking/Calling amount: :attr:`poker.state.State.checking_or_calling_amount`
- Effective bring-in amount: :attr:`poker.state.State.effective_bring_in_amount`
- Min completion/bet/raise to amount:
  :attr:`poker.state.State.min_completion_betting_or_raising_to_amount`
- Pot completion/bet/raise to amount:
  :attr:`poker.state.State.pot_completion_betting_or_raising_to_amount`
- Max completion/bet/raise to amount:
  :attr:`poker.state.State.max_completion_betting_or_raising_to_amount`
- Person who is in showdown: :attr:`poker.state.State.showdown_index`
- Indices of players who cannot win and whose hand is about to be killed:
  :attr:`poker.state.State.hand_killing_indices`
- Players who won but has not taken back the chips into their stack yet:
  :attr:`poker.state.State.chips_pulling_indices``

After each action is performed, description of which player was involved,
what was the amount, what card was burnt, what cards were dealt, how much bets
were collected, et cetera are returned. The types of these are as shown:

- Ante posting: :class:`pokerkit.state.AntePosting`
- Bet collection: :class:`pokerkit.state.BetCollection`
- Blind/straddle posting: :class:`pokerkit.state.BlindOrStraddlePosting`
- Card burning: :class:`pokerkit.state.CardBurning`
- Hole dealing: :class:`pokerkit.state.HoleDealing`
- Board dealing: :class:`pokerkit.state.BoardDealing`
- Standing pat/discarding: :class:`pokerkit.state.StandingPatOrDiscarding`
- Folding: :class:`pokerkit.state.Folding`
- Checking/calling: :class:`pokerkit.state.CheckingOrCalling`
- Bring-in posting: :class:`pokerkit.state.BringInPosting`
- Completion/betting/raising to:
  :class:`pokerkit.state.CompletionBettingOrRaisingTo`
- Hole cards showing/mucking:
  :class:`pokerkit.state.HoleCardsShowingOrMucking`
- Hand killing: :class:`pokerkit.state.HandKilling`
- Chips pushing: :class:`pokerkit.state.ChipsPushing`
- Chips pulling: :class:`pokerkit.state.ChipsPulling`

Again, if an operation is not valid, errors will be raised. PokerKit’s
philosophy is that it should focus on maintaining the game state and enforcing
rules. Error handling is left to the user, who may need to handle errors
differently depending on the application. All the errors raised are
``ValueError``.

Interactions
------------

Now, let's look at some sample interactions!

This is a simple interaction.

.. code-block:: pycon

   >>> from pokerkit import *
   >>> state = FixedLimitTexasHoldem.create_state(
   ...     (
   ...         Automation.ANTE_POSTING,
   ...         Automation.BET_COLLECTION,
   ...         Automation.BLIND_OR_STRADDLE_POSTING,
   ...         Automation.CARD_BURNING,
   ...         Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
   ...         Automation.HAND_KILLING,
   ...         Automation.CHIPS_PUSHING,
   ...         Automation.CHIPS_PULLING,
   ...     ),
   ...     True,
   ...     None,
   ...     (1, 2),
   ...     2,
   ...     4,
   ...     200,
   ...     2,
   ... )
   >>> # Below shows the pre-flop dealings and actions.
   >>> state.deal_hole('AcAs')
   HoleDealing(player_index=0, cards=(Ac, As), statuses=(False, False))
   >>> state.deal_hole('7h6h')
   HoleDealing(player_index=1, cards=(7h, 6h), statuses=(False, False))
   >>> state.complete_bet_or_raise_to()
   CompletionBettingOrRaisingTo(player_index=1, amount=4)
   >>> state.complete_bet_or_raise_to()
   CompletionBettingOrRaisingTo(player_index=0, amount=6)
   >>> state.fold()
   Folding(player_index=1)
   >>> # Below show the final stacks.
   >>> state.stacks
   [204, 196]

Below shows the first televised million dollar pot between Tom Dwan and Phil
Ivey.

Link: https://youtu.be/GnxFohpljqM

.. code-block:: pycon

   >>> state = NoLimitTexasHoldem.create_state(
   ...     (
   ...         Automation.ANTE_POSTING,
   ...         Automation.BET_COLLECTION,
   ...         Automation.BLIND_OR_STRADDLE_POSTING,
   ...         Automation.CARD_BURNING,
   ...         Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
   ...         Automation.HAND_KILLING,
   ...         Automation.CHIPS_PUSHING,
   ...         Automation.CHIPS_PULLING,
   ...     ),
   ...     True,
   ...     500,
   ...     (1000, 2000),
   ...     2000,
   ...     (1125600, 2000000, 553500),
   ...     3,
   ... )
   >>> # Below shows the pre-flop dealings and actions.
   >>> state.deal_hole('Ac2d')  # Ivey
   HoleDealing(player_index=0, cards=(Ac, 2d), statuses=(False, False))
   >>> state.deal_hole('5h7s')  # Antonius*
   HoleDealing(player_index=1, cards=(5h, 7s), statuses=(False, False))
   >>> state.deal_hole('7h6h')  # Dwan
   HoleDealing(player_index=2, cards=(7h, 6h), statuses=(False, False))
   >>> state.complete_bet_or_raise_to(7000)  # Dwan
   CompletionBettingOrRaisingTo(player_index=2, amount=7000)
   >>> state.complete_bet_or_raise_to(23000)  # Ivey
   CompletionBettingOrRaisingTo(player_index=0, amount=23000)
   >>> state.fold()  # Antonius
   Folding(player_index=1)
   >>> state.check_or_call()  # Dwan
   CheckingOrCalling(player_index=2, amount=16000)
   >>> # Below shows the flop dealing and actions.
   >>> state.deal_board('Jc3d5c')
   BoardDealing(cards=(Jc, 3d, 5c))
   >>> state.complete_bet_or_raise_to(35000)  # Ivey
   CompletionBettingOrRaisingTo(player_index=0, amount=35000)
   >>> state.check_or_call()  # Dwan
   CheckingOrCalling(player_index=2, amount=35000)
   >>> # Below shows the turn dealing and actions.
   >>> state.deal_board('4h')
   BoardDealing(cards=(4h,))
   >>> state.complete_bet_or_raise_to(90000)  # Ivey
   CompletionBettingOrRaisingTo(player_index=0, amount=90000)
   >>> state.complete_bet_or_raise_to(232600)  # Dwan
   CompletionBettingOrRaisingTo(player_index=2, amount=232600)
   >>> state.complete_bet_or_raise_to(1067100)  # Ivey
   CompletionBettingOrRaisingTo(player_index=0, amount=1067100)
   >>> state.check_or_call()  # Dwan
   CheckingOrCalling(player_index=2, amount=262400)
   >>> # Below shows the river dealing.
   >>> state.deal_board('Jh')
   BoardDealing(cards=(Jh,))
   >>> # Below show the final stacks.
   >>> state.stacks
   [572100, 1997500, 1109500]

Below shows an all-in hand between Xuan and Phua.

Link: https://youtu.be/QlgCcphLjaQ

.. code-block:: pycon

   >>> state = NoLimitShortDeckHoldem.create_state(
   ...     (
   ...         Automation.ANTE_POSTING,
   ...         Automation.BET_COLLECTION,
   ...         Automation.BLIND_OR_STRADDLE_POSTING,
   ...         Automation.CARD_BURNING,
   ...         Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
   ...         Automation.HAND_KILLING,
   ...         Automation.CHIPS_PUSHING,
   ...         Automation.CHIPS_PULLING,
   ...     ),
   ...     True,
   ...     3000,
   ...     {-1: 3000},
   ...     3000,
   ...     (495000, 232000, 362000, 403000, 301000, 204000),
   ...     6,
   ... )
   >>> # Below shows the pre-flop dealings and actions.
   >>> state.deal_hole('Th8h')  # Badziakouski
   HoleDealing(player_index=0, cards=(Th, 8h), statuses=(False, False))
   >>> state.deal_hole('QsJd')  # Zhong
   HoleDealing(player_index=1, cards=(Qs, Jd), statuses=(False, False))
   >>> state.deal_hole('QhQd')  # Xuan
   HoleDealing(player_index=2, cards=(Qh, Qd), statuses=(False, False))
   >>> state.deal_hole('8d7c')  # Jun
   HoleDealing(player_index=3, cards=(8d, 7c), statuses=(False, False))
   >>> state.deal_hole('KhKs')  # Phua
   HoleDealing(player_index=4, cards=(Kh, Ks), statuses=(False, False))
   >>> state.deal_hole('8c7h')  # Koon
   HoleDealing(player_index=5, cards=(8c, 7h), statuses=(False, False))
   >>> state.check_or_call()  # Badziakouski
   CheckingOrCalling(player_index=0, amount=3000)
   >>> state.check_or_call()  # Zhong
   CheckingOrCalling(player_index=1, amount=3000)
   >>> state.complete_bet_or_raise_to(35000)  # Xuan
   CompletionBettingOrRaisingTo(player_index=2, amount=35000)
   >>> state.fold()  # Jun
   Folding(player_index=3)
   >>> state.complete_bet_or_raise_to(298000)  # Phua
   CompletionBettingOrRaisingTo(player_index=4, amount=298000)
   >>> state.fold()  # Koon
   Folding(player_index=5)
   >>> state.fold()  # Badziakouski
   Folding(player_index=0)
   >>> state.fold()  # Zhong
   Folding(player_index=1)
   >>> state.check_or_call()  # Xuan
   CheckingOrCalling(player_index=2, amount=263000)
   >>> # Below shows the flop dealing.
   >>> state.deal_board('9h6cKc')
   BoardDealing(cards=(9h, 6c, Kc))
   >>> # Below shows the turn dealing.
   >>> state.deal_board('Jh')
   BoardDealing(cards=(Jh,))
   >>> # Below shows the river dealing.
   >>> state.deal_board('Ts')
   BoardDealing(cards=(Ts,))
   >>> # Below show the final stacks.
   >>> state.stacks
   [489000, 226000, 684000, 400000, 0, 198000]

Below shows the largest online poker pot every played between
Patrik Antonius and Viktor Blom.

Link: https://youtu.be/UMBm66Id2AA

.. code-block:: pycon

   >>> state = PotLimitOmahaHoldem.create_state(
   ...     (
   ...         Automation.ANTE_POSTING,
   ...         Automation.BET_COLLECTION,
   ...         Automation.BLIND_OR_STRADDLE_POSTING,
   ...         Automation.CARD_BURNING,
   ...         Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
   ...         Automation.HAND_KILLING,
   ...         Automation.CHIPS_PUSHING,
   ...         Automation.CHIPS_PULLING,
   ...     ),
   ...     True,
   ...     None,
   ...     (50000, 100000),
   ...     2000,
   ...     (125945025, 67847350),
   ...     2,
   ... )
   >>> # Below shows the pre-flop dealings and actions.
   >>> state.deal_hole('Ah3sKsKh')  # Antonius
   HoleDealing(player_index=0, cards=(Ah, 3s, Ks, Kh), statuses=(False, False, False, False))
   >>> state.deal_hole('6d9s7d8h')  # Blom
   HoleDealing(player_index=1, cards=(6d, 9s, 7d, 8h), statuses=(False, False, False, False))
   >>> state.complete_bet_or_raise_to(300000)  # Blom
   CompletionBettingOrRaisingTo(player_index=1, amount=300000)
   >>> state.complete_bet_or_raise_to(900000)  # Antonius
   CompletionBettingOrRaisingTo(player_index=0, amount=900000)
   >>> state.complete_bet_or_raise_to(2700000)  # Blom
   CompletionBettingOrRaisingTo(player_index=1, amount=2700000)
   >>> state.complete_bet_or_raise_to(8100000)  # Antonius
   CompletionBettingOrRaisingTo(player_index=0, amount=8100000)
   >>> state.check_or_call()  # Blom
   CheckingOrCalling(player_index=1, amount=5400000)
   >>> # Below shows the flop dealing and actions.
   >>> state.deal_board('4s5c2h')
   BoardDealing(cards=(4s, 5c, 2h))
   >>> state.complete_bet_or_raise_to(9100000)  # Antonius
   CompletionBettingOrRaisingTo(player_index=0, amount=9100000)
   >>> state.complete_bet_or_raise_to(43500000)  # Blom
   CompletionBettingOrRaisingTo(player_index=1, amount=43500000)
   >>> state.complete_bet_or_raise_to(77900000)  # Antonius
   CompletionBettingOrRaisingTo(player_index=0, amount=77900000)
   >>> state.check_or_call()  # Blom
   CheckingOrCalling(player_index=1, amount=16247350)
   >>> # Below shows the turn dealing.
   >>> state.deal_board('5h')
   BoardDealing(cards=(5h,))
   >>> # Below shows the river dealing.
   >>> state.deal_board('9c')
   BoardDealing(cards=(9c,))
   >>> # Below show the final stacks.
   >>> state.stacks
   [193792375, 0]

Below shows a bad beat between Yockey and Arieh.

Link: https://youtu.be/pChCqb2FNxY

.. code-block:: pycon

   >>> state = FixedLimitDeuceToSevenLowballTripleDraw.create_state(
   ...     (
   ...         Automation.ANTE_POSTING,
   ...         Automation.BET_COLLECTION,
   ...         Automation.BLIND_OR_STRADDLE_POSTING,
   ...         Automation.CARD_BURNING,
   ...         Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
   ...         Automation.HAND_KILLING,
   ...         Automation.CHIPS_PUSHING,
   ...         Automation.CHIPS_PULLING,
   ...     ),
   ...     True,
   ...     None,
   ...     (75000, 150000),
   ...     150000,
   ...     300000,
   ...     (1180000, 4340000, 5910000, 10765000),
   ...     4,
   ... )
   >>> # Below shows the pre-flop dealings and actions.
   >>> state.deal_hole('7h6c4c3d2c')  # Yockey
   HoleDealing(player_index=0, cards=(7h, 6c, 4c, 3d, 2c), statuses=(False, False, False, False, False))
   >>> state.deal_hole('JsJcJdJhTs')  # Hui*
   HoleDealing(player_index=1, cards=(Js, Jc, Jd, Jh, Ts), statuses=(False, False, False, False, False))
   >>> state.deal_hole('KsKcKdKhTh')  # Esposito*
   HoleDealing(player_index=2, cards=(Ks, Kc, Kd, Kh, Th), statuses=(False, False, False, False, False))
   >>> state.deal_hole('AsQs6s5c3c')  # Arieh
   HoleDealing(player_index=3, cards=(As, Qs, 6s, 5c, 3c), statuses=(False, False, False, False, False))
   >>> state.fold()  # Esposito
   Folding(player_index=2)
   >>> state.complete_bet_or_raise_to()  # Arieh
   CompletionBettingOrRaisingTo(player_index=3, amount=300000)
   >>> state.complete_bet_or_raise_to()  # Yockey
   CompletionBettingOrRaisingTo(player_index=0, amount=450000)
   >>> state.fold()  # Hui
   Folding(player_index=1)
   >>> state.check_or_call()  # Arieh
   CheckingOrCalling(player_index=3, amount=150000)
   >>> # Below shows the first draw and actions.
   >>> state.stand_pat_or_discard()  # Yockey
   StandingPatOrDiscarding(player_index=0, cards=())
   >>> state.stand_pat_or_discard('AsQs')  # Arieh
   StandingPatOrDiscarding(player_index=3, cards=(As, Qs))
   >>> state.deal_hole('2hQh')  # Arieh
   HoleDealing(player_index=3, cards=(2h, Qh), statuses=(False, False))
   >>> state.complete_bet_or_raise_to()  # Yockey
   CompletionBettingOrRaisingTo(player_index=0, amount=150000)
   >>> state.check_or_call()  # Arieh
   CheckingOrCalling(player_index=3, amount=150000)
   >>> # Below shows the second draw and actions.
   >>> state.stand_pat_or_discard()  # Yockey
   StandingPatOrDiscarding(player_index=0, cards=())
   >>> state.stand_pat_or_discard('Qh')  # Arieh
   StandingPatOrDiscarding(player_index=3, cards=(Qh,))
   >>> state.deal_hole('4d')  # Arieh
   HoleDealing(player_index=3, cards=(4d,), statuses=(False,))
   >>> state.complete_bet_or_raise_to()  # Yockey
   CompletionBettingOrRaisingTo(player_index=0, amount=300000)
   >>> state.check_or_call()  # Arieh
   CheckingOrCalling(player_index=3, amount=300000)
   >>> # Below shows the third draw and actions.
   >>> state.stand_pat_or_discard()  # Yockey
   StandingPatOrDiscarding(player_index=0, cards=())
   >>> state.stand_pat_or_discard('6s')  # Arieh
   StandingPatOrDiscarding(player_index=3, cards=(6s,))
   >>> state.deal_hole('7c')  # Arieh
   HoleDealing(player_index=3, cards=(7c,), statuses=(False,))
   >>> state.complete_bet_or_raise_to()  # Yockey
   CompletionBettingOrRaisingTo(player_index=0, amount=280000)
   >>> state.check_or_call()  # Arieh
   CheckingOrCalling(player_index=3, amount=280000)
   >>> # Below show the final stacks.
   >>> state.stacks
   [0, 4190000, 5910000, 12095000]

Below shows an example badugi hand from Wikipedia.

Link: https://en.wikipedia.org/wiki/Badugi

.. code-block:: pycon

   >>> state = FixedLimitBadugi.create_state(
   ...     (
   ...         Automation.ANTE_POSTING,
   ...         Automation.BET_COLLECTION,
   ...         Automation.BLIND_OR_STRADDLE_POSTING,
   ...         Automation.CARD_BURNING,
   ...         Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
   ...         Automation.HAND_KILLING,
   ...         Automation.CHIPS_PUSHING,
   ...         Automation.CHIPS_PULLING,
   ...     ),
   ...     True,
   ...     None,
   ...     (1, 2),
   ...     2,
   ...     4,
   ...     200,
   ...     4,
   ... )
   >>> # Below shows the pre-flop dealings and actions.
   >>> state.deal_hole('As4hJcKh')  # Bob*
   HoleDealing(player_index=0, cards=(As, 4h, Jc, Kh), statuses=(False, False, False, False))
   >>> state.deal_hole('3s5d7s8s')  # Carol*
   HoleDealing(player_index=1, cards=(3s, 5d, 7s, 8s), statuses=(False, False, False, False))
   >>> state.deal_hole('KsKdQsQd')  # Ted*
   HoleDealing(player_index=2, cards=(Ks, Kd, Qs, Qd), statuses=(False, False, False, False))
   >>> state.deal_hole('2s4c6dKc')  # Alice*
   HoleDealing(player_index=3, cards=(2s, 4c, 6d, Kc), statuses=(False, False, False, False))
   >>> state.fold()  # Ted
   Folding(player_index=2)
   >>> state.check_or_call()  # Alice
   CheckingOrCalling(player_index=3, amount=2)
   >>> state.check_or_call()  # Bob
   CheckingOrCalling(player_index=0, amount=1)
   >>> state.check_or_call()  # Carol
   CheckingOrCalling(player_index=1, amount=0)
   >>> # Below shows the first draw and actions.
   >>> state.stand_pat_or_discard('JcKh')  # Bob*
   StandingPatOrDiscarding(player_index=0, cards=(Jc, Kh))
   >>> state.stand_pat_or_discard('7s8s')  # Carol*
   StandingPatOrDiscarding(player_index=1, cards=(7s, 8s))
   >>> state.stand_pat_or_discard('Kc')  # Alice*
   StandingPatOrDiscarding(player_index=3, cards=(Kc,))
   >>> state.deal_hole('TcJs')  # Bob*
   HoleDealing(player_index=0, cards=(Tc, Js), statuses=(False, False))
   >>> state.deal_hole('7cTh')  # Carol*
   HoleDealing(player_index=1, cards=(7c, Th), statuses=(False, False))
   >>> state.deal_hole('Qc')  # Alice*
   HoleDealing(player_index=3, cards=(Qc,), statuses=(False,))
   >>> state.check_or_call()  # Bob
   CheckingOrCalling(player_index=0, amount=0)
   >>> state.complete_bet_or_raise_to()  # Carol
   CompletionBettingOrRaisingTo(player_index=1, amount=2)
   >>> state.check_or_call()  # Alice
   CheckingOrCalling(player_index=3, amount=2)
   >>> state.check_or_call()  # Bob
   CheckingOrCalling(player_index=0, amount=2)
   >>> # Below shows the second draw and actions.
   >>> state.stand_pat_or_discard('Js')  # Bob*
   StandingPatOrDiscarding(player_index=0, cards=(Js,))
   >>> state.stand_pat_or_discard()  # Carol*
   StandingPatOrDiscarding(player_index=1, cards=())
   >>> state.stand_pat_or_discard('Qc')  # Alice*
   StandingPatOrDiscarding(player_index=3, cards=(Qc,))
   >>> state.deal_hole('Ts')  # Bob*
   HoleDealing(player_index=0, cards=(Ts,), statuses=(False,))
   >>> state.deal_hole('9h')  # Alice*
   HoleDealing(player_index=3, cards=(9h,), statuses=(False,))
   >>> state.check_or_call()  # Bob
   CheckingOrCalling(player_index=0, amount=0)
   >>> state.complete_bet_or_raise_to()  # Carol
   CompletionBettingOrRaisingTo(player_index=1, amount=4)
   >>> state.complete_bet_or_raise_to()  # Alice
   CompletionBettingOrRaisingTo(player_index=3, amount=8)
   >>> state.fold()  # Bob
   Folding(player_index=0)
   >>> state.check_or_call()  # Carol
   CheckingOrCalling(player_index=1, amount=4)
   >>> # Below shows the third draw and actions.
   >>> state.stand_pat_or_discard('Th')  # Carol*
   StandingPatOrDiscarding(player_index=1, cards=(Th,))
   >>> state.stand_pat_or_discard()  # Alice*
   StandingPatOrDiscarding(player_index=3, cards=())
   >>> state.deal_hole('8h')  # Carol*
   HoleDealing(player_index=1, cards=(8h,), statuses=(False,))
   >>> state.check_or_call()  # Carol
   CheckingOrCalling(player_index=1, amount=0)
   >>> state.complete_bet_or_raise_to()  # Alice
   CompletionBettingOrRaisingTo(player_index=3, amount=4)
   >>> state.check_or_call()  # Carol
   CheckingOrCalling(player_index=1, amount=4)
   >>> # Below show the final stacks.
   >>> state.stacks
   [196, 220, 200, 184]

There are more example hands in the unit tests. Please take a look at the
repository to learn more.
