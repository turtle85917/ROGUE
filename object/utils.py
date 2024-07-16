from typing import Callable
from random import randint, choice

from scene.manager import SceneManager
from scene.MiniMap.node import BinaryRoom, Node

from object.position import Position

def getSpawnPos(manager:SceneManager, room:BinaryRoom, choices:list[Position] = [], originPos:Position|None = None, otherCondition:Callable[[Position], bool]|None = None)->Position:
  '''
  소환될 위치를 가져옵니다.

  @param manager 씬 매니저
  @param room 방
  '''
  not_used = []
  resulted = False
  position:Position
  while True:
    if len(choices) > 0 and len(list(filter(lambda x:x not in not_used, choices))) == 0:
      resulted = False
      break
    position = Position(randint(room.left + 1, room.right - 1), randint(room.top + 1, room.bottom - 1)) if len(choices) == 0 else originPos + choice(list(filter(lambda x:x not in not_used, choices)))
    if overflowMovement(room, position):
      not_used.append(position)
      continue
    overlaps = list(filter(lambda x:x.position == position, room.enemies))
    if len(overlaps) == 0 or manager.player.position != position or (otherCondition != None and otherCondition(position)) or (originPos != None and position != originPos):
      resulted = True
      break
    else:
      not_used.append(position)
  if not resulted:
    return originPos
  return position

def limitedMovement(room:BinaryRoom|Node, position:Position)->bool:
  return room.top + 1 > position.y < room.bottom - 1 and room.left + 1 > position.x < room.right - 1

def overflowMovement(room:BinaryRoom|Node, position:Position)->bool:
  return room.top + 1 > position.y or position.y > room.bottom - 1 or room.left + 1 > position.x or position.x > room.right - 1
