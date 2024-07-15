from random import randint

from scene.manager import SceneManager
from scene.MiniMap.node import BinaryRoom, Node

from object.position import Position

def getSpawnPos(manager:SceneManager, room:BinaryRoom)->Position:
  '''
  소환될 위치를 가져옵니다.

  @param manager 씬 매니저
  @param room 방
  '''
  position:Position
  while True:
    position = Position(randint(room.left + 1, room.right - 1), randint(room.top + 1, room.bottom - 1))
    overlaps = list(filter(lambda x:x.position == position, room.enemies))
    if len(overlaps) == 0 or manager.player.position != position:
      break
  return position

def limitedMovement(room:BinaryRoom|Node, position:Position)->bool:
  return room.top + 1 > position.y < room.bottom - 1 and room.left + 1 > position.x < room.right - 1

def overflowMovement(room:BinaryRoom|Node, position:Position)->bool:
  return room.top + 1 > position.y or position.y > room.bottom - 1 or room.left + 1 > position.x or position.x > room.right - 1
