import json
import multiprocessing as mp
import os

readme_file = "scoreboard_out.md"
data_file = "data_out.json"


if os.getenv('DOCKER'):
    data_file = "/home/jovyan/data_out.json"
    readme_file = "/home/jovyan/scoreboard_out.md"


# any bot class names to leave off the scoreboard for various reasons.
bots_to_skip = ["HumanBot", "WatchingBot", "InterestingBot_2", "SampleBot"]


def play_bots(combination_data):
    from gameArena import GameArena
    bot1_name, bot1_class = combination_data[0]
    bot2_name, bot2_class = combination_data[1]
    num_cards = combination_data[2]
    num_games = combination_data[3]

    print(str(bot1_name) + " vs " + str(bot2_name))
    import sys
    sys.stdout.flush()
    game = GameArena(num_cards=num_cards, num_games=num_games, player_arr=[bot1_class, bot2_class])
    bot1_score, bot2_score = game.play(play_method="quiet")

    return bot1_name, bot1_score, bot2_name, bot2_score


def _get_bot_classes(bots_to_skip=None):
    import inspect, importlib, os

    bot_classes = []
    # import all the bot python files
    for bot_file in os.listdir("bots"):

        # skip files that don't seem like bots
        if "bot" not in bot_file.lower() or not bot_file.endswith(".py"):
            continue

        bot_file = bot_file[:-3]  # remove *.py
        print("importing " + str(bot_file))
        bot_module = importlib.import_module("bots." + bot_file)
        bot_tuples = inspect.getmembers(bot_module, inspect.isclass)
        for bot_name, bot_class in bot_tuples:
            if bot_file not in str(bot_class):
                # ignore inherited bots
                continue
            if bot_name in bots_to_skip:
                # ignore bots to skip
                print("  skip " + bot_name)
                continue
            print("  found " + bot_name)
            # get list of bots from bot modules
            bot_classes.append([bot_name, bot_class])
    return bot_classes


# return results from playing games
def _play_game(num_games, num_cards, player_arr):
    from gameArena import GameArena
    game = GameArena(num_cards=num_cards, num_games=num_games, player_arr=player_arr)
    return game.play(play_method="quiet")


# generate scoreboard json by running games
def _generate_json(num_games, num_cards, bot_names):
    import itertools, time, sys

    start = time.time()

    bot_classes = _get_bot_classes(bots_to_skip=bots_to_skip)

    # generate bot combinations; either all bots vs all others, or just run specified bots vs all others
    if bot_names:
        # scoreboard update: just pit the named bots vs all others
        with open('scoreboard/data.json', 'r') as infile:
            bot_results = json.load(infile)
        # print(bot_results)
        combinations = []
        for bot1_name in bot_names:
            bot_results[bot1_name] = {}

            # find bot by name
            bot1 = None
            for bot in bot_classes:
                bot_name = bot[0]
                if bot1_name == bot_name:
                    bot1 = bot
                    break
            if not bot1:
                raise Exception("Cannot find bot " + bot1_name)
            for bot2 in bot_classes:
                if bot1 != bot2:
                    combinations.append((bot1, bot2))
    else:
        # scoreboard refresh: pit all the bots against each other
        bot_results = {bot[0]: {} for bot in bot_classes}
        combinations = itertools.combinations(bot_classes, 2)

    combination_data = []
    for combination in combinations:
        combination_data.append(combination + (num_cards, num_games))

    # turn each game into a process:
    cpu_count = mp.cpu_count()
    print("Number of processors: ", cpu_count)

    results = []
    if cpu_count > 1:
        print("we're multiprocessing, gentlemen")
        pool = mp.Pool(cpu_count)
        results = pool.map(play_bots, combination_data)
    else:
        print("we're single-threaded, boyos")
        sys.stdout.flush()
        for combo in combination_data:
            results.append(play_bots(combo))
            sys.stdout.flush()
    # update player results
    for result in results:
        bot1_name, bot1_score, bot2_name, bot2_score = result

        bot_results[bot1_name][bot2_name] = bot1_score
        bot_results[bot2_name][bot1_name] = bot2_score

    with open(data_file, 'w') as outfile:
        json.dump(bot_results, outfile, indent=4, sort_keys=True)
    # print(bot_results)

    print("Completed scoreboard in " + str(time.time() - start) + " seconds")


# generate readme scoreboard from the raw json data
def _generate_readme(num_games, num_cards):
    import operator
    with open(data_file) as f:
        data = json.load(f)

        # get wins per bot
        wins_per_bot = {name: {} for name in data.keys() if name not in bots_to_skip}
        for bot_name, result in data.items():
            if bot_name in bots_to_skip:
                continue
            wins = 0
            for result_name, result_number in result.items():
                if result_name in bots_to_skip:
                    continue
                if result_number > num_games / 2:
                    wins += 1
            wins_per_bot[bot_name] = wins

        sorted_bots = sorted(wins_per_bot.items(), key=operator.itemgetter(1))
        sorted_bots.reverse()
        # print(sorted_bots)

        # print ranked bots
        with open(readme_file, "w") as o:
            o.write("# Bot Scores\n")
            o.write("Results of " + str(num_games) + " 1v1 games, with " + str(num_cards) + " cards each\n\n")
            o.write("|rank|bot|score|results|\n")
            o.write("|-----|-----|-----|-----|\n")
            i = 0
            last_wins = num_games
            for bot_name, wins in sorted_bots:
                if wins < last_wins:
                    i += 1  # handle ties
                last_wins = wins
                # be obnoxious about scores

                o.write("|**#" + str(i) + "**|" + str(bot_name) + "|" + str(wins) + "|")

                sorted_opponents = sorted(data[bot_name].items(), key=operator.itemgetter(1))
                sorted_opponents.reverse()
                for opponent, won_games in sorted_opponents:
                    if opponent in bots_to_skip:
                        continue
                    win_percent = round(won_games / num_games * 100, 2)
                    if win_percent > 50:
                        o.write("WIN ")
                    else:
                        o.write("LOSS ")
                    o.write(str(win_percent) + "% vs " + str(opponent) + "<br>")
                o.write("|\n")


def generate_scoreboard(num_games=10, num_cards=13, bot_names=None):
    _generate_json(num_games, num_cards, bot_names)
    _generate_readme(num_games, num_cards)


if __name__ == "__main__":
    import sys
    print("--ARGV--")

    for arg in sys.argv:

        print(arg)
    print("--ARGV--")

    generate_scoreboard(bot_names=['SmarterLearningBot','Simple3NeuralBot'])
