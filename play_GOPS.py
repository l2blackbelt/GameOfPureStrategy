#!/usr/bin/env python


from gameArena import GameArena

#import all the bots
from bots.simpleBots import *
from bots.alexBots import *
from bots.philBots import *
from bots.brianBots import *
from bots.JamesBots import *

#make python 2 and 3 behave the same for raw input
if hasattr(__builtins__, 'raw_input'):
    input = raw_input



#play the game
def main():



	#play_method
	#quiet = display nothing but the results
	#verbose = display everything, including optional bot outputs.
	#print_last_game = play quiet until the last game, then display verbose output

	#TODO: 1_wins = play quiet until player x wins, stop and display verbose output  #TO-DO, not implemented
	game = GameArena(num_cards=3, num_games=10, player_arr=[HumanBot, ObviousBot], prize_order='sequential')
	game.play(play_method = "verbose")




###########################################################################################


if __name__== "__main__":
	main()



