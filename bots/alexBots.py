#!/usr/bin/python
import itertools, random

from utils.log import log
from bots.simpleBots import BasicBot, ObviousBot


class InterestingBot(BasicBot):
	#this bot figures out how many of the highest cards it needs (decending) to win
	#majority of the points, bidding low until it finds a card it "needs"
	#knows what other player's cards are, and will bid the lowest card it can in order to get it.
	def __init__(self, player_num, num_players, num_cards, num_games, max_overbid = 1):
		#give the bot access to game state variables
		BasicBot.__init__(self, player_num, num_players,num_cards)

		num_points = sum([i for i in range(0,num_cards)])

		self.points_needed = num_points/num_players+1  #this is the minimum points needed to win
		self.starting_num_cards_to_desire = int(num_cards/num_players) #don't attempt to win more than my "share" of rounds

		###tweak these
		#self.ignore_top = 2  #ignore these many of the "top" cards, unless sure win.  #TODO, implement?
		#self.max_overwin_multiplier = 1  #TODO: maximum amount the bot will try to "overwin" aka not win by the exact necessary amount
		#self.max_overwin = 5
		self.max_overbid = max_overbid
		#self.max_assume_opponent_overbid = 3
		###

		self.end_game(-1)

	def end_game(self, result):
		self.my_won_cards = []
		self.list_of_desired_cards = []

	def __generate_list_of_desired_cards(self,game,verbose):
		cur_list = []
		my_won_cards = game.current_won_cards[self.player_num]
		num_my_won_cards = len(my_won_cards)
		
		my_score = sum(my_won_cards)

		#sum all points on the table and in score piles, subtract points I already scored, divide by num players, add 1
		points_needed = int((sum([sum(game.current_won_cards[player_num])for player_num in range(0,self.num_players) if player_num != self.player_num]) + sum(game.current_prizes) - my_score)/self.num_players)+1
		
		if verbose:
			log(self,"Need points to win: "+str(points_needed))
		num_cards_to_desire =  min(max(self.starting_num_cards_to_desire-num_my_won_cards,1), self.num_cards) #need to tweak number of cards to desire as pool shrinks

		for subset in itertools.combinations(game.current_prizes,num_cards_to_desire):
			#max_overwin = #TODO: this changes throughout the game, bot will consider more agressive strategies earlier, then get more conservative upon later recalculates.
			points_to_win = sum(subset) + my_score
			if points_to_win >= points_needed:# TODO: overwin      and points_to_win - self.points_needed < self.max_overwin:
				cur_list.append(subset)

		if len(cur_list)==0:
			if verbose:
				log(self,"Crap, I'm conceding.")
			return game.current_prizes #shit, I'm gunna lose.  Just try to get everything

		return cur_list[random.randint(0,len(cur_list)-1)]  #pick a list at random from available options


	def take_turn(self, game, verbose = False):

		#update my list of cards I won, and generate a flattened list of cards opponents won
		opponents_won_cards = [card for player_num,hand in enumerate(game.current_won_cards) for card in hand if player_num!=self.player_num] 
		my_won_cards = game.current_won_cards[self.player_num]
		prize_card = game.prize_this_round
		
		if not self.list_of_desired_cards or [i for i in opponents_won_cards if i in self.list_of_desired_cards]:  #check if someone won a card I want
			if verbose:
				log(self,"recalculating list...")
			self.list_of_desired_cards = self.__generate_list_of_desired_cards(game,verbose) #generate need new strategy.

		if verbose:
			log(self,"list: "+str(self.list_of_desired_cards))


		my_current_hand = game.current_hands[self.player_num]

		if prize_card in self.list_of_desired_cards:
			if verbose:
				log(self,"I want it")


			#play the highest card I need to secure the round, knowing opponent's hand, up to my max bid
			max_card_in_opponent_hand = max([max(game.current_hands[player_num])for player_num in range(0,self.num_players) if player_num != self.player_num])
			highest_bid = prize_card+self.max_overbid
			#log(self,str(max_card_in_opponent_hand)+" "+str(highest_bid)) #TODO-SAW SOME WERID BEHAVIOR here, should have noticed max card was lower
			play = 0
			#first check and see if I can play lower than my max bid
			if max_card_in_opponent_hand < highest_bid:
				if verbose:
					log(self,"I see my highest opponent's card is "+str(max_card_in_opponent_hand))
				play = self._play_between(my_current_hand,max_card_in_opponent_hand+1, highest_bid, 1)
			#if I don't have that card, play the highest card I have up to my max bid
			if not play:
				play = self._play_between(my_current_hand,highest_bid,1,-1)
			#if I don't have that card, play the max card I have in my hand
			if not play:
				play = max(my_current_hand)

		else:
			play = min(my_current_hand)
			if verbose:
				log(self,"I don't care")
		
		return play

