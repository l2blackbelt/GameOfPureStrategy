#!/usr/bin/python

from utils.log import log
from bots.simpleBots import BasicBot

class PhillipBotUpBot(BasicBot):

	def take_turn(self, game, verbose = False):
		"""
		card = (int) value 1 thru num_cards

		variables available to your bot:
			player_num (int) = player index for this bot.  Used to look up data for self and opponent(s) in the game_state object
			prize_card (int) = prize card currently showing, to bid on.
			game_state.current_won_cards[player_num][cards] = list of cards each player has won so far
			game_state.current_scores[player_num]           = current score of each each player
			game_state.current_hands[player][cards]			= list of cards currently in each player's hand
			game_state.current_prizes[cards]                = list of prizes remaining
			game_state.prize_this_round (int)               = current prize showing for this round
		"""
		num_cards_remaining = len(game.current_prizes)
		my_score = game.current_scores[self.player_num]
		my_current_hand = game.current_hands[self.player_num]
		
		if (my_score > 0) or (game.prize_this_round == 12):
			play = max(my_current_hand)
		else:
			play = min(my_current_hand) #base strategy, need to add tweaks later
		return play