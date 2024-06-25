from typing import Literal, Callable

from pynput.keyboard import Key
from object.position import Position

from scene.MiniMap.node import BinaryRoom
from scene.MiniMap.utils import *

from object.player.stats import Stats

class Player:
  position:Position
  lastDirection:Literal["up", "down", "left", "right"] | None
  directions:dict[str, Position] = {
    "up": Position(0, -1),
    "down": Position(0, 1),
    "left": Position(-1, 0),
    "right": Position(1, 0)
  }

  stats:Stats
  isInRoom:bool

  __movementKeys:dict[str, list[Key]] = {
    "up": ['w', Key.up],
    "down": ['s', Key.down],
    "left": ['a', Key.left],
    "right": ['d', Key.right]
  }

  def __init__(self):
    self.lastDirection = None
    self.stats = Stats()
    self.position = Position(0, 0)

  def enterRoom(self, room:BinaryRoom):
    left, top = room.calculateCenter()
    self.position = Position(left, top)
    self.isInRoom = True

  def movePlayer(self, key, callback:Callable[[], None]|None, room:BinaryRoom|None = None):
    movement = self.__getMovement(key)
    if movement in self.__movementKeys:
      # 움직이기
      self.position += self.directions[movement]
      if room != None and self.isInRoom and (room.top + 1 > self.position.y or self.position.y > room.bottom - 1 or room.left + 1 > self.position.x or self.position.x > room.right - 1):
        self.position -= self.directions[movement]
      self.lastDirection = movement
      # 콜백 함수
      if callback != None:
        callback()

  def __getMovement(self, key)->str|None:
    for k, v in self.__movementKeys.items():
      if key in v:
        return k
    return None
