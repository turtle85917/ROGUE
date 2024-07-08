from dataclasses import dataclass

from object.position import Position
from _types.direction import Direction

@dataclass
class Bubble:
  life:int
  direction:Direction
  position:Position
  color:int
