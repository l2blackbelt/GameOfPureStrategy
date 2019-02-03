#!/usr/bin/python
import random

"""
BasicBot
This basic bot will play the next card in its hard every turn
All competing bots should extend this model
"""
class BasicBot:
	def __init__(self, player_num, num_players, num_cards):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		self.player_num = player_num
		self.num_players = num_players
		self.num_cards = num_cards
		return
	def end_game(self, result):
		#Called by GameArena upon game end. Result is the number of the winning bot previous game, -1 if tie
		return

	def _play_between(self, my_current_hand, starting_card_value, ending_card_value, i):
		#utility function to play the first available card between starting_card_value, ending_card_value, incrementer i
		for card in range(starting_card_value,ending_card_value,i):
			if card in my_current_hand:
				return card
		return 0 #couldn't find the card in my hand

	def take_turn(self, game_state, verbose = False):

		#Basic bot returns the lowest card in their hand
		return min(game_state.current_hands[self.player_num])

"""
ObviousBot
this obvious bot will always try to play value of prize + offset, else play BasicBot
"""
class ObviousBot(BasicBot):

	def take_turn(self, game_state, verbose = False, offset = 0):
		#play whatever card is on the table, plus offset, if applicable
		obvious_play = (game_state.prize_this_round + offset-1) % self.num_cards+1
		my_current_hand = game_state.current_hands[self.player_num]

		if obvious_play in my_current_hand:
			return obvious_play
		else:
			return BasicBot.take_turn(self,game_state)

class ObviousPlusOneBot(ObviousBot):
	def take_turn(self, game_state, verbose = False):
		return ObviousBot.take_turn(self,game_state,verbose=verbose,offset=1)




"""
RandomBot
this random bot will play the cards available to it at random
"""
class RandomBot(BasicBot):
	def take_turn(self, game_state, verbose = False):
		#select a card at a random index to play from list of available cards
		my_current_hand = game_state.current_hands[self.player_num]
		random_card_index = random.randint(0,len(my_current_hand)-1)

		random_play = my_current_hand[random_card_index]
		return random_play


"""
HumanBot
this human bot allows a human to play via the python command line
"""
class HumanBot(BasicBot):
	def take_turn(self, game_state, verbose = False):

		log(self,"--You are player "+str(self.player_num))
		log(self,"--Current prize card: "+str(game_state.prize_this_round))

		play_ok = False
		while(play_ok == False):
			
			try:
				human_play = int(input("Enter your play: "))
			except ValueError:
				log(self,"That's not a number....")
				continue
			except (KeyboardInterrupt, EOFError) as e:
				print("\n\n  quitter.\n")
				exit(0)
			if human_play not in game_state.current_hands[self.player_num]:
				log(self,"card '"+str(human_play)+"' is not available to you.  Try again.")
			else:
				play_ok = True

		return human_play