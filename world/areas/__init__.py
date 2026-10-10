import time

area_array = {}
"""Holds array of all areas."""

def into_overworld_map(new_rooms):
    area_array.update(new_rooms)

__all__ = ["area_array", "into_overworld_map", "get_season", "get_weather", "get_recipients"]
"""Exports the area array, the function to add new rooms, the function to get the current season, and the function to get the current weather."""

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

def get_weather():
    # Placeholder function for getting the current weather
    return "clear"

EXCLUDE_SENDER = {"gush"}
"""Commands whose output is not shown to the player who sent them."""

def get_recipients(command, sender_id, candidate_ids):
    """Returns the player ids that should receive a command's output."""
    if command in EXCLUDE_SENDER:
        return [pid for pid in candidate_ids if pid != sender_id]
    return list(candidate_ids)
