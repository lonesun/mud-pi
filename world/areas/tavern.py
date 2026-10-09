import time

from . import into_overworld_map, get_season, get_weather

SEASON = get_season()
WEATHER = get_weather()

import random
random_objects = ["a mug", "a chair", "a table", "a barrel"]

seasonal = {
    "tavern": {
        "spring": "The tavern is adorned with fresh flowers and a light breeze flows through the open windows",
        "summer": "The tavern is filled with the warm glow of sunlight streaming through the windows",
        "autumn": "The tavern is decorated with autumn leaves and the air is crisp with the changing season",
        "winter": "The tavern is warm and cozy, with a roaring fire and snow falling outside the windows"
    },
    "outside": {
        "spring": "The outside of the tavern is lively with the sounds of spring, birds chirping and flowers blooming",
        "summer": "The outside of the tavern is bathed in the warm summer sun, with people enjoying the pleasant weather",
        "autumn": "The outside of the tavern is adorned with colorful autumn leaves, and the air is crisp and cool",
        "winter": "The outside of the tavern is covered in a blanket of snow, with icicles hanging from the roof"
    }
}

gebiet = {
    "Tavern": {
        "name": "The Prancing Pony",
        "acting_cue": " You can see {}.".format(random.choice(random_objects)),
        "energy": "The air feels " + ("warm and pleasant" if SEASON == "summer" else "crisp and cool" if SEASON == "autumn" else "fresh and invigorating" if SEASON == "spring" else "cold and biting") + ".",
        "description": "{}.".format(seasonal["tavern"][SEASON]),
        "exits": {
            "outside": "Outside",
        },
        "area": "tavern01",
    },
    "Outside": {
        "name": "Outside the Prancing Pony",
        "acting_cue": "You can see {}.\nThe weather is {}.".format(random.choice(random_objects), WEATHER),
        "energy": "The air feels " + ("warm and pleasant" if SEASON == "summer" else "crisp and cool" if SEASON == "autumn" else "fresh and invigorating" if SEASON == "spring" else "cold and biting") + ".",
        "description": "{}. The weather is {}.".format(seasonal["outside"][SEASON], WEATHER),
        "exits": {
            "inside": "Tavern",
            "path": "Forest",
        },
        "area": "tavern01",
    }
}

into_overworld_map(gebiet)
