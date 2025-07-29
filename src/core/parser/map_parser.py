import orjson
import os
from loguru import logger
from typing import Optional

from core.classes.map import *
from core.classes.units import *


def parse_map(path: str) -> Map:
    json: dict
    with open(path, "r+") as f:
        json = orjson.loads(f.read())
    
    name = json["name"]
    description = json["description"]
    version = json["version"]
    author = json["author"]
    starting_year = json["startingYear"]
    starting_season = json["startingSeason"]
    seasons = json["seasons"]
    powers: list[Power] = []
    provinces = []

    new_map = Map(
        name=name,
        description=description,
        version=version,
        author=author,
        starting_year=starting_year,
        starting_season=starting_season,
        seasons=seasons
    )

    for province in json["provinces"]:
        name = province["name"]
        abbreviation = province["abbreviation"]
        aliases = province["aliases"]
        province_type = province["type"]
        adjacencies = province["adjacencies"]
        provinces.append(
            Province(
                name=name,
                abbreviation=abbreviation,
                aliases=aliases,
                type=province_type,
                adjacencies=adjacencies
            )
        )
    
    new_map.provinces = provinces
    new_map.update_adjacencies()

    for power in json["powers"]:
        name = power["name"]
        adjective = power["adjective"]
        color = power["color"]

        home_territory: list[Province] = []
        for province in power["homeTerritory"]:
            search_result = new_map.search_province_by_name(province)
            if search_result is not None:
                home_territory.append(search_result)
        
        supply_centers: list[Province] = []
        for province in power["supplyCenters"]:
            search_result = new_map.search_province_by_name(province)
            if search_result is not None:
                supply_centers.append(search_result)
        
        units: list[Unit] = []
        for unit in power["units"]:
            location = new_map.search_province_by_name(unit["location"])

            new_unit: Optional[Unit] = None
            match unit["type"]:
                case "Army":
                    new_unit = Army(location=location)
                case "Fleet":
                    new_unit = Fleet(location=location)
            
            if new_unit is not None:
                units.append(new_unit)
        
        powers.append(Power(
            name=name,
            adjective=adjective,
            color=color,
            home_territory=home_territory,
            supply_centers=supply_centers,
            units=units
        ))
    
    new_map.powers = powers

    return new_map

# def _parse_map(path: str) -> Map:
#     json: dict
#     with open(path, "r+") as f:
#         json = orjson.loads(f.read())

#     map_id = 0
#     name = ""
#     powers: list[Power] = []
#     provinces = []
#     units = []

#     for map_property in json["map"]:
#         match map_property:
#             case "id":
#                 map_id = json["map"]["id"]
#             case "name":
#                 name = json["map"]["name"]
#             case "powers":
#                 for power in json["map"]["powers"]:
#                     new_power = Power(
#                         id=power["id"],
#                         name=power["name"]
#                     )
#                     powers.append(new_power)
#             case "provinces":
#                 for province in json["map"]["provinces"]:
#                     new_province = Province(
#                         id=province["id"],
#                         name=province["name"],
#                         abbreviation=province["abbreviation"],
#                         type=province["type"],
#                         adjacencies=province["adjacencies"],
#                         home_territory=Map.get_power_by_id(province["home_territory"], powers),
#                         is_supply_center=province["is_supply_point"],
#                         occupied_units=province["occupied_units"]
#                     )
#                     provinces.append(new_province)
#             case "units":
#                 for unit in json["map"]["units"]:
#                     new_unit: Optional[Unit] = None
#                     if unit["power"] == None:
#                         logger.error(f"Unit with id {unit['id']} does not have an associated power.")
#                         continue

#                     power = Map.get_power_by_id(unit["power"], powers)
#                     if power == None:
#                         logger.error(f"Power with id {unit['power']} could not be found.")
#                         continue

