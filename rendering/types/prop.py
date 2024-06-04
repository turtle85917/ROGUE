from enum import StrEnum

# 맵 오브젝트
class Prop(StrEnum):
  Cell = ' '

  Room = '.'
  Wall = '#'
  ActiveWall = '\033[31m#\033[0m'
  Road = '\033[36m#\033[0m'
  Door = '+'

  Player = '@'
