from typing import Literal

from node import BinaryRoom

class Player:
  position:tuple[int, int]

  def __init__(self, room:BinaryRoom):
    left, top = room.calculateCenter()
    self.position = (left, top)

  def movePlayer(self, movement:Literal["up", "down", "left", "right"]):
    match(movement):
      case "up":
        self.position = (self.position[0], self.position[1] - 1)
      case "down":
        self.position = (self.position[0], self.position[1] + 1)
      case "left":
        self.position = (self.position[0] - 1, self.position[1])
      case "right":
        self.position = (self.position[0] + 1, self.position[1])
