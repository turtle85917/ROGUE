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
