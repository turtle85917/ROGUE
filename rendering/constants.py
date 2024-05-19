from enum import StrEnum

class Props(StrEnum):
  CELL = ' '

  DEFAULT_BLOCK  = '#'
  COLORED_BLOCK  = '\033[35m#\033[0m'
  COLORED_BLOCK2 = '\033[31m#\033[0m'
