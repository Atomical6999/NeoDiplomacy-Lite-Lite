import os
from loguru import logger
from typing import Sequence
from rich.console import Console
from rich.table import Table

from utils import console as console_utils
from core.classes.map import *
from core.classes.units import *
from core.parser.map_parser import *
from adjudicator.orders import *

PATH = r"D:\Users\Conor\Microsoft Visual Studio Code\Projects\python\NeoDiplomacy Lite Lite\maps"

active_map: Map
console = Console()

def get_maps() -> Sequence[str]:
    return [os.path.join(PATH, p) for p in os.listdir(PATH)]

def load_map_from_file(path: str) -> Map:
    print(f"Loading map {path}...")
    parsed_map = parse_map(path)
    print(f"Successfully loaded map {path}")
    return parsed_map

# def create_power() -> Power | None:
#     power_name = console_utils.Entry("Enter a name for the power, or type 'back' to go back.").create_widget()

#     if power_name.strip().upper() != "BACK":
#         return edit_power(Power(name=power_name))

# def edit_power(power: Power) -> Power:
#     while True:
#         edit_power_selection = console_utils.SelectionMenu(title=f"Editing {power.name}...\n\n{str(power)}", options_display=["Edit Name", "Edit Home Territory", "Edit Supply Centers", "Confirm"]).create_widget()
#         match edit_power_selection:
#             case 0:
#                 power_name = console_utils.Entry("Enter a name for the power, or type 'back' to go back.").create_widget()

#                 if power_name.strip().upper() != "BACK":
#                     power.name = power_name
#             case 1:
#                 pass
#             case 2:
#                 pass
#             case 3:
#                 break

#     return power

def view_powers(nd_map: Map) -> None:
    abbreviations = False
    while True:
        table = Table(title=f"{nd_map.name} Powers")

        columns = ["Name", "Adjective", "Color", "SC's", "Home Territory", "Units"]
        for column in columns:
            table.add_column(column)

        rows = []
        for power in nd_map.powers:
            supply_centers_display = []
            home_territory_display = []
            units_display = []

            if abbreviations:
                supply_centers_display = console_utils.comma_separated_list([supply_center.abbreviation for supply_center in power.supply_centers])
                home_territory_display = console_utils.comma_separated_list([home_territory.abbreviation for home_territory in power.home_territory])
                for unit in power.units:
                    units_display.append(f"{unit.location.abbreviation} ({unit})") if unit.location is not None else None
                units_display = console_utils.comma_separated_list(units_display)
            else:
                supply_centers_display = console_utils.comma_separated_list([supply_center.name for supply_center in power.supply_centers])
                home_territory_display = console_utils.comma_separated_list([home_territory.name for home_territory in power.home_territory])
                for unit in power.units:
                    units_display.append(f"{unit.location.name} ({unit})") if unit.location is not None else None
                units_display = console_utils.comma_separated_list(units_display)

            rows.append([power.name, power.adjective, power.color, supply_centers_display, home_territory_display, units_display])

        for row in rows:
            table.add_row(*row, style="bright_green")

        console.print(table)

        edit_powers_selection = console_utils.SelectionMenu(options_display=["Toggle Abbreviations", "Back"]).create_widget()

        match edit_powers_selection:
            case 0:
                abbreviations = not abbreviations
            case 1:
                break

# def search_for_province(nd_map: Map) -> Optional[Province]:
#     display_provinces(nd_map, True)

#     province_selection = console_utils.Entry(title="Enter the name, abbreviation, or index of a province:").create_widget()

#     result: Optional[Province] = None

#     try:
#         province_selection = int(province_selection)

#         if province_selection < len(nd_map.provinces) and province_selection >= 0:
#             result = nd_map.provinces[province_selection]
#     except ValueError:
#         result = nd_map.search_provinces(str(province_selection))

#     return result

# def create_unit(province: Province, nd_map: Map) -> Optional[Unit]:
#     unit_type = console_utils.SelectionMenu(title="Select a Unit Type for the unit:", options=list(UnitType), options_display=list(UnitType.__members__)).create_widget()

#     match unit_type:
#         case UnitType.ARMY:
#             return edit_unit(Army(), nd_map)
#         case UnitType.FLEET:
#             return edit_unit(Fleet(), nd_map)
#         case UnitType.PLANE:
#             return edit_unit(Plane(), nd_map)

# def edit_unit(unit: Unit, nd_map: Map) -> Optional[Unit]:
#     while True:
#         edit_unit_selection = console_utils.SelectionMenu(options_display=["Edit Type", "Edit Power", "Delete Unit", "Confirm"]).create_widget()

