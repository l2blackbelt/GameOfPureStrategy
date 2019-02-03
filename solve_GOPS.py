#!/usr/bin/python

import random, time, itertools, copy

#make python 2 and 3 behave the same for raw input
if hasattr(__builtins__, 'raw_input'):
    input = raw_input

def log(self,string):
	print(str(self.__class__.__name__)+": "+string)



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
			log(self,"  scores: "+str(sum(self.current_won_cards[player_num])))
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


"""
GameArena
"""
class GameArena:
	def __init__(self, num_cards, num_games, player_arr=[], verbose = 0):
		self.player_arr = player_arr
		self.num_cards = num_cards
		self.num_games = num_games
		self.num_players = len(player_arr)
		self.win_counter = [0 for player in range(0,self.num_players)] #all players start at 0 wins
		self.tie_counter = 0
		self.verbose = verbose #0=display final result, 1=display winner of each gane, 2=full game state per round

		self.current_players = [] #array that contains the player objects, in case I want to look at them when it's over

	def play(self):
		self.start = time.time()


		log(self,"Beginning "+str(self.num_games)+" game(s)")

		total_ins = 0
		total_turns = 0


		#init first game, and players
		game = GameOfPureStrategy(self.num_cards, self.num_players, verbose=False)

		for player_num,player in enumerate(self.player_arr):
			initial_game_state = copy.deepcopy(game) #we deepcopy to prevent bots from accidentally/maliciously modifying game data
			self.current_players.append(player(player_num, initial_game_state))

		for game_num in range(0,self.num_games):

			game = GameOfPureStrategy(self.num_cards, self.num_players, verbose=(self.verbose > 1))


			#start game
			turn_start = time.time()
			for turn in range(0, self.num_cards):
				
				#ask game to update with a new prize for the round
				game.calculate_current_prize()


				#ask all players for their turn
				turns = []
				for player in self.current_players:
					game_state = copy.deepcopy(game)
					turns.append(player.take_turn(game_state))
				#take the turn
				result = game.take_turn_if_valid(turns)

			if result >= 0: #game successfully concluded with no tie. result=winner_num
				winner_num = result
				self.win_counter[winner_num]+=1
				if self.verbose >= 1:
					log(self,"Round "+str(game_num)+" goes to player "+str(result)+".")
			elif result == -1:
				self.tie_counter+=1
				if self.verbose >= 1:
					log(self,"There was a tie. No win awarded.")#TODO: 3+ player games?
			else:
				raise ValueError("recieved unexpected return code from GameOfPureStrategy: "+result)
			total_turns += (time.time() - turn_start)

			#send end-of-game game signal to all players
			for player in self.current_players:
				player.end_game(result)

		#send end-of-game game signal to all players
		for player in self.current_players:
			player.end_match()


		log(self,"Complete. Results of "+str(self.num_games)+" games:")
		for player_num in range(0,self.num_players):
			log(self,"  player "+str(player_num)+": "+str(self.win_counter[player_num]))
		log(self,"Number of ties: "+str(self.tie_counter))


		log(self, "all turns took "+str(total_turns)+" seconds")
		#log(self, "total accounted for time "+str(total_turns+total_ins))




#######################################

"""
BasicBot
This basic bot will play the next card in its hard every turn
All competing bots should extend this model
"""
class BasicBot:
	def __init__(self, player_num, initial_game_state):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		self.player_num = player_num
		return
	def end_game(self, result):
		#Called by GameArena upon game end. Result is the number of the winning bot previous game, -1 if tie
		return
	def end_match(self):
		#Called by GameArena upon match end. (Useful for printing any stats the bot collected)
		return
	def take_turn(self, game_state):
		"""
		card = (int) value 1 thru num_cards

		variables available to your bot:
			player_num (int) = player index for this bot.  Used to look up data for self and opponent(s) in the game_state object
			prize_card (int) = prize card currently showing, to bid on.
			game_state.current_won_cards[player_num][cards] = list of cards each player has won so far
			game_state.current_hands[player][cards]			= list of cards currently in each player's hand
			game_state.current_prizes[cards]                = list of prizes remaining
			game_state.prize_this_round (int)               = current prize showing for this round
		"""

		#Basic bot returns the first card in their hand
		return game_state.current_hands[self.player_num][0]