#                     match unit["type"]:
#                         case UnitType.ARMY:
#                             new_unit = Army(unit["id"], power)
#                         case UnitType.FLEET:
#                             new_unit = Fleet(unit["id"], power)
#                         case UnitType.PLANE:
#                             new_unit = Plane(unit["id"], power)
#                         case _:
#                             logger.error(f"Invalid Unit type {unit['type']} for Unit id {unit['id']} - Accepts {list(UnitType)}")
#                     if new_unit is not None:
#                         units.append(new_unit)
#             case _:
#                 logger.warning("Unknown key.")

#     for province in provinces:
#         # Parse units
#         new_units: list[Unit] = []
#         for unit_id in province.occupied_units:
#             unit = Map.get_unit_by_id(id=unit_id, units=units)
#             if unit is not None:
#                 new_units.append(unit)
#             else:
#                 logger.warning(f"Province with id {unit_id} not found in occupied uints of Province id {province.id}")

#         province.occupied_units = new_units

#         # Parse adjacencies
#         new_adjacencies: list[Province] = []
#         for province_id in province.adjacencies:
#             p = Map.get_province_by_id(id=province_id, provinces=provinces)
#             if isinstance(p, Province):
#                 if p.id == province.id:
#                     logger.error(f"Province with id {province.id} is adjacent to itself. Skipping...")
#                     continue

#                 new_adjacencies.append(p)
#             else:
#                 logger.warning(f"Province with id {province_id} not found in adjacencies of Province id {province.id}")

#         province.adjacencies = new_adjacencies

#     return Map(id=map_id, name=name, powers=powers, provinces=provinces)

# def save_map(nd_map: Map, path: str) -> None:
#     json_save = {}
#     map_dict = {}

#     map_dict["name"] = nd_map.name

#     # Powers
#     powers = []
#     for count, power in enumerate(nd_map.powers):
#         power_dict: dict = {}

#         power.id = count
#         power_dict["id"] = power.id
#         power_dict["name"] = power.name
#         powers.append(power_dict)
#     map_dict["powers"] = powers

#     # Units
#     units = []
#     index = 0
#     for province in nd_map.provinces:
#         for unit in province.occupied_units:
#             unit_dict: dict = {}

#             unit.id = index
#             unit_dict["id"] = unit.id

#             if isinstance(unit, Army):
#                 unit_dict["type"] = UnitType.ARMY
#             elif isinstance(unit, Fleet):
#                 unit_dict["type"] = UnitType.FLEET
#             elif isinstance(unit, Plane):
#                 unit_dict["type"] = UnitType.PLANE

#             for power in nd_map.powers:
#                 if unit.power:
#                     if power.id == unit.power.id:
#                         unit_dict["power"] = power.id
#                         continue
#                 else:
#                     unit_dict["power"] = -1

#             units.append(unit_dict)
#             index += 1

#     # Provinces
#     for count, province in enumerate(nd_map.provinces):
#         province.id = count

#     provinces = []
#     for province in nd_map.provinces:
#         province_dict: dict = {}

#         province_dict["id"] = province.id
#         province_dict["name"] = province.name
#         province_dict["abbreviation"] = province.abbreviation
#         province_dict["type"] = province.type

#         adjacencies = []
#         for p in province.adjacencies:
#             if isinstance(p, Province):
#                 adjacencies.append(p.id)
#         province_dict["adjacencies"] = adjacencies

#         if province.home_territory is not None:
#             province_dict["home_territory"] = province.home_territory.id
#         else:
#             province_dict["home_territory"] = -1

#         province_dict["is_supply_point"] = province.is_supply_center
#         province_dict["occupied_units"] = [unit.id for unit in province.occupied_units]

#         provinces.append(province_dict)
#     map_dict["provinces"] = provinces
#     map_dict["units"] = units

#     json_save["map"] = map_dict

#     with open(os.path.join(path, nd_map.name + ".json"), "wb") as f:
#         json = orjson.dumps(json_save)
#         f.write(json)