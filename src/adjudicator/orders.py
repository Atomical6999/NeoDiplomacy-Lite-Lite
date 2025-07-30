from re import split as resplit

from core.classes.map import Unit
from core.classes.units import *
from core.classes.map import *
from core.classes.units import Unit

class Order:
    def __init__(self) -> None:
        self.power: Power
        self.unit: OrderedUnit

        self.resolved = False
        self.resolution = False
        self.visited = False
    
    def get_unit_type(self) -> str:
        if isinstance(self.unit, OrderedArmy):
            return "A"
        else:
            return "F"
    
    def __str__(self) -> str:
        return f"{self.get_unit_type()} {self.unit.location.abbreviation if self.unit.location is not None else ""}"

class Hold(Order):
    def __init__(self) -> None:
        super().__init__()

class Move(Order):
    def __init__(self) -> None:
        super().__init__()
        self.destination: Province
        self.path: bool

    def __str__(self) -> str:
        return super().__str__() + f"-{self.destination.abbreviation}"

class Support(Order):
    def __init__(self) -> None:
        super().__init__()
        self.supported_order: Order
    
    def __str__(self) -> str:
        return super().__str__() + " S " +self.supported_order.__str__()

class Convoy(Order):
    def __init__(self) -> None:
        super().__init__()
        self.convoy: Move


class OrderedUnit(Unit):
    def __init__(self, unit: Unit) -> None:
        super().__init__(unit.location)
        self.attack_strength: int = 0 # Strength to attack and conquer province moved to
        self.defend_strength: int = 0 # Strength of unit engaged in a head-to-head to prevent the opposing unit from succeeding
        self.prevent_strength: int = 0 # Strength preventing another ordered unit to succeed moving to the same province

class OrderedArmy(OrderedUnit):
    def __init__(self, unit: Unit) -> None:
        super().__init__(unit)

class OrderedFleet(OrderedUnit):
    def __init__(self, unit: Unit) -> None:
        super().__init__(unit)


def parse_move_order(line: str, nd_map: Map, current_power: Power, unit: OrderedUnit) -> Optional[Move]:
    destination_str = line.split("-")[-1].strip()
    destination = nd_map.search_province_by_name(destination_str)

    order = Move()
    if current_power is not None:
        order.power = current_power
    order.unit = unit
    if destination is not None:
        order.destination = destination
    
    return order

def parse_order_file(nd_map: Map, path: str) -> list[Order]:
    lines: list[str] = []
    with open(path, "r") as file:
        lines = file.readlines()
    
    orders: list[Order] = []

    current_power: Optional[Power] = None
    for line in lines:
        line = line.strip().upper()

        if line == "":
            continue

        order: Optional[Order] = None

        power_str = line.split(":")[0]
        if power_str != line:
            # Line contains colon
            power = nd_map.search_power_by_name(power_str)

            if power is not None:
                current_power = power
            continue
        else:
            unit: Unit

            unit_str = line.split(" ")[0]

            unit_location_str = line.split(" ")[1].split("-")[0]
            # unit_location_str = line.split(unit_str)[1].strip().split(" ")[0].split("-")[0]

            if unit_str == "A" or "ARMY":
                unit = OrderedArmy(Army(nd_map.search_province_by_name(unit_location_str)))
            elif unit_str == "F" or "FLEET":
                unit = OrderedFleet(Fleet(nd_map.search_province_by_name(unit_location_str)))
            else:
                print("Invalid unit type " + unit_str)
                continue

            next = line.split(unit_location_str)[1].strip()
            next_word = next.split(" ")[0].strip()
            if next[0] == "-":
                # Move order
                if current_power is not None:
                    order = parse_move_order(line, nd_map, current_power, unit)

                if order is not None:
                    orders.append(order)
                continue
            elif "SUPPORT" in next_word or next_word == "S":
                # Support

                if next.index("-") > 0:
                    # If -, move support
                    first_prov_str, second_prov_str = next.split("-")
                    
                    first_province = nd_map.search_province_by_name(first_prov_str.strip().split(" ")[-1].strip())
                    second_province = nd_map.search_province_by_name(second_prov_str.strip())

                    order = Support()
                    if current_power is not None:
                        order.power = current_power
                    order.unit = unit

                    supported_order = Move()
                    if first_province is not None:
                        power_search = nd_map.get_unit_power_from_province(first_province)
                        if power_search is not None:
                            supported_order.power = power_search
                        unit_search = nd_map.get_unit_from_province(first_province)
                        if unit_search is not None:
                            if isinstance(unit_search, Army):
                                supported_order.unit = OrderedArmy(unit_search)
                            else:
                                supported_order.unit = OrderedFleet(unit_search)
                    if second_province is not None:
                        supported_order.destination = second_province
                    
                    order.supported_order = supported_order

                    if order is not None:
                        orders.append(order)
                else:
                    # Else, hold support
                    supported_order = Hold()

                    province_str = next.strip().split(" ")[-1]
                    province = nd_map.search_province_by_name(province_str.strip())

                    if province is not None:
                        power_search = nd_map.get_unit_power_from_province(province)
                        if power_search is not None:
                            supported_order.power = power_search 
                    
                        unit_search = nd_map.get_unit_from_province(province)
                        if unit_search is not None:
                            if isinstance(unit_search, Army):
                                supported_order.unit = OrderedArmy(unit_search)
                            else:
                                supported_order.unit = OrderedFleet(unit_search)
            
    return orders

def get_powers_for_test_case(nd_map: Map, path: str) -> list[Power]:
    for power in nd_map.powers:
        power.units = []

    powers: list[Power] = nd_map.powers

    lines = []

    with open(path, "r") as file:
        lines = file.readlines()

    current_power: Optional[Power] = None
    for line in lines:
        line = line.strip().upper()

        if line == "":
            continue

        power_str = line.split(":")[0]
        if power_str != line:
            # Line contains colon
            power = nd_map.search_power_by_name(power_str)

            if power is not None:
                current_power = power
            continue
        else:
            unit: Unit

            unit_str = line.split(" ")[0]

            unit_location_str = line.split(unit_str)[1].strip().split(" ")[0].split("-")[0]

            if unit_str == "A" or "ARMY":
                unit = Army(nd_map.search_province_by_name(unit_location_str))
            elif unit_str == "F" or "FLEET":
                unit = Fleet(nd_map.search_province_by_name(unit_location_str))
            else:
                print("Invalid unit type " + unit_str)
                continue

            
            for power in powers:
                if power == current_power:
                    power.units.append(unit)
                    break

    print(current_power)

    return powers