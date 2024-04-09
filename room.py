from __future__ import annotations
from random import randint

WIDTH = 100
HEIGHT = 40

class Room:
  __min_width = 9
  __max_width = 12
  __min_height = 3
  __max_height = 6
  rooms:list[BinaryRoom] = []

  def __init__(self, maxRoom:int):
    for _ in range(maxRoom):
      count = 0
      while True:
        width = randint(self.__min_width, self.__max_width)
        height = randint(self.__min_height, self.__max_height)
        left = randint(0, WIDTH - width)
        top = randint(0, HEIGHT - height)
        room = BinaryRoom(width, height, left, top)
        count += 1
        if count > 100: break # 100번 넘게 방 생성 실패 시, 종료
        if room.inRoom(self.rooms): continue
        else:
          self.rooms.append(room)
          break

  def drawRooms(self, game_map:list[list[str]]):
    for room in self.rooms:
      room.draw(game_map)

  def connectRooms(self, game_map:list[list[int]]):
    connectRooms:list[list[int]] = []
    for room in self.rooms:
      costs = list(map(lambda x:(room.left - x.left, room.top - x.top), self.rooms))
      simpleCosts = list(filter(lambda x:x[1][0] == 0 or x[1][1] == 0, enumerate(costs)))
      for i, cost in simpleCosts:
        target = self.rooms[i]
        x1, y1 = target.calculateCenter()
        x2, y2 = room.calculateCenter()
        startPos = (min(x1, x2), min(y1, y2))
        endPos = (max(x1, x2), max(y1, y2))
        if cost[0] == 0:
          for y in range(startPos[1], endPos[1]): game_map[y][x1] = '@'
        elif cost[1] == 0:
          for x in range(startPos[0], endPos[0]): game_map[y1][x] = '@'

class BinaryRoom:
  trim = -6

  def __init__(self, width:int, height:int, left:int, top:int):
    self.width = width
    self.height = height
    self.left = left
    self.top = top
    self.right = self.width + self.left - 1
    self.bottom = self.height + self.top - 1

  def draw(self, game_map:list[list[str]]):
    for y in range(len(game_map)):
      if y >= self.top and self.bottom >= y:
        for x in range(len(game_map[y])):
          if x >= self.left and self.right >= x:
            game_map[y][x] = '#'

  def inRoom(self, rooms:list[BinaryRoom])->bool:
    for room in rooms:
      if self.top <= room.bottom - room.trim and self.bottom >= room.top + room.trim and\
        self.left <= room.right - room.trim and self.right >= room.left + room.trim:
        return True
    return False

  def calculateCenter(self)->tuple[int,int]:
    return (self.left + self.right) // 2, (self.top + self.bottom) // 2
