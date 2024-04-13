from __future__ import annotations
from constants import *
from random import randint

class Room:
  __min_width__ = 16
  __max_width__ = 24
  __min_height__ = 6
  __max_height__ = 18
  __connectRooms__:dict[BinaryRoom, list[tuple[int, tuple[int,int]]]] = {}
  rooms:list[BinaryRoom] = []

  def __init__(self, maxRoom:int):
    for _ in range(maxRoom):
      count = 0
      while True:
        width = randint(self.__min_width__, self.__max_width__)
        height = randint(self.__min_height__, self.__max_height__)
        left = randint(0, WIDTH - width)
        top = randint(0, HEIGHT - height)
        room = BinaryRoom(width, height, left, top)
        count += 1
        if count > 100: break # 100번 넘게 방 생성 실패 시, 종료
        if room.inRoom(self.rooms): continue
        else:
          self.rooms.append(room)
          break

  def setRooms(self, newRooms:list[BinaryRoom]):
    self.rooms = newRooms

  def drawRooms(self, game_map:list[list[str]]):
    for room in self.rooms:
      room.draw(game_map)
      connectedPos = list(filter(lambda x:x[0] == room, self.__connectRooms__.items()))
      for room, connects in connectedPos:
        for currentRoom, pos in connects:
          if pos[0] == 0:
            right = room.right
            left = currentRoom.left
            game_map[pos[1]][right] = '+'
            game_map[pos[1]][left] = '+'
          if pos[1] == 0:
            bottom = room.bottom
            top = currentRoom.top
            game_map[bottom][pos[0]] = '+'
            game_map[top][pos[0]] = '+'

  def connectRooms(self, game_map:list[list[int]]):
    def update_connect_rooms(key:BinaryRoom, value:tuple[BinaryRoom, tuple[int,int]]):
      if self.__connectRooms__.get(key):
        self.__connectRooms__[key].append(value)
      else:
        self.__connectRooms__[key] = [value]

    for room in self.rooms:
      for i, _ in enumerate(self.rooms):
        target = self.rooms[i]
        if room == target: continue
        x1, y1 = target.calculateCenter()
        x2, y2 = room.calculateCenter()
        if abs(y1 - y2) < min(target.height, room.height):
          startPos = min(x1, x2)
          endPos = max(x1, x2)
          yOffset = abs(y1 - y2) // 2
          y = min(y1, y2) + yOffset
          currentRoom:BinaryRoom = room
          if y1 < y2: currentRoom = target
          update_connect_rooms(room, [currentRoom, (0, y)])
          for x in range(startPos, endPos): game_map[y][x] = '#'
        elif abs(x1 - x2) < min(target.width, room.width):
          startPos = min(y1, y2)
          endPos = max(y1, y2)
          xOffset = abs(x1 - x2) // 2
          x = min(x1, x2) + xOffset
          currentRoom:BinaryRoom = room
          if x1 < x2: currentRoom = target
          update_connect_rooms(room, [currentRoom, (x, 0)])
          for y in range(startPos, endPos): game_map[y][x] = '#'

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
            if x == self.left or x == self.right or y == self.top or y == self.bottom:
              game_map[y][x] = '#'
            else:
              game_map[y][x] = ' '

  def inRoom(self, rooms:list[BinaryRoom])->bool:
    for room in rooms:
      if self.top <= room.bottom - room.trim and self.bottom >= room.top + room.trim and\
        self.left <= room.right - room.trim and self.right >= room.left + room.trim:
        return True
    return False

  def calculateCenter(self)->tuple[int,int]:
    return (self.left + self.right) // 2, (self.top + self.bottom) // 2
