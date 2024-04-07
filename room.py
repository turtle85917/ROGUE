from __future__ import annotations
from random import randint
import math

WIDTH = 100
HEIGHT = 40

class Room:
  __min_width = 10
  __max_width = 15
  __min_height = 3
  __max_height = 8
  rooms:list[BinaryRoom] = []

  def __init__(self, maxRoom:int):
    for i in range(maxRoom):
      while True:
        width = randint(self.__min_width, self.__max_width)
        height = randint(self.__min_height, self.__max_height)
        left = randint(math.ceil(width / 2), WIDTH - width)
        top = randint(math.ceil(height / 2), HEIGHT - height)
        room = BinaryRoom(width, height, left, top)
        if room.inRoom(self.rooms): continue
        else:
          self.rooms.append(room)
          print(width, height)
          break

  def drawRooms(self, game_map:list[list[str]]):
    for room in self.rooms:
      room.draw(game_map)

class BinaryRoom:
  trim = -5

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
      if self.top - self.trim < room.bottom + room.trim and self.bottom + self.trim > room.top - room.trim and\
        self.left + self.trim < room.right - room.trim and self.right - self.trim > room.left + room.trim:
        return True
    return False
