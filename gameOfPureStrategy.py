#!/usr/bin/python

import random

from utils.log import log

"""
GameOfPureStrategy
This structure contains all the logic to play GOPS.
It will check if all the plays and the prize are valid, then will update the game state
	return -9999 as long as the game continues
	return -1 if game completes in a tie
	return winner_num if game completes in a win
"""
class GameOfPureStrategy:

	def __init__(self, num_cards, num_players, prize_order="random", verbose=False):

		self.num_players = num_players
		self.current_won_cards = [[] for player in range(0,num_players)] #all players start with no cards
		self.current_scores = [0 for player in range(0,num_players)]
		self.current_hands = []
		self.current_prizes = []
		self.prize_this_round = 0
		self.prize_order = prize_order
		self.verbose = verbose

		starting_hand = [card for card in range(1,num_cards+1)]

		#initialize remaining deck (points to collect) to be the same as starting hand
		self.current_prizes = list(starting_hand)

		#initialize current_hands to be all the cards for each player
		for player in range(0,num_players):
			self.current_hands.append(list(starting_hand))

		if self.verbose:
			self.log_status()

	def log_status(self):
		log(self,"Current hands:")
		for player_num,player_hand in enumerate(self.current_hands):
			log(self," player "+str(player_num))
			log(self,"  hand  : "+str(player_hand))
			log(self,"  won cards: "+str(self.current_won_cards[player_num]))
			log(self,"  scores: "+str(self.current_scores[player_num]))
		log(self,"Current prizes left:")
		log(self," "+str(self.current_prizes))

	def calculate_current_prize(self):
		if self.prize_this_round in self.current_prizes: 
			raise ValueError("FAIL! Prize has already been calculated for this round")

		if self.prize_order=="sequential": 
			self.prize_this_round = self.current_prizes[0]
		elif self.prize_order=="random":   
			self.prize_this_round = self.current_prizes[random.randint(0,len(self.current_prizes)-1)]
		else: 
			raise ValueError("What the hell you doin with an unsupported prize_order")


	def take_turn_if_valid(self, play_array=[]):

		if self.prize_this_round not in self.current_prizes: 
			raise ValueError("FAIL! Play cannot start before prize is calculated")

		if len(play_array) != self.num_players:
			raise ValueError("FAIL! Expect one card played for each of the "+str(self.num_players)+" players")

		for player_num,play in enumerate(play_array):
			if play not in self.current_hands[player_num]:
				raise ValueError("FAIL! player "+str(player_num)+" does not have card "+str(play)+" available to play")

		if self.prize_this_round not in self.current_prizes:
			raise ValueError("FAIL! Prize value "+str(self.prize_this_round)+" is not available")

		#if passed all checks, take the turn
		return self.__take_turn(play_array)

	def __take_turn(self, play_array=[]):

		#passed an array of player scores, return an array of all those who tied for first place
		def find_winners(player_scores):
			winning_score = 0
			winning_players = [] #list, in case players tie for first
			for player_num,score in enumerate(player_scores):
				if score > winning_score:
					winning_score = score
					winning_players = [player_num]
				elif score == winning_score:
					winning_players.append(player_num)
			return winning_players, winning_score

		#remove prize from prize pool
		self.current_prizes.remove(self.prize_this_round)
		if self.verbose:
			log(self,"prize is "+str(self.prize_this_round))

		#remove played card from each player's hand
		for player_num,play in enumerate(play_array):
			self.current_hands[player_num].remove(play)
			if self.verbose:
				log(self,"player "+str(player_num)+" played "+str(play))

		#figure out which play won the hand
		winners_of_the_hand, winning_play = find_winners(play_array)

		#award prize for the hand
		if len(winners_of_the_hand) == 1:
			hand_winner = winners_of_the_hand[0]
			self.current_won_cards[hand_winner].append(self.prize_this_round) 
			self.current_scores[hand_winner]+=self.prize_this_round
			if self.verbose:
				log(self,"RESULT: "+str(self.prize_this_round)+" points awarded to player "+str(hand_winner)+"\n")
		elif self.verbose:
			log(self,"RESULT: There was a tie for first between players "+str(winners_of_the_hand)+" with "+str(winning_play)+" and no points were awarded\n")

		if self.verbose:
			self.log_status()


		#end the game and declare winner if all prizes are awarded
		if len(self.current_prizes)==0:

			#figure out which player won the game
			final_scores = [sum(won_cards_per_player) for won_cards_per_player in self.current_won_cards]
			winners_of_the_game, winning_score = find_winners(final_scores)

			if len(winners_of_the_game)>1:
				if self.verbose:
					log(self,"GAME OVER. tie between players "+str(winners_of_the_game)+" with "+str(winning_score)+" points")
					log(self,"----------------------------------\n")
				return -1

			else:
				if self.verbose:
					log(self,"GAME OVER. player "+str(winners_of_the_game[0])+" wins with "+str(winning_score)+" points")
					log(self,"----------------------------------\n")
				return winners_of_the_game[0]				

		return -9999

