from enum import StrEnum

# 맵 생성 조건
WIDTH = 140
HEIGHT = 55

MAX_DEPTH = 4

# 맵 오브젝트
class Props(StrEnum):
  CELL = ' '

  ROOM = '.'
  WALL = '#'
  ROAD = '\033[36m#\033[0m'
  DOOR = '+'

  PLAYER = '@'
