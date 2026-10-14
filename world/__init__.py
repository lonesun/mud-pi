"""Holds array of all areas.
Provides access to function(`into_overworld_map(new_rooms)`) for adding new rooms.
"""
from .areas import area_array, into_overworld_map
from .areas import tavern  # noqa: F401  registers the tavern rooms
from .areas import forest  # noqa: F401  registers the forest rooms

__all__ = ["area_array", "into_overworld_map"]