"""
RandomBot
this random bot will play the cards available to it at random
"""
class RandomBot(BasicBot):
	def take_turn(self, game_state):
		#select a card at a random index to play from list of available cards
		my_current_hand = game_state.current_hands[self.player_num]
		random_card_index = random.randint(0,len(my_current_hand)-1)

		random_play = my_current_hand[random_card_index]
		return random_play
"""
ObviousBot
this obvious bot will always match whatever card is face up with a card from its hand
"""
class ObviousBot(BasicBot):
	def take_turn(self, game_state):
		#duplicate whatever prize card is on the table
		obvious_play = game_state.prize_this_round
		my_current_hand = game_state.current_hands[self.player_num]

		if obvious_play in my_current_hand:
			return obvious_play
		else:
			return BasicBot.take_turn(self,game_state)
"""
HumanBot
this human bot allows a human to play via the python command line
"""
class HumanBot(BasicBot):
	def take_turn(self, game_state):

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

"""
LearningBot plays like an obviousbot, but also recording your moves.  
once it has a certain certainty of what it thinks you'll do given a card, it plays the counterstrategy

Currently, though it gathers data on all players, it can only account for one player's plays at a time
"""
class LearningBot(ObviousBot):
	def __init__(self, player_num, initial_game_state, just_watch = False):
		#Bot is initialized once at the beginning of the competition, and persists between games.
		self.player_num = player_num
		self.num_players = len(initial_game_state.current_hands)
		self.num_cards = len(initial_game_state.current_prizes)
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
		log(self,"Current frequency_array")
		log(self, " x = frequency opponent plays response 1-"+str(self.num_cards)+" given prize")
		for i,e in enumerate(self.frequency_array):
			log(self,"prize="+str(i+1)+" "+str(e))


	def end_game(self, result):
		#reset counter on new game
		self.__note_last_move([])
		self.opponent_hand_last_round = None

	def end_match(self):
		self.__print_current_frequency_array()

	def take_turn(self, game_state):

		#record moves from last round
		if self.opponent_hand_last_round != None: #if not first round of the first game
			self.__note_last_move(game_state.current_hands[self.player_to_beat])


		#if have history to base on, play best counter
		frequency_array_given_prize = self.frequency_array[game_state.prize_this_round-1]
		their_most_likely_play = frequency_array_given_prize.index(max(frequency_array_given_prize))+1
		if their_most_likely_play == self.num_cards:
			best_play = 1
		else:
			best_play = their_most_likely_play+1

		#play best play if card available, else play a random available card
		if not self.just_watch and best_play in game_state.current_hands[self.player_num]:
			play = best_play
		else:
			play =  ObviousBot.take_turn(self,game_state)


		self.prize_last_round = game_state.prize_this_round #keep this for next turn
		self.opponent_hand_last_round = [card for card in game_state.current_hands[self.player_to_beat]]
		return play


class WatchingBot(LearningBot):
	def __init__(self, game, player_num):
		LearningBot.__init__(self,game,player_num,just_watch = True)

