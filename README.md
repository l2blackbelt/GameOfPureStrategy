# GameOfPureStrategy

Battlin' strategies to win the most games of the [Game of Pure Strategy (GOPS)](https://en.wikipedia.org/wiki/Goofspiel)


### [Check out the current bot leaderboard here!](scoreboard/bot_scores.md)

## What is this?
I found GOPS interesting, due to the facts that 
1. it is the only extant pure strategy card game (no luck of the draw), and 
2. it is currently unsolved >4 cards by modern mathematics

I thought it would be fun to try my hand at designing strategies to play this game, and pitting them against each other to see which won out.
So I wrote a bunch of python classes to simulate games of GOPS, and an object-oriented structure that make it easy for anyone to write classes to play.

If you dig this half as much as I do, perhaps you want to make a bot and see how it performs.  If so, here's what you need to know:

## How do I use this?
* play_GOPS.py is the module that kicks off test games.
	* Bots are passed by the class to GameArena, so you can easily modify:
		* which bots participate, 
		* how many games to play
		* how to print to console.  (useful for figuring out how bots play and tweaking strategy)

## Think you can do better?
I do my official tests with 2 bots, 100,000 runs, and 13 cards.

1. Create your bot(s), and place them in a new python file in the [bots](bots) directory. 
	* *Check out required bot format in [bots/A_sampleBot.py](bots/A_sampleBot.py)*
2. Send me a pull request with your bot.  I'll add your bot to the leaderboard :)




