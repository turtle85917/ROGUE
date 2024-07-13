from typing import Callable
from math import e, pow

from object.position import Position

from scene.MiniMap.node import BinaryRoom

from object.player.stats import Stats

class Player:
  position:Position
  lastMovement:str|None
  directions:dict[str, Position] = {
    "up": Position(0, -1),
    "down": Position(0, 1),
    "left": Position(-1, 0),
    "right": Position(1, 0)
  }

  stats:Stats
  isInRoom:bool
  isDisarmed:bool # 방 안으로 들어온 상태인지

  __movementKeys:dict[str, list[str]] = {
    "up": ['w', "up"],
    "down": ['s', "down"],
    "left": ['a', "left"],
    "right": ['d', "right"]
  }
  __mappingKeys:dict[str, list[str]] = {
    "up": ['w'],
    "down": ['s'],
    "left": ['a'],
    "right": ['d'],
    "attack-up": ["up"],
    "attack-down": ["down"],
    "attack-left": ["left"],
    "attack-right": ["right"],
    "pick-up-item": ["e"],
    "exit": ["r", "enter"]
  }
  __movingMovement:list[str] = ["up", "down", "left", "right"]

  def __init__(self):
    self.lastMovement = None
    self.stats = Stats()
    self.position = Position(0, 0)
    self.isDisarmed = False

  def enterRoom(self, room:BinaryRoom):
    left, top = room.calculateCenter()
    self.position = Position(left, top)
    self.isInRoom = True

  def movePlayer(self, key, callback:Callable[[], None]|None = None, room:BinaryRoom|None = None):
    movement = self.getMovement(key)
    if movement in self.__movingMovement:
      # 움직이기
      self.position += self.directions[movement]
      if room != None and self.isInRoom and (room.top + 1 > self.position.y or self.position.y > room.bottom - 1 or room.left + 1 > self.position.x or self.position.x > room.right - 1):
        self.position -= self.directions[movement]
      self.lastMovement = movement
      # 콜백 함수
      if callback != None:
        callback()
  def getMovement(self, key)->str|None:
    keys = self.__mappingKeys if self.isDisarmed else self.__movementKeys
    for k, v in keys.items():
      if key in v:
        return k
    return None

  def levelUp(self)->bool:
    if self.stats.exp - self.__getExp(self.stats.level - 1) >= self.stats.nextExp:
      self.stats.level += 1
      self.stats.nextExp = self.__getExp(self.stats.level + 1)
      return True
    return False
  def __getExp(self, level:int)->int:
    if level == 0:
      return 0
    return round(pow(40 * e, 0.3 * level))
