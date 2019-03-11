#!/usr/bin/python

from utils.log import log
from bots.simpleBots import BasicBot
import random

def get_Chosen(nums):
	chosen = []
	while True:
		if len(nums) == 0:
			break
		idx = random.randint(0,len(nums)-1)
		if not nums[idx] in chosen:
			chosen.append(nums[idx])
			total = 0
			for x in chosen:
				total = total + x
			total += nums[idx]
			nums.remove(nums[idx])
			if total >= 46:
				break
	chosen.sort(reverse = True)
	return chosen



class HalfPointsBot(BasicBot): #can extend one of the simple bots, BasicBot, ObviousBot, RandomBot
	#these are the three methods called by GameArena.  If your bot doesn't need one, you can delete it.

	def __init__(self, player_num, num_players, num_cards, num_games):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		nums = list(range(1,num_cards))
		self.chosen = get_Chosen(nums)
		self.player_num = player_num #your player number
		self.num_players = num_players #normally 2, but ideally, you should allow your bot to gracefully handle more
		self.num_cards = num_cards
		return
	def end_game(self, result):
		#Called by GameArena upon game end. Result is the number of the winning bot previous game, -1 if tie
		#Likely want to reset any tracking variables that persist between rounds here.
		nums = list(range(1,self.num_cards))
		self.chosen = get_Chosen(nums)
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
			log(self, str(self.chosen) )


		#do fun logic
		if not game_state.prize_this_round in self.chosen:
			return min(game_state.current_hands[self.player_num])
		else:
			finder = self.chosen.index(game_state.prize_this_round)
			return game_state.current_hands[self.player_num][-finder:][0]

class HalfPointsAdaptBot(BasicBot): #can extend one of the simple bots, BasicBot, ObviousBot, RandomBot
	#these are the three methods called by GameArena.  If your bot doesn't need one, you can delete it.

	def __init__(self, player_num, num_players, num_cards, num_games):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		nums = list(range(1,num_cards))
		self.abort_BotUp = 0
		self.abort_Obvious = 0
		self.chosen = get_Chosen(nums)
		self.player_num = player_num #your player number
		self.num_players = num_players #normally 2, but ideally, you should allow your bot to gracefully handle more
		self.num_cards = num_cards
		self.last_wins = 0
		return
	def end_game(self, result):
		#Called by GameArena upon game end. Result is the number of the winning bot previous game, -1 if tie
		#Likely want to reset any tracking variables that persist between rounds here.
		nums = list(range(1,self.num_cards))
		self.chosen = get_Chosen(nums)
		self.abort_Obvious = 0
		self.abort_BotUp = 0
		self.last_wins = 0
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
			log(self, str(self.chosen) )


		#do fun logic
		safe_to_use = 1
		for i in range(0,self.num_players):
			if i != self.player_num:

				if self.num_players == 2:
					
					if sum(game_state.current_prizes) == sum(game_state.current_hands[i]):
						self.abort_Obvious += 1
					
					if len(game_state.current_prizes) == (self.num_cards - int(round(float(self.num_cards)*0.3))) and sum(game_state.current_hands[i]) >= (sum(range(1,self.num_cards)) - 13):
						self.abort_BotUp = 1

				if max(game_state.current_hands[self.player_num]) > max(game_state.current_hands[i]):
					safe_to_use = 1
				else:
					safe_to_use = 0

		#if len(game_state.current_prizes) >= 5 and (game_state.prize_this_round + game_state.current_scores[self.player_num]) > max(game_state.current_scores):
		#	return max(game_state.current_hands[self.player_num])

		if self.abort_Obvious > 4:
			if (game_state.prize_this_round + 1) in game_state.current_hands[self.player_num]:
				return (game_state.prize_this_round + 1)
			else:
				return min(game_state.current_hands[self.player_num])

		if self.abort_BotUp == 1:
			idx = int(len(game_state.current_hands[self.player_num])/2)
			return game_state.current_hands[self.player_num][idx]

		if safe_to_use == 1 and max(game_state.current_prizes) == game_state.prize_this_round:
			if game_state.prize_this_round in self.chosen:
				self.chosen.remove(game_state.prize_this_round)
			return max(game_state.current_hands[self.player_num])

		if not game_state.prize_this_round in self.chosen:
			return min(game_state.current_hands[self.player_num])
		else:
			finder = self.chosen.index(game_state.prize_this_round)
			self.chosen.remove(game_state.prize_this_round)
			if len(game_state.current_hands[self.player_num]) == 1:
				return game_state.current_hands[self.player_num][0]
			elif game_state.current_hands[self.player_num][-(finder):][0] == 13:
				return game_state.current_hands[self.player_num][-(finder+1):][0]
			else:
				return game_state.current_hands[self.player_num][-(finder):][0]

