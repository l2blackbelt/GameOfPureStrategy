# GameOfPureStrategy
python classes to play GOPS

##What in the sweet Jesus is this?
I thought the Game Of Pure Stratergy was really cool, so I created a python class, GameOfPureStrategy, to simulate a game of it.
Then I created GameArena so I could simulate multiple games in a row.  Then I started creating more complicated bots.  I'm not sure what happened, but I'm here, with a very flexible and friendly implementation of GOPS in python, where competing "solutions" can fight head to head for the most wins in nerdy combat.

And now that you're here, we're here together.

If you dig this half as much as I do, perhaps you want to make a bot and see how it performs.  If so, here's what you need to know:

##How do I use this?

play_GOPS.py is the module that kicks off games.  

You can easily modify which bots participate, how many games to play, and how to print to console.

If you want to make a new bot, check out bots/A_samplebot.py which provides a template, along with instructions.


##Current Champs to beat
I do my official tests with 2 bots, 100,000 runs, and 13 cards.


Right now, the (semi) deterministic bot to beat is InterestingBot, which handly beats other deterministic bots, and creams RandomBot up to 86% of the time.

The Learning bot to beat is LearningBot, which absolutely curb-stomps InterestingBot 80% of the time.


If you think your bot is the shiznit, send me a pull request, and we shall do battle.