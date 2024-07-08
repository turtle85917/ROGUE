from enum import StrEnum

# 맵 오브젝트
class Prop(StrEnum):
  Cell = ' '

  Room       = '.'
  Wall       = '#'
  Road       = '#'
  Door       = '+'
  Object     = ''
  Player     = '@'
