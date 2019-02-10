# GameOfPureStrategy

Battlin' strategies to win the most games of the [Game of Pure Strategy (GOPS)](https://en.wikipedia.org/wiki/Goofspiel)


### [Check out the current bot leaderboard here!](bot_scores.md)

## What in the sweet Jesus is this?
I thought the Game Of Pure Stratergy was really cool, so I created a python class, GameOfPureStrategy, to simulate a game of it.
Then I created GameArena so I could simulate multiple games in a row.  Then I started creating ever more complicated bots to play.  I'm not sure what happened, now I have a very flexible implementation of GOPS in python, **where competing "solutions" can fight head to head for the most wins in nerdy combat.**

And now that you're here, we're here together.

If you dig this half as much as I do, perhaps you want to make a bot and see how it performs.  If so, here's what you need to know:

## How do I use this?
* play_GOPS.py is the module that kicks off games.
	* Bots are passed by the class to GameArena, so you can easily modify:
		* which bots participate, 
		* how many games to play
		* how to print to console.  (useful for figuring out how bots play and tweaking strategy)

## Think you can do better?
I do my official tests with 2 bots, 100,000 runs, and 13 cards.

1. Create your bot(s), and place them in a new python file in the [bots](bots) directory. 
	* *Check out required bot format in [bots/A_sampleBot.py](bots/A_sampleBot.py)*
2. Send me a pull request with your bot.  I'll add your bot to the leaderboard :)




