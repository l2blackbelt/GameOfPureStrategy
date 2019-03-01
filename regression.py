import scoreboard


def bot_regression():

	num_games = 5 #test bots can handle more than one game
	num_cards = 13
	bot_names = []
	bots_to_skip = ["HumanBot"] #these bots cannot be regessed

	bot_classes = scoreboard._get_bot_classes(bots_to_skip)
	num_bots = len(bot_classes)


	#verify all bots can run 1v1 for 5 games
	for i in range(0,num_bots,2):
		bot1_name, bot1_class = bot_classes[i]
		bot2_name, bot2_class = bot_classes[(i+1)%num_bots] #wrap back around if there's not an even number of bots

		print(str(bot1_name)+" vs "+str(bot2_name))
		scoreboard._play_game(num_cards=num_cards, num_games=num_games, player_arr=[bot1_class, bot2_class])


if __name__== "__main__":
	bot_regression()

