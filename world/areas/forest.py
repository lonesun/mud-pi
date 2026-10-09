from . import into_overworld_map, get_season, get_weather

SEASON = get_season()
WEATHER = get_weather()

import random
random_objects = ["a flower", "a tree", "a gnome", "a fox"]

seasonal = {
    "spring": "The forest is adorned with fresh flowers and a light breeze flows through the trees",
    "summer": "The forest is filled with the warm glow of sunlight streaming through the trees",
    "autumn": "The forest is decorated with autumn leaves and the air is crisp with the changing season",
    "winter": "The forest is quiet and serene, with snow covering the ground and a crisp chill in the air"
}

gebiet = {

    "Forest": {
        "name": "Grey Forest",
        "acting_cue": "You can see {}".format(random.choice(random_objects)),
        "energy": "The air feels " + ("warm and pleasant" if SEASON == "summer" else "crisp and cool" if SEASON == "autumn" else "fresh and invigorating" if SEASON == "spring" else "cold and biting") + ".",
        "description": "{}.".format(seasonal[SEASON]),
        "exits": {"inside": "Tavern"},
        "area": "forest01",
    }
}

into_overworld_map(gebiet)
