#!/usr/bin/python

from utils.log import log
from bots.simpleBots import BasicBot

class SampleBot(BasicBot): #can extend one of the simple bots, BasicBot, ObviousBot, RandomBot
	#these are the three methods called by GameArena.  If your bot doesn't need one, you can delete it.

	def __init__(self, player_num, num_players, num_cards):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		self.player_num = player_num #your player number
		self.num_players = num_players #normally 2, but ideally, you should allow your bot to gracefully handle more
		self.num_cards = num_cards
		return
	def end_game(self, result):
		#Called by GameArena upon game end. Result is the number of the winning bot previous game, -1 if tie
		#Likely want to reset any tracking variables that persist between rounds here.
		return
	def take_turn(self, game_state, verbose = False):
		"""
		Called by GameArena when it's time to take your turn.  You are passed a "game" object with this info to work with:

			game_state.current_won_cards[player_num][cards] = list of cards each player has won so far
			game_state.current_scores[player_num]           = current score of each each player
			game_state.current_hands[player][cards]			= list of cards currently in each player's hand
			game_state.current_prizes[cards]                = list of prizes remaining
			game_state.prize_this_round (int)               = current prize showing for this round
		"""

		#use log(self,"text") instead of print("text") so we know what module is printing, for cleaner output
		log(self,"This is how I do a print statement!") 
		

		#a completed bot should wrap all log statments in verbosity checks, so we don't get a flooded console if running 1000 iterations
		if verbose:
			log(self,"This is a verbose print statment!") 


		#do fun logic
		num_cards_remaining = len(game_state.current_prizes)
		my_score = game_state.current_scores[self.player_num]
		my_current_hand = game_state.current_hands[self.player_num]

		if (my_score > 0) or (game_state.prize_this_round == 12):
			play = max(my_current_hand)
		else:
			play = BasicBot.take_turn(game_state) #can always ask the bot you extended to take the turn as a base case
		
		return play # return a card to play