#!/usr/bin/python
import itertools, random

from utils.log import log
from bots.simpleBots import BasicBot, ObviousBot


class GreedBot(BasicBot):
    """ GreedBot is Greedy.  Will put the highest bid it can whenever the prize is big enough. """
    def __init__(self, player_num, num_players, num_cards, num_games, greed_level=11):
        BasicBot.__init__(self, player_num, num_players, num_cards, num_games)
        self.greed_level = greed_level

    def take_turn(self, game_state, verbose=False):
        if game_state.prize_this_round >= self.greed_level:
            return max(game_state.current_hands[self.player_num])
        else:
            return BasicBot.take_turn(self, game_state, verbose)


class OddBot(BasicBot):
    """ While OddBot is really bad at this game, it is really fond of the odd prizes. """
    def take_turn(self, game_state, verbose=False):
        if game_state.prize_this_round % 2 != 0:
            return max(game_state.current_hands[self.player_num])
        else:
            return BasicBot.take_turn(self, game_state, verbose)


class SafeBetBot(BasicBot):
    """ SafeBetBot only bids high if it can win. """
    def __init__(self, player_num, num_players, num_cards, num_games, greed_level=10):
        BasicBot.__init__(self, player_num, num_players, num_cards, num_games)
        self.greed_level = greed_level

    def take_turn(self, game_state, verbose=False):
        confident_win = True
        my_hand = game_state.current_hands[self.player_num]
        best_card = max(my_hand)
        for hand in game_state.current_hands:
            if hand == my_hand:
                pass
            if best_card <= max(hand):
                confident_win = False
                break

        if game_state.prize_this_round >= self.greed_level and confident_win:
            return max(game_state.current_hands[self.player_num])
        else:
            return BasicBot.take_turn(self, game_state, verbose)
