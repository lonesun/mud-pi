area_array = {}
"""Holds array of all areas."""

def into_overworld_map(new_rooms):
    area_array.update(new_rooms)

__all__ = ["area_array", "into_overworld_map"]
"""Exports the area array and the function to add new rooms."""