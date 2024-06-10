from typing import Literal

from node import BinaryRoom
from position import Position

class Player:
  position:Position
  lastDirection:Literal["up", "down", "left", "right"] | None
  directions:dict[str, Position] = {
    "up": Position(0, -1),
    "down": Position(0, 1),
    "left": Position(-1, 0),
    "right": Position(1, 0)
  }

  isInRoom:bool

  def __init__(self, room:BinaryRoom):
    left, top = room.calculateCenter()
    self.lastDirection = None
    self.position = Position(left, top)

  def movePlayer(self, movement:Literal["up", "down", "left", "right"]):
    self.position += self.directions[movement]
    self.lastDirection = movement
