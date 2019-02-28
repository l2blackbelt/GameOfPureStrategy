import scoreboard


def bot_regression():

	num_games = 5 #test bots can handle more than one game
	num_cards = 13
	bot_names = []
	scoreboard._generate_json(num_games,num_cards,bot_names)  #let all the bots run against each other and see if there's an error

if __name__== "__main__":
	bot_regression()

