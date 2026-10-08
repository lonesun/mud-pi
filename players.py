def save(player_table):
    """Saves the data for a given player.

    Parameters:
    player_table -- a dictionary mapping player ids to their data
    """
    filename = "./dta/players.json"
    import json

    with open(filename, "w") as f:
        json.dump(player_table, f)

def load():
    """Loads the data for all players.

    Returns:
    A dictionary mapping player ids to their data
    """
    filename = "./dta/players.json"
    import json

    try:
        with open(filename, "r") as f:
            player_table = json.load(f)
            return player_table
    except FileNotFoundError:
        return {}

def forget(filename="./dta/players.json"):
    """Deletes the saved player data file.

    Parameters:
    filename -- the path to the file containing the saved player data
    """
    import os
    if os.path.exists(filename):
        os.remove(filename)
