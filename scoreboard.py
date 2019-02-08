#!/usr/bin/python

from utils.log import log

from bots import *
#make python 2 and 3 behave the same for raw input
if hasattr(__builtins__, 'raw_input'):
    input = raw_input







#import all the bots
from bots.simpleBots import BasicBot, ObviousBot, RandomBot, HumanBot, ObviousPlusOneBot
from bots.alexBots import LearningBot, WatchingBot, InterestingBot
from bots.philBots import PhillipBotUpBot
from bots.brianBots import GreedBot, SafeBetBot, OddBot



#any bot class names to leave off the scoreboard for various reasons.
bots_to_skip = ["HumanBot"]




import inspect, sys, itertools, json, time

#getattr(bots, "HumanBot")

clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
print(clsmembers)



#########rest of imports go here ###########
from gameArena import GameArena
############################################


num_games = 100000
num_cards = 13


start = time.time()

bot_names = [bot[0] for bot in clsmembers]
bot_results = { name:{} for name in bot_names}


for combination in itertools.combinations(clsmembers,2):
	bot1_name, bot1_class = combination[0]
	bot2_name, bot2_class = combination[1]

	if bot1_name in bots_to_skip or bot2_name in bots_to_skip:
		continue

	print(str(bot1_name)+" vs "+str(bot2_name))
	game = GameArena(num_cards=num_cards, num_games=num_games, player_arr=[bot1_class, bot2_class])
	bot1_score, bot2_score = game.play(play_method = "quiet")
	
	#update player results
	bot_results[bot1_name][bot2_name] = bot1_score
	bot_results[bot2_name][bot1_name] = bot2_score


with open('data.json', 'w') as outfile:
    json.dump(bot_results, outfile, indent=4, sort_keys=True)
print(bot_results)

print("Completed scoreboard in "+str(time.time()-start)+" seconds")
