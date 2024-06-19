from typing import Literal, Union, Callable

from pynput.keyboard import Key
from position import Position

from scene.MiniMap.node import BinaryRoom
from scene.MiniMap.utils import *

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

  stats:Stats

  isInRoom:bool

  __movementKeys:dict[str, list[Key]] = {
    "up": ['w', Key.up],
    "down": ['s', Key.down],
    "left": ['a', Key.left],
    "right": ['d', Key.right]
  }
  __pressedMovements:list[Union[None, Literal["up", "down", "left", "right"]]]

  def __init__(self, room:BinaryRoom):
    left, top = room.calculateCenter()
    self.lastDirection = None
    self.position = Position(left, top)
    self.__pressedMovements = []

    self.stats = Stats()

  def checkMovement(self, key):
    movement = self.__getMovement(key)
    if movement != None and movement not in self.__pressedMovements:
      self.__pressedMovements.append(movement)
  def movePlayer(self, key, callback:Callable[[], None]|None):
    movement = self.__getMovement(key)
    if movement != None and movement in self.__pressedMovements:
      self.__pressedMovements.remove(movement)
      # 움직이기
      self.position += self.directions[movement]
      self.lastDirection = movement
      # 콜백 함수
      if callback != None:
        callback()

  def __getMovement(self, key)->str|None:
    for k, v in self.__movementKeys.items():
      if key in v:
        return k
    return None
