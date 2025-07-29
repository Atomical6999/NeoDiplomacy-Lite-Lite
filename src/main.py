from loguru import logger

from core.nd_core import main_menu
from core.classes.map import *
from core.classes.units import *

def main():
    logger.add("logs\\{time}.log", format="{time} | {level} | {name} - {message}", rotation="20 MB")
    main_menu()

if __name__ == "__main__":
    main()