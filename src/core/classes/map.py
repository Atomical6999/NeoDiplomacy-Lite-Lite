from core.classes.units import *

from enum import Enum, StrEnum
from abc import ABC, abstractmethod
from typing import Optional
from loguru import logger

class ProvinceType(Enum):
    LAND = 0
    SEA = 1
    COASTAL = 2

class Power():
    def __init__(self, name: str, adjective: str, color: str, home_territory: list = [], supply_centers: list = [], units: list[Unit] = []) -> None:
        self.name: str = name
        self.adjective: str = adjective
        self.color: str = color
        self.home_territory: list[Province] = home_territory
        self.supply_centers: list[Province] = supply_centers
        self.units: list[Unit] = units

    def __str__(self) -> str:
        return f"Name: {self.name}\nHome Territory: Not implemented\nSupply Centers: Not implemented"

class CoastType(StrEnum):
    NC = "NC"
    NEC = "NEC"
    EC = "EC"
    SEC = "SEC"
    SC = "SC"
    SWC = "SWC"
    WC = "WC"
    NWC = "NWC"

# class Coast(Moveable):
#     def __init__(self, coast_type: CoastType, adjacencies: list = []) -> None:
#         super().__init__(adjacencies)
#         self.coast_type: CoastType = coast_type

#     def __str__(self) -> str:
#         return f"Type: {self.coast_type}\nAdjacencies: {self.adjacencies}"

class Province():
    def __init__(self, name: str, abbreviation: str, aliases: list[str], type: str, adjacencies: list[str]) -> None:
        self.name: str = name
        self.abbreviation: str = abbreviation
        self.aliases: list[str] = aliases
        self.type: str = type
        self.adjacencies_str: list[str] = adjacencies
        self.adjacencies: list[Province] = []

        self.hold_strength: int = 0 # Strength to prevent a unit moving into this province. Empty = 0
        self.occupied: bool = False

    def __str__(self) -> str:
        adjacency_names = ""
        if self.adjacencies != []:
            for province in self.adjacencies:
                adjacency_names += " " + province.name

        return f"Name: {self.name}\nAbbreviation: {self.abbreviation}\nType: {self.type}\nAdjacencies:{adjacency_names if adjacency_names != "" else self.adjacencies_str}"

class Map():
    # @staticmethod
    # def get_power_by_id(id: int, powers: list[Power]) -> Optional[Power]:
    #     for power in powers:
    #         if power.id == id:
    #             return power

    # @staticmethod
    # def get_unit_by_id(id: int, units: list[Unit]) -> Optional[Unit]:
    #     for unit in units:
    #         if unit.id == id:
    #             return unit

    # @staticmethod
    # def get_province_by_id(id: int, provinces: list[Province]) -> Optional[Province]:
    #     for province in provinces:
    #         if province.id == id:
    #             return province
    #     return None

    # def search_provinces(self, query: str) -> Optional[Province]:
    #     for province in self.provinces:
    #         fixed_query = query.strip().upper()
    #         if province.name.strip().upper() == fixed_query:
    #             return province
    #         elif province.abbreviation.strip().upper() == fixed_query:
    #             return province
    #     return None

    # def get_home_territories_of_power(self, power: Power) -> list[Province]:
    #     """Returns a list of all provinces that are the home territory of a provided power, as described in the province editor."""
    #     home_territories: list[Province] = []
    #     for province in self.provinces:
    #         if province.home_territory == power:
    #             home_territories.append(province)
    #     return home_territories

    def get_unit_from_province(self, province: Province) -> Optional[Unit]:
        for power in self.powers:
            for unit in power.units:
                if unit.location == province:
                    return unit
                
    def get_unit_power_from_province(self, province: Province) -> Optional[Power]:
        for power in self.powers:
            for unit in power.units:
                if unit.location == province:
                    return power

    def search_province_by_name(self, search_string: str) -> Optional[Province]:
        """Searches the map's provinces for a Province, first checking against name, then abbreviation, then aliases."""
        for province in self.provinces:
            if province.name.strip().upper() == search_string or province.abbreviation.strip().upper() == search_string or search_string in province.aliases:
                return province
    
    def search_power_by_name(self, search_string: str) -> Optional[Power]:
        """Searches the map's powers and returns one if found"""
        for power in self.powers:
            if power.name.strip().upper() == search_string:
                return power

    def update_adjacencies(self) -> None:
        for province in self.provinces:
            # print(f"Updating {province}")
            adjacencies: list[Province] = []
            for adjacency in province.adjacencies_str:
                adjacent_province = self.search_province_by_name(adjacency)
                # print(f"Adjacent province: {adjacent_province}")
                if adjacent_province is not None:
                    adjacencies.append(adjacent_province)
            
            province.adjacencies = adjacencies

    def __init__(self, name: str, description: str, version: str, author: str, starting_year: int, starting_season: str, seasons: list[str], powers: list[Power] = [], provinces: list[Province] = []) -> None:
        self.name: str = name
        self.description: str = description
        self.version: str = version
        self.author: str = author
        self.starting_year: int = starting_year
        self.starting_season: str = starting_season
        self.seasons: list[str] = seasons
        self.powers: list[Power] = powers
        self.provinces: list[Province] = provinces

    def __str__(self) -> str:
        return f"Name: {self.name}\nPowers ({len(self.powers)}): {[power.name for power in self.powers]}\nProvinces ({len(self.provinces)}): {[province.name for province in self.provinces]}"