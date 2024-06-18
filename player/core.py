from typing import Literal

from scene.MiniMap.node import BinaryRoom
from position import Position
from scene.MiniMap.utils import *

from rendering.layer import Layer
from rendering.main import Render

from player.stats import Stats

class Player:
  position:Position
  lastDirection:Literal["up", "down", "left", "right"] | None
  directions:dict[str, Position] = {
    "up": Position(0, -1),
    "down": Position(0, 1),
    "left": Position(-1, 0),
    "right": Position(1, 0)
  }

  inRoom:BinaryRoom
  stats:Stats

  isInRoom:bool

  def __init__(self, room:BinaryRoom):
    left, top = room.calculateCenter()
    self.lastDirection = None
    self.position = Position(left, top)

    self.stats = Stats()

  def spawnRoom(self):
    clearConsole()

    layer = Layer(50, 50)

    self.inRoom.width *= 5
    self.inRoom.height *= 5

    drawNode(layer, self.inRoom)
    print(layer.shape)

  def movePlayer(self, movement:Literal["up", "down", "left", "right"]):
    self.position += self.directions[movement]
    self.lastDirection = movement