class BuyingPowerBot(BasicBot): #can extend one of the simple bots, BasicBot, ObviousBot, RandomBot
	#these are the three methods called by GameArena.  If your bot doesn't need one, you can delete it.

	def __init__(self, player_num, num_players, num_cards, num_games):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		nums = list(range(1,num_cards))
		self.player_num = player_num #your player number
		self.num_players = num_players #normally 2, but ideally, you should allow your bot to gracefully handle more
		self.num_cards = num_cards
		self.total_prize = sum(nums)
		self.abort_Max = 0
		self.abort_Three = 0
		return
	def end_game(self, result):
		self.abort_Max = 0
		self.abort_Three = 0
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
		my_hand = game_state.current_hands[self.player_num]
		power = []
		score = game_state.current_scores[self.player_num]
		same = 0
		for i in range(0,self.num_players):
			if i != self.player_num:

				power.append(sum(game_state.current_hands[i]))
				if score == game_state.current_scores[i]:
					same = 1
				else:
					same = 0

				if max(game_state.current_hands[self.player_num]) > max(game_state.current_hands[i]):
					safe_to_use = 1
				else:
					safe_to_use = 0


		my_buying_power = sum(my_hand) - max(power)

		if verbose:
			log(self, str(my_buying_power) )

		percentage = [-3,-2,-1, 0, 1, 2, 2]
		high_percentage = [1, 2, 3]
		idx = random.randint(0,len(percentage)-1)
		high_idx = random.randint(0,len(high_percentage)-1)

		if len(my_hand) == 2 and same == 1 and self.abort_Three == 0:
			if game_state.prize_this_round > game_state.current_prizes[0]:
				return max(my_hand)
			else:
				return min(my_hand)

		if self.abort_Three == 1:
			return max(my_hand)	
		
		if safe_to_use == 1 and max(game_state.current_prizes) == game_state.prize_this_round:
			return max(game_state.current_hands[self.player_num])

		if len(my_hand) == 3 and same == 1:
			if (game_state.prize_this_round + min(game_state.current_prizes)) < max(game_state.current_prizes):
				return min(my_hand)
			else:
				self.abort_Three = 1
				my_hand.remove(min(my_hand))
				return min(my_hand)
	
		if self.abort_Max == 1:
			return max(my_hand)

		if len(my_hand) == self.num_cards:
			return min(my_hand)
			#if (game_state.prize_this_round + percentage[idx]) in my_hand:
			#	return (game_state.prize_this_round + percentage[idx])
			#else:
			#	return min(my_hand)
		elif my_buying_power > 7:
			if (game_state.prize_this_round + high_percentage[high_idx]) in my_hand:
				return (game_state.prize_this_round + high_percentage[high_idx])
			else:
				return min(my_hand)
		elif game_state.prize_this_round >= self.num_cards/2 and my_buying_power > 3:
			if (game_state.prize_this_round + percentage[idx]) in my_hand:
				return (game_state.prize_this_round + percentage[idx])
			else:
				return min(my_hand)

		if my_buying_power > sum(game_state.current_prizes)/2:
			self.abort_Max = 1
			return max(my_hand)
		else:
			return min(my_hand)
 
	#	if (game_state.prize_this_round+1) in my_hand:
	#		return (game_state.prize_this_round+1)
	#	elif (game_state.prize_this_round+1) >= self.num_cards:
	#		return max(my_hand)
	#	elif (game_state.prize_this_round + sum(game_state.current_prizes) + game_state.current_scores[self.player_num]) < self.total_prize:
	#		return max(my_hand)
	#	else:
	#		return min(my_hand)


