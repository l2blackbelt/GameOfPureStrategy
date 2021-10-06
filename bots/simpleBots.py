#!/usr/bin/python
import random
from utils.log import log

"""
BasicBot
This basic bot will play the next card in its hard every turn
All competing bots should extend this model
"""
class BasicBot:
	def __init__(self, player_num, num_players, num_cards, num_games):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		self.player_num = player_num
		self.num_players = num_players
		self.num_cards = num_cards
		self.num_games = num_games
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
	def __init__(self, player_num, num_players, num_cards, num_games):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		self.player_num = player_num
		self.num_players = num_players
		self.num_cards = num_cards
		self.num_games = num_games
		return
	def take_turn(self, game_state, verbose = False):

		log(self,"--You are player {}".format(self.player_num))
		log(self,"--Current prize card: {}".format(game_state.prize_this_round))
		log(self, 'Predicted Value: {}'.format(predictedValueCalculator(self, game_state)))

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

"""
calculate predicted value loss =0, tie = 0.5, win =1 revisit.
todo:
formalize in numbers what it means to be only able to tie, or also lose next move.  I think this would be 0.25  (half shot of tying)
"""
def predictedValueCalculator(chosen_bot, game_state):
	num_cards = game_state.num_cards
	my_id = chosen_bot.player_num

	my_score = game_state.current_scores[my_id]
	their_score = game_state.current_scores[1-my_id]
	my_hand = game_state.current_hands[my_id]
	their_hand = game_state.current_hands[1-my_id]

	points_available = sum(game_state.current_prizes)
	points_possible = sum([i+1 for i in range(num_cards)])

	# helpful stats maybe
	log(chosen_bot, "points available = {}".format(points_available))

	# I wonder how the simplification of summation would actually work?
	# It's not a general solution by any means but I wanna know how well it plays.

	if num_cards >13 or num_cards <2:
		return "? good luck."

	# rules cover: 2 card game.
	# Hands match.  Will "predict" one trivial way to tie.
	if my_hand == their_hand and my_score == their_score:
		return 0.5

	# trivial state, you have more points than remain to be gotten
	if my_score > points_possible/2:
		return 1

	# trivial state, they have more points than remain to be gotten
	if their_score > points_available/2:
		return 0

	#predicted value calculator cannot know anything about either player's stretegy.
	#therefore in a 3 card game where I try to invert obviousbot, the best I can do is tie, but I could also lose. half chance of tying = 0.25
	#
	if num_cards == 3:
		if
	return "ohhhh sheeeeeeit"