#         match edit_unit_selection:
#             case 0:
#                 unit_type = console_utils.SelectionMenu(title=f"Select a Unit Type for {unit}:", options=list(UnitType), options_display=list(UnitType.__members__)).create_widget() # type: ignore
#                 match unit_type:
#                     case UnitType.ARMY:
#                         unit = Army(power=unit.power) # type: ignore
#                     case UnitType.FLEET:
#                         unit = Fleet(power=unit.power) # type: ignore
#                     case UnitType.PLANE:
#                         unit = Plane(power=unit.power) # type: ignore
#             case 1:
#                 # Power
#                 power_selection = console_utils.SelectionMenu(title=f"Select a Power for {unit} to be owned by:", options=[*nd_map.powers, None], options_display=[*[power.name for power in nd_map.powers], "None"]).create_widget() # type: ignore
#                 if power_selection:
#                     unit.power = power_selection # type: ignore
#             case 2:
#                 # Delete
#                 return None
#             case 3:
#                 break
#     return unit # type: ignore

# def edit_units(province: Province, nd_map: Map) -> None:
#     while True:
#         table = Table(title=f"{province.name} Units")

#         columns = ["Unit Type", "Power"]
#         for column in columns:
#             table.add_column(column)

#         rows = []
#         for unit in province.occupied_units:
#             if unit.power:
#                 rows.append([str(type(unit)), unit.power.name])

#         for row in rows:
#             table.add_row(*row, style="bright_green")

#         console.print(table)

#         edit_units_selection = console_utils.SelectionMenu(options_display=["Add Unit", "Edit or Delete Unit", "Back"]).create_widget()

#         match edit_units_selection:
#             case 0:
#                 new_unit = create_unit(province, nd_map)
#                 if new_unit:
#                     province.occupied_units.append(new_unit)
#             case 1:
#                 units_string = []
#                 for u in province.occupied_units:
#                     text = ""
#                     text += str(type(u))
#                     if u.power:
#                         text += f" ({u.power.name})"
#                     units_string.append(text)

#                 edit_unit_selection = console_utils.SelectionMenu(options=province.occupied_units, options_display=units_string).create_widget()

#                 new_unit = edit_unit(edit_unit_selection, nd_map)
#                 if new_unit is None:
#                     province.occupied_units.remove(edit_unit_selection)
#             case 2:
#                 break

# def create_coast(province: Province, nd_map: Map) -> Optional[Coast]:
#     coast_type = console_utils.SelectionMenu(title="Select a Coast type:", options=list(CoastType)).create_widget()

#     return edit_coast(Coast(coast_type), nd_map)

# def edit_coast(coast: Coast, nd_map: Map) -> Coast:
#     while True:
#         edit_coast_selection = console_utils.SelectionMenu(title=f"Editing {coast.coast_type}...\n\n{str(coast)}", options_display=["Edit Type", "Edit Adjacencies", "Confirm"]).create_widget()

#         match edit_coast_selection:
#             case 0:
#                 coast.coast_type = console_utils.SelectionMenu(title="Select a Coast type:", options=list(CoastType)).create_widget()
#             case 1:
#                 # Adjacencies
#                 print(f"Editing {coast.coast_type} adjacencies...")
#                 province_selection = search_for_province(nd_map)
#                 if province_selection:
#                     if province_selection in coast.adjacencies:
#                         coast.adjacencies.remove(province_selection)
#                         province_selection.adjacencies.remove(coast)
#                     elif province_selection == coast:
#                         print(f"Province {province_selection.name} cannot be adjacent to itself.")
#                         console_utils.enter()
#                     else:
#                         coast.adjacencies.append(province_selection)
#                         province_selection.adjacencies.append(coast)
#             case 2:
#                 break

#     return coast

# def edit_coasts(province: Province, nd_map: Map) -> None:
#     abbreviations: bool = False
#     while True:
#         table = Table(title=f"{province.name} Coasts")

#         columns = ["Coast", "Adjacencies"]
#         for column in columns:
#             table.add_column(column)

#         rows = []
#         for coast in province.coasts:
#             adjacency_names = ""
#             coast.adjacencies.sort(key=lambda p: p.name if isinstance(p, Province) else p.coast_type if isinstance(p, Coast) else "")
#             for count, adjacent_province in enumerate(coast.adjacencies):
#                 append: str = ""
#                 if isinstance(adjacent_province, Province):
#                     append = adjacent_province.abbreviation if abbreviations else adjacent_province.name
#                 elif isinstance(adjacent_province, Coast):
#                     append = adjacent_province.coast_type
#                 if count != len(province.adjacencies) - 1:
#                     adjacency_names += append + ", "
#                 else:
#                     adjacency_names += append

#             rows.append([coast.coast_type, adjacency_names])

#         for row in rows:
#             table.add_row(*row, style="bright_green")

#         console.print(table)

