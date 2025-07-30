from enum import Enum
from abc import ABC, abstractmethod

class Unit(ABC):

    def __init__(self, location) -> None:
        self._location = location
        self.order = None

    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, loc):
        self._location = loc
        loc.occupied = True
        # TODO: set occupied back to false at some point

class Army(Unit):

    def __init__(self, location) -> None:
        super().__init__(location)

    def __str__(self) -> str:
        return "Army"

class Fleet(Unit):
    def __init__(self, location) -> None:
        super().__init__(location)

    def __str__(self) -> str:
        return "Fleet"

# class Plane(Unit):
#     def move(self):
#         print("MOVE !!!")

#     def __init__(self, id: int = -1, power = None) -> None:
#         super().__init__(id, power)

#     def __str__(self) -> str:
#         return "Plane"