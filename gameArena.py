#!/usr/bin/python

import time, copy

from utils.log import log
from gameOfPureStrategy import GameOfPureStrategy

"""
GameArena
"""
class GameArena:
	def __init__(self, num_cards, num_games, player_arr=[]):
		self.player_arr = player_arr
		self.num_cards = num_cards
		self.num_games = num_games
		self.num_players = len(player_arr)
		self.win_counter = [0 for player in range(0,self.num_players)] #all players start at 0 wins
		self.tie_counter = 0
		self.current_players = [] #array that contains the player objects, in case I want to look at them when it's over

	def play(self, play_method):
		self.start = time.time()


		log(self,"Beginning "+str(self.num_games)+" game(s)")
		for player_num, player in enumerate(self.player_arr):
			log(self," player "+str(player_num)+": "+str(player.__name__))

		total_ins = 0
		total_turns = 0


		#init players
		for player_num,player in enumerate(self.player_arr):
			self.current_players.append(player(player_num, self.num_players, self.num_cards, self.num_games))

		#begin the match
		for game_num in range(0,self.num_games):

			#check if verbose this round
			if play_method == "verbose" or (play_method == "print_last_game" and game_num == self.num_games-1):
				verbose = True
			else:
				verbose = False


			game = GameOfPureStrategy(self.num_cards, self.num_players, verbose=verbose)


			#start game
			turn_start = time.time()
			for turn in range(0, self.num_cards):
				
				#ask game to update with a new prize for the round
				game.calculate_current_prize()


				#ask all players for their turn
				turns = []
				for player in self.current_players:
					game_state = copy.deepcopy(game)
					turns.append(player.take_turn(game_state,verbose=verbose))
				#take the turn
				result = game.take_turn_if_valid(turns)

			if result >= 0: #game successfully concluded with no tie. result=winner_num
				winner_num = result
				self.win_counter[winner_num]+=1
				if verbose:
					log(self,"Round "+str(game_num)+" goes to player "+str(result)+".")
			elif result == -1:
				self.tie_counter+=1
				if verbose:
					log(self,"There was a tie. No win awarded.")#TODO: 3+ player games?
			else:
				raise ValueError("recieved unexpected return code from GameOfPureStrategy: "+result)
			total_turns += (time.time() - turn_start)

			#send end-of-game game signal to all players
			for player in self.current_players:
				player.end_game(result)


		log(self,"Complete. Results of "+str(self.num_games)+" games:")
		for player_num in range(0,self.num_players):
			log(self,"  player "+str(player_num)+": "+str(self.win_counter[player_num]))
		log(self,"Number of ties: "+str(self.tie_counter))


		log(self, "all turns took "+str(total_turns)+" seconds")

		#return the results
		return self.win_counter
		#log(self, "total accounted for time "+str(total_turns+total_ins))