#         edit_units_selection = console_utils.SelectionMenu(options_display=["Add Coast", "Edit or Delete Coast", "Toggle Abbreviations", "Back"]).create_widget()

#         match edit_units_selection:
#             case 0:
#                 new_coast = create_coast(province, nd_map)
#                 if new_coast:
#                     province.coasts.append(new_coast)
#             case 1:
#                 edit_coast_selection = console_utils.SelectionMenu(options=province.coasts, options_display=[coast.coast_type for coast in province.coasts]).create_widget()

#                 new_coast = edit_coast(edit_coast_selection, nd_map)
#                 if new_coast is None:
#                     province.coasts.remove(edit_coast_selection)
#             case 2:
#                 abbreviations = not abbreviations
#             case 3:
#                 break

# def edit_province(province: Province, nd_map: Map) -> Province:
#     while True:
#         edit_province_selection = console_utils.SelectionMenu(title=f"Editing {province.name}...\n\n{str(province)}", options_display=["Edit Name", "Edit Abbreviation", "Edit Type", "Toggle Supply Center", "Edit Home Territory", "Edit Occupied Units", "Edit Adjacencies", "Edit Coasts", "Confirm"]).create_widget()
#         match edit_province_selection:
#             case 0:
#                 province_name = console_utils.Entry("Enter a name for the province, or type 'back' to go back.").create_widget()

#                 if province_name.strip().upper() != "BACK":
#                     province.name = province_name
#             case 1:
#                 province_abbreviation = console_utils.Entry("Enter an abbreviation for the province, or type 'back' to go back.").create_widget()

#                 if province_abbreviation.strip().upper() != "BACK":
#                     province.abbreviation = province_abbreviation
#             case 2:
#                 province.type = console_utils.SelectionMenu(title=f"Select a Province Type for {province.name}:", options=list(ProvinceType), options_display=list(ProvinceType.__members__)).create_widget()
#             case 3:
#                 # Supply Center
#                 province.is_supply_center = not province.is_supply_center
#             case 4:
#                 # Home Territory
#                 home_territory_selection = console_utils.SelectionMenu(title=f"Select a Power for {province.name} to be home territory of:", options=[*nd_map.powers, None], options_display=[*[power.name for power in nd_map.powers], "None"]).create_widget()
#                 if home_territory_selection:
#                     province.home_territory = home_territory_selection
#             case 5:
#                 # Occupied Units
#                 edit_units(province, nd_map)
#             case 6:
#                 # Adjacencies
#                 print(f"Editing {province.name} adjacencies...")
#                 province_selection = search_for_province(nd_map)
#                 if province_selection:
#                     if province_selection in province.adjacencies:
#                         province.adjacencies.remove(province_selection)
#                         province_selection.adjacencies.remove(province)
#                     elif province_selection == province:
#                         print(f"Province {province_selection.name} cannot be adjacent to itself.")
#                         console_utils.enter()
#                     else:
#                         province.adjacencies.append(province_selection)
#                         province_selection.adjacencies.append(province)
#             case 7:
#                 # Coasts
#                 edit_coasts(province, nd_map)
#             case 8:
#                 break

#     return province

# def create_province(nd_map: Map) -> Province | None:
#     while True:
#         province_name = console_utils.Entry(
#             "Enter a name for the province, or type 'back' to go back.",
#             disallowed_entries=[p.name.strip().upper() for p in nd_map.provinces],
#             disallowed_message="A province with that name already exists."
#         ).create_widget()

#         if province_name.strip().upper() != "BACK":
#             province_abbreviation = console_utils.Entry(
#                 "Enter an abbreviation for the province, or type 'back' to go back.",
#                 disallowed_entries=[p.abbreviation.strip().upper() for p in nd_map.provinces],
#                 disallowed_message="A province with that abbreviation already exists."
#             ).create_widget()

#             if province_abbreviation.strip().upper() != "BACK":
#                 return edit_province(Province(name=province_name, abbreviation=province_abbreviation, adjacencies=[], coasts=[]), nd_map)

def display_provinces(nd_map: Map, show_indices: bool = False, abbreviations: bool = False, exclude_list: list[Province] = []) -> None:
    nd_map.provinces.sort(key=lambda p: p.name)
    table = Table(title=f"{nd_map.name} Provinces")

    if show_indices:
        columns = ["Index", "Name", "Abbr", "Aliases", "Type", "Adjacencies"]
    else:
        columns = ["Name", "Abbr", "Aliases", "Type", "Adjacencies"]
    for column in columns:
        table.add_column(column)

    provinces = nd_map.provinces
    rows = []
    for province_count, province in enumerate(provinces):
        adjacency_display = ""
        province.adjacencies.sort(key=lambda p: p.name)
        for count, adjacent_province in enumerate(province.adjacencies):
            if isinstance(adjacent_province, Province):
                append = adjacent_province.abbreviation if abbreviations else adjacent_province.name
                if count != len(province.adjacencies) - 1:
                    adjacency_display += append + ", "
                else:
                    adjacency_display += append

        if show_indices:
            rows.append([str(province_count), province.name, province.abbreviation, console_utils.comma_separated_list(province.aliases), province.type, adjacency_display])
        else:
            rows.append([province.name, province.abbreviation, console_utils.comma_separated_list(province.aliases), province.type, adjacency_display])

    for row in rows:
        table.add_row(*row, style="bright_green")

    console.print(table)

