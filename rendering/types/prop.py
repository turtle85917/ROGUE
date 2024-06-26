from enum import StrEnum
from rendering.style import Style, AnsiColor

# 맵 오브젝트
class Prop(StrEnum):
  Cell = ' '

  Room       = '.'
  Wall       = '#'
  ActiveWall = Style('#', AnsiColor.TextRed).out()
  Road       = Style('#', AnsiColor.TextCyan).out()
  Door       = '+'
  Object     = ''
  Player     = '@'