class InterestingBot(BasicBot):
	#this bot figures out how many of the highest cards it needs (decending) to win 
	#	TODO: change to weighted random, with 2<min fewest possible cards preferred.
	#if (card it thinks it needs): bid minimum needed to get that card, knowing that other players played.
	#	Should have a max overbid value I can edit
	#if (card it doesn't need): Throw away a low card.
	#majority of the points, bidding low until it finds a card it "needs"
	#knows what other player's cards are, and will bid the lowest card it can in order to get it.
	def __init__(self, player_num, initial_game_state, max_overbid = 1, verbose = False):
		#give the bot access to game state variables
		self.player_num = player_num
		self.verbose = verbose

		num_cards = len(initial_game_state.current_prizes)
		num_players = len(initial_game_state.current_hands)
		num_points = sum(initial_game_state.current_prizes) #never initialize a bot in the middle of a game, bro.

		self.points_needed = num_points/num_players+1  #this is the minimum points needed to win
		self.starting_num_cards_to_desire = int(num_cards/num_players) #don't attempt to win more than my "share" of rounds

		###tweak these
		#self.ignore_top = 2  #ignore these many of the "top" cards, unless sure win.  #TODO, implement?
		#self.max_overwin_multiplier = 1  #TODO: maximum amount the bot will try to "overwin" aka not win by the exact necessary amount
		#self.max_overwin = 5
		self.max_overbid = max_overbid
		#self.max_assume_opponent_overbid = 3
		###

		self.game_end(-1)

	def game_end(self, result):
		self.my_won_cards = []
		self.list_of_desired_cards = []


	def generate_list_of_desired_cards(self,game):
		cur_list = []
		num_cards = len(game.current_prizes)
		num_players = len(game.current_hands)
		my_won_cards = game.current_won_cards[self.player_num]
		num_my_won_cards = len(my_won_cards)
		my_score = sum(my_won_cards)
		num_cards_to_desire =  min(max(self.starting_num_cards_to_desire-num_my_won_cards,1), num_cards) #need to tweak number of cards to desire as pool shrinks

		for subset in itertools.combinations(game.current_prizes,num_cards_to_desire):
			#max_overwin = #TODO: this changes throughout the game, bot will consider more agressive strategies earlier, then get more conservative upon later recalculates.
			points_to_win = sum(subset) + my_score
			if points_to_win >= self.points_needed:# TODO: overwin      and points_to_win - self.points_needed < self.max_overwin:
				cur_list.append(subset)

		if len(cur_list)==0:
			if self.verbose:
				log(self,"Crap, I'm conceding.")
			return game.current_prizes #shit, I'm gunna lose.  Just try to get everything

		return cur_list[random.randint(0,len(cur_list)-1)]


	def take_turn(self, game):

		#update my list of cards I won, and generate a flattened list of cards opponents won
		opponents_won_cards = [card for player_num,hand in enumerate(game.current_won_cards) for card in hand if player_num!=self.player_num] 
		my_won_cards = game.current_won_cards[self.player_num]
		prize_card = game.prize_this_round
		
		if self.list_of_desired_cards == [] or [i for i in opponents_won_cards if i in self.list_of_desired_cards]:  #check if someone won a card I want
			self.list_of_desired_cards = self.generate_list_of_desired_cards(game) #generate need new strategy.
			if self.verbose:
				log(self,"recalculating list...")
		if self.verbose:
			log(self,"list: "+str(self.list_of_desired_cards))


		my_current_hand = game.current_hands[self.player_num]

		if prize_card in self.list_of_desired_cards:
			self.check_last_round_points = True  #I care about the results of this, and need to recalculate
			if self.verbose:
				log(self,"I want it")

			#TODO: what's the lowest card, up to my max bid, I can play? (considering their hand)
			#try to play my max bid if possible, otherwise, play highest card I can.
			for card in range(prize_card+self.max_overbid,1,-1):
				if card in my_current_hand:
					return card
		else:
			if self.verbose:
				log(self,"I don't care")
			self.check_last_round_points = False
		return min(my_current_hand)  #return lowest card if I can't do anything else

#class inheretence.  Instantiates an interestingbot but overwites max_overbid in init.
class InterestingBot_2(InterestingBot):
	def __init__(self, game, player_num):
		InterestingBot.__init__(self,game,player_num,max_overbid = 2)

class WinBot:
	#i want to recurse through all the possibilities, and generate a lookup table for every possible game state.
	#For every play in the game, I want to make sure I play the card that gives me the most opportunities to win
	#perhaps ties I randomly break.
	def generate_lookup_table(self, num_cards, num_players):
		pass  #needs more work


class PhillipBotUpBot(BasicBot):
	def __init__(self,initial_game_state,player_num):
		#give the bot access to game state variables
		self.player_num = player_num
		self.num_cards = len(game.current_prizes)

	def take_turn(self, game):
		"""
		card = (int) value 1 thru num_cards

		variables available to your bot:
			player_num (int) = player index for this bot.  Used to look up data for self and opponent(s) in the game_state object
			prize_card (int) = prize card currently showing, to bid on.
			game_state.current_won_cards[player_num][cards] = list of cards each player has won so far
			game_state.current_hands[player][cards]			= list of cards currently in each player's hand
			game_state.current_prizes[cards]                = list of prizes remaining
			game_state.prize_this_round (int)               = current prize showing for this round
		"""
		num_cards_remaining = len(game.current_prizes)
		my_score = self.game.current_scores[self.player_num]
		my_current_hand = self.game.current_hands[self.player_num]
		
		if (my_score > 0) or (prize_card == 12):
			play = max(my_current_hand)
		else:
			play = min(my_current_hand) #base strategy, need to add tweaks later
		return play



###########################################################################################



def main():
	start = time.time()


	game = GameArena(num_cards=13, num_games=100000, player_arr=[LearningBot, InterestingBot], verbose=0)
	game.play()


	end = time.time()
	print("Completed in "+str(end - start)+" seconds")



###########################################################################################


if __name__== "__main__":
	main()



