import time

area_array = {}
"""Holds array of all areas."""

def into_overworld_map(new_rooms):
    area_array.update(new_rooms)

__all__ = ["area_array", "into_overworld_map", "get_season"]
"""Exports the area array, the function to add new rooms, and the function to get the current season."""

def get_season():
    week = int(time.strftime("%U"))
    if 12 <= week < 25:
        return "spring"
    elif 25 <= week < 38:
        return "summer"
    elif 38 <= week < 51:
        return "autumn"
    else:
        return "winter"
