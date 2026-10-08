import time

from . import into_overworld_map, get_season, get_weather

SEASON = get_season()
print("Current season:", SEASON)
WEATHER = get_weather()
print("Current weather:", WEATHER)

import random
random_objects = ["a mug", "a chair", "a table", "a barrel"]

seasonal = {
    "spring": "The tavern is adorned with fresh flowers and a light breeze flows through the open windows",
    "summer": "The tavern is filled with the warm glow of sunlight streaming through the windows",
    "autumn": "The tavern is decorated with autumn leaves and the air is crisp with the changing season",
    "winter": "The tavern is warm and cozy, with a roaring fire and snow falling outside the windows"
}

gebiet = {
    "Tavern": {
        "description": "{}. You can see {}.".format(seasonal[SEASON], random.choice(random_objects)),
        "exits": {"outside": "Outside"},
    },
    "Outside": {
        "description": "You're standing outside a tavern. The weather is {}.".format(WEATHER),
        "exits": {"inside": "Tavern"},
    }
}

into_overworld_map(gebiet)