#class inheretence.  Instantiates an interestingbot but overwites max_overbid in init.
class InterestingBot_2(InterestingBot):
	def __init__(self, player_num, num_players, num_cards, num_games):
		InterestingBot.__init__(self,player_num,num_players,num_cards, num_games, max_overbid = 2)



class LearningBot(ObviousBot):
	def __init__(self, player_num, num_players, num_cards, just_watch = False):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		ObviousBot.__init__(self, player_num, num_players,num_cards)

		#this array of arrays is indexed 1-num_cards.  At each index is another array 1-num_cards that is the probibility of your opponent picking that card
		#frequency_array[player][card][frequency-of-each-card-played]
		self.frequency_array = [[ 0 for card in range(0,self.num_cards)] for card1 in range(0,self.num_cards)] #all players start with no cards

		#note these variables are formatted to be array indexes and are 1 less than the card face value.
		self.prize_last_round = -1
		self.opponent_hand_last_round = None

		self.player_to_beat = self.num_players - self.player_num - 1
		self.just_watch = just_watch
		return

	def __note_last_move(self,opponent_current_hand):
		played_card_last_round = [play for play in self.opponent_hand_last_round if play not in opponent_current_hand]
		played_card_last_round = played_card_last_round[0]
		self.frequency_array[self.prize_last_round-1][played_card_last_round-1] +=1

	def __print_current_frequency_array(self):
		log(self,"Tracking player "+str(self.player_to_beat))
		log(self,"Current frequency_array")
		log(self, " x = frequency opponent plays response 1-"+str(self.num_cards)+" given prize")
		for i,e in enumerate(self.frequency_array):
			log(self,"prize="+str(i+1)+" "+str(e))


	def end_game(self, result):
		#reset counter on new game
		self.__note_last_move([])
		self.opponent_hand_last_round = None
		

	def take_turn(self, game_state, verbose = False):

		#record moves from last round
		if self.opponent_hand_last_round != None: #if not first round of a game
			self.__note_last_move(game_state.current_hands[self.player_to_beat])


		#if have history to base on, play best counter
		frequency_array_given_prize = self.frequency_array[game_state.prize_this_round-1]
		their_most_likely_play = frequency_array_given_prize.index(max(frequency_array_given_prize))+1
		if their_most_likely_play == self.num_cards:
			best_play = 1
		else:
			best_play = their_most_likely_play+1

		#play best play if card is available, else play like ObviousBot
		if not self.just_watch and best_play in game_state.current_hands[self.player_num]:
			play = best_play
		else:
			play =  ObviousBot.take_turn(self,game_state)


		self.prize_last_round = game_state.prize_this_round #keep this for next turn
		self.opponent_hand_last_round = [card for card in game_state.current_hands[self.player_to_beat]]

		if verbose:
			self.__print_current_frequency_array()

		return play


class WatchingBot(LearningBot):
	def __init__(self, player_num, num_players, num_cards):
		LearningBot.__init__(self,player_num,num_players,num_cards,just_watch = True)