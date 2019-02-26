#!/usr/bin/python

from utils.log import log
from bots.simpleBots import BasicBot

class PhillipAdaptoBot(BasicBot):

	def __init__(self, player_num, num_players, num_cards, num_games):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		self.player_num = player_num #I can use this to cheat I think by asking the other bots what they are planning on playing
		self.num_players = num_players #normally 2, but ideally, you should allow your bot to gracefully handle more
		self.num_cards = num_cards
		self.num_games = num_games
		
		self.current_record = 0
		self.game_count = 0
		self.state = 0 #I'll use this to cycle through strategies attempting to hard counter my opponent
		self.implemented_strategies = 8 #can only cycle through strategies that I know
		self.wobble = 0 #some secret sauce
		self.staying_power = 0
		
		
		return
	def end_game(self, result):
		#Called by GameArena upon game end. Result is the number of the winning bot previous game, -1 if tie
		#Likely want to reset any tracking variables that persist between rounds here.
		self.game_count += 1
		if result != self.player_num and self.wobble == 0:
			#It think that means I lost, and am not hard countering
			self.state += 1
			if self.state >= self.implemented_strategies:
				self.state = 0 #You're probably sunk at this point
		else:
			self.current_record += 1 - self.wobble # a little ugly, but who cares
			#this means I won, and should not change strategy
			if self.wobble == 1:
				if self.state == 3:
					self.state = 4
				elif self.state == 4:
					self.state = 3
				if result != self.player_num:
					#you lost
					self.staying_power += 1
					if self.staying_power > self.num_games/4:
						self.wobble = 0
						self.state = 5
						self.staying_power = 0
		return
	def take_turn(self, game_state, verbose = False):
		"""
		Called by GameArena when it's time to take your turn.  You are passed a "game" object with this info to work with:
		card = (int) value 1 thru num_cards
		variables available to your bot:
			self.player_num  = your player number
			self.num_players = normally 2, but ideally, you should allow your bot to gracefully handle more
			self.num_cards = normally 13, but ideally, you should allow your bot to gracefully handle any amount
			
			game_state.current_won_cards[player_num][cards] = list of cards each player has won so far
			game_state.current_scores[player_num]           = current score of each each player
			game_state.current_hands[player][cards]			= list of cards currently in each player's hand
			game_state.current_prizes[cards]                = list of prizes remaining
			game_state.prize_this_round (int)               = current prize showing for this round
		"""

		#use log(self,"text") instead of print("text") so we know what module is printing, for cleaner output
		#log(self,"This is how I do a print statement!") 
		

		#a completed bot should wrap all log statments in verbosity checks, so we don't get a flooded console if running 1000 iterations
		if verbose:
			log(self,"This is a verbose print statment!") 


		#the goal is to beat the opponent by one when possible (most effecient)
		num_cards_remaining = len(game_state.current_prizes)
		my_score = game_state.current_scores[self.player_num]
		my_current_hand = game_state.current_hands[self.player_num]
		
		if self.state == 0:#default case should be obvious bot
			play = game_state.prize_this_round
		elif self.state == 1: #bidding fairly didn't win the first round, could be playing a random bot or literally anything...
		  play = min(my_current_hand)
		elif self.state == 2:
			play = max(my_current_hand)
		elif self.state == 3: #I'll try to hard counter alex's learning bot here
			self.wobble = 1 #time to confuse learningbot
			if game_state.prize_this_round < (self.num_cards - 1):
				play = game_state.prize_this_round + 2
			else:
				play = min(my_current_hand)
			#self.state = 4
		elif self.state == 4:
			if game_state.prize_this_round > 2:
				play = game_state.prize_this_round - 2
			else:
				play = max(my_current_hand)
			#self.state = 3
		elif self.state == 5:
			play = BasicBot.take_turn(self, game_state) #can always ask the bot you extended to take the turn as a base case
		elif self.state == 6:
			if game_state.prize_this_round < self.num_cards:
				play = game_state.prize_this_round + 1
			else:
				play = 1
		elif self.state == 7:
			if game_state.prize_this_round < self.num_cards - 1:
				play = game_state.prize_this_round + 2
			else:
				play = min(my_current_hand)
				
		return play # return a card to play

class PhillipBotUpBot(BasicBot):

	def take_turn(self, game, verbose = False):
		"""
		Called by GameArena when it's time to take your turn.  You are passed a "game" object with this info to work with:

		card = (int) value 1 thru num_cards

		variables available to your bot:
			self.player_num  = your player number
			self.num_players = normally 2, but ideally, you should allow your bot to gracefully handle more
			self.num_cards = normally 13, but ideally, you should allow your bot to gracefully handle any amount
			
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
