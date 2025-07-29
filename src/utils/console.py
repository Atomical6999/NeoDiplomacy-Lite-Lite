from typing import Optional, Any, Sequence, MutableSequence
from abc import ABC, abstractmethod
from os import system

from core.classes.units import *
from core.classes.map import *

class Widget(ABC):
    @abstractmethod
    def create_widget(self) -> Any:
        pass

    def __init__(self, title: str) -> None:
        self.title: str = title

class Submit():
    pass

class SelectionMenu(Widget):
    """Creates a single-select menu and returns the selected option, with an optional display text for each option. You can optionally not display."""

    def create_widget(self, display: bool = True) -> Any:
        while True:
            index = 0

            if display:
                print(self.title + "\n")

                for option in self.options:
                    if self.options_display != []:
                        print(f"[{index + 1}] - {self.options_display[index]}")
                    else:
                        print(f"[{index + 1}] - {option}")

                    index += 1

            try:
                inp = int(input("\n -> "))
                if inp < 1 or inp > index:
                    print("That is not an option.\n")
                    enter()
                else:
                    clear()
                    break
            except ValueError:
                print("Invalid input.\n")
                enter()
            except Exception as e:
                print("Invalid input.\n")
                enter()

        print()
        return self.options[inp - 1]

    def __init__(self, title: str = "Select an option:", options: Sequence[Any | Submit] = [], options_display: list[str] = []) -> None:
        super().__init__(title)
        if options == []:
            options = [i for i in range(len(options_display))]
        self.options: Sequence[Any | Submit] = options
        self.options_display: list[str] = options_display

class MultiSelectionMenu(SelectionMenu):
    def create_widget(self, display: bool = True) -> list[Any]:
        print("WWOWOWOOWOW")
        selections: list[Any] = []

        while Submit() not in selections:

            index = 0

            if display:
                print(self.title)

                for option in self.options:
                    if self.options_display != []:
                        print(f"[{index + 1}] - {self.options_display[index]}")
                    else:
                        print(f"[{index + 1}] - {option}")

                    index += 1

            selection = super().create_widget(display=False)

            if selection in selections:
                selections.remove(selection)

        selections.remove(Submit())

        return selections

    def __init__(self, title: str = "Select an option:", options: MutableSequence[str | Submit] = [], options_display: list[str] = []) -> None:
        options.append(Submit())
        options_display.append("SUBMIT")
        super().__init__(title, options, options_display)

class Entry(Widget):
    """A short text input widget"""

    def create_widget(self) -> str:
        while True:
            print(self.title)
            inp = input(" -> ")

            if inp.strip().upper() in self.disallowed_entries:
                print(self.disallowed_message)
                enter()
            else:
                break

        clear()
        return inp

    def __init__(self, title: str, disallowed_entries: list[str] = [], disallowed_message: str = "That entry is not allowed.") -> None:
        super().__init__(title)
        self.disallowed_entries: list[str] = disallowed_entries
        self.disallowed_message: str = disallowed_message

class FormFieldsError(Exception):
    DEFAULT_MESSAGE = "Form values should be a type, not an object, unless it is FormSelectionMenu object"

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message or self.DEFAULT_MESSAGE)

class FormSelectionMenu(SelectionMenu):
    def __init__(self, message: str = "Select an option:", options: list[str] = []) -> None:
        super().__init__(message, options)

class Form(Widget):
    """A form by provided dictionary of key-value pairs where key is field title and value is field type and returns a response"""

    def create_widget(self) -> dict:
        print(self.title)

        for key, value in self.fields.items():
            if isinstance(value, FormSelectionMenu):
                MultiSelectionMenu(title=key, options=list(value.options), options_display=value.options_display)
            elif not isinstance(value, type):
                raise FormFieldsError(f"{value} should be a type, not an object, unless it is FormSelectionMenu object")
            else:
                pass

        return {}

    def __init__(self, title: str, fields: dict[str, type | FormSelectionMenu]) -> None:
        super().__init__(title)
        self.fields: dict[str, type | FormSelectionMenu] = fields

def enter() -> None:
    print("Press ENTER to continue.")
    input()

def clear() -> None:
    """Clears the console"""
    system('cls')

def comma_separated_list(l: list[str], print_and: bool = False) -> str:
    """Returns a list with each value comma-separated"""
    output = ""
    for count, item in enumerate(l):
        if count != len(l) - 1:
            output += item + ", "
        else:
            output += "and " + item if print_and else item
    
    return output