def edit_provinces(nd_map: Map) -> None:
    abbreviations = False
    while True:
        display_provinces(nd_map, abbreviations=abbreviations)

        edit_provinces_selection = console_utils.SelectionMenu(options_display=["Toggle Abbreviations", "Back"]).create_widget()

        match edit_provinces_selection:
            case 0:
                abbreviations = not abbreviations
            case 1:
                break

def view_map(nd_map: Map) -> None:
    while True:
        edit_map_selection = console_utils.SelectionMenu(
            title=f"Editing {nd_map.name}...\n\n{str(nd_map)}",
            options_display=["View Powers", "View Provinces", "Back"]
        ).create_widget()

        match edit_map_selection:
            case 0:
                view_powers(nd_map)
            case 1:
                edit_provinces(nd_map)
                pass
            case 2:
                break

# def create_map() -> None:
#     map_name = console_utils.Entry("Enter a name for the map, or type 'back' to go back.").create_widget()

#     if map_name.strip().upper() == "BACK":
#         return

#     nd_map = Map()
#     nd_map.name = map_name

#     edit_map(nd_map)

def load_map() -> None:
    maps = get_maps()
    map_selection = console_utils.SelectionMenu(title="Select a map:", options=maps, options_display=[m.split("\\")[-1] for m in maps]).create_widget()

    active_map = load_map_from_file(map_selection)
    view_map(active_map)

def map_menu() -> None:
    load_map()

def test_cases_menu() -> None:
    while True:
        print("Loading DATC map and test case files...")
        nd_map = load_map_from_file(os.path.join(PATH, "DATC.json"))


        print("\n\nDiplomacy Adjudicator Test Cases (DATC)" \
        "\nHere you can simulate each test case and see if the result matches the expected.")
        
        test_cases_selection = console_utils.SelectionMenu(options_display=["Back", "All", "test.order"]).create_widget()
        
        match test_cases_selection:
            case 0:
                break
            case 1:
                pass
            case 2:
                get_powers_for_test_case(nd_map, r"D:\Users\Conor\Microsoft Visual Studio Code\Projects\python\NeoDiplomacy Lite Lite\src\adjudicator\test_cases\test.order")
                orders = parse_order_file(nd_map, r"D:\Users\Conor\Microsoft Visual Studio Code\Projects\python\NeoDiplomacy Lite Lite\src\adjudicator\test_cases\test.order")

                for order in orders:
                    print(order)
                input("ENTER TO OCNIN:")

def main_menu() -> None:
    while True:
        menu_selection = console_utils.SelectionMenu(title="NeoDiplomacy Lite^2", options_display=["New Game", "Load Game", "View Maps", "About", "Quit Game"]).create_widget()

        match menu_selection:
            case 0:
                print("It's not done yet.")
            case 1:
                print("It's not done yet.")
            case 2:
                console_utils.clear()
                map_menu()
            case 3:
                while True:
                    print("This is a console-based lightweight version of NeoDiplomacy without any graphical display for creating, editing, and managing custom Diplomacy games and maps." \
                    "\nThe adjudicator is (will be) DATC compliant. This means that it follows the standard conventions and rulesets generally accepted in the Diplomacy community." \
                    "\nTo view and execute DATC test cases to confirm the integrity of this adjudicator, press 0.")
                    about_selection = console_utils.SelectionMenu(options_display=["Diplomacy Adjudicator Test Cases", "Back"]).create_widget()

                    match about_selection:
                        case 0:
                            test_cases_menu()
                        case 1:
                            break
            case 4:
                break

        """
        self.id: int = id
        self.name: str = name
        self.abbreviation: str = abbreviation
        self.type: ProvinceType = type
        self.adjacencies: list[Province] = adjacencies

        self.home_territory: Power = home_territory
        self.is_supply_point: bool = is_supply_point
        self.occupied_units: list[Unit] = occupied_units
        """

        # console.Form(title="Create Province", fields={
        #     "name": str,
        #     "abbreviation": str,
        #     "type": ProvinceType,
        #     "adjacencies": console.FormSelectionMenu("Create"),
        #     "home_territory": console.FormSelectionMenu(),
        #     "is_supply_point": bool,
        #     "occupied_units": int
        # }).create_widget()