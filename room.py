from __future__ import annotations
from constants import *
from enum import IntEnum
from random import randint
import math

class Direction(IntEnum):
  LEFT = 0
  RIGHT = 1
  TOP = 2
  BOTTOM = 3

class Room:
  __min_width__ = 16
  __max_width__ = 24
  __min_height__ = 6
  __max_height__ = 18
  __connectRooms__:dict[BinaryRoom,list[tuple[int,tuple[bool,int,tuple[int,int]]]]] = {}
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
      # connectedPos = list(filter(lambda x:x[0] == room, self.__connectRooms__.items()))
      # for room, connects in connectedPos:
      #   for currentRoom, (isRow, staticPos, (startPos, endPos)) in connects:
      #     if isRow:
      #       game_map[startPos + 1][staticPos] = DOOR
      #       game_map[endPos - 1][staticPos] = DOOR

  def connectRooms(self, game_map:list[list[int]]):
    def updateConnectRooms(key:BinaryRoom, value:tuple[BinaryRoom, tuple[bool,int,tuple[int,int]]]):
      if self.__connectRooms__.get(key):
        self.__connectRooms__[key].append(value)
      else:
        self.__connectRooms__[key] = [value]

    paths:list[tuple[int, int]] = []

    for room in self.rooms:
      for i, _ in enumerate(self.rooms):
        target = self.rooms[i]
        if room == target: continue
        x1, y1 = target.calculateCenter()
        x2, y2 = room.calculateCenter()
        if abs(y1 - y2) < min(target.height, room.height):
          # 시작 위치, 목표 위치
          startPos = min(x1, x2)
          endPos = max(x1, x2)
          # 중복 path 무시
          if (startPos, endPos) in paths: continue
          # 방이 걸쳐있는 경우, 무시
          filtredRooms = list(filter(lambda x:startPos < x.calculateCenter()[0] < endPos, self.rooms))
          if len(filtredRooms) > 0: continue
          # y 좌표 구하기
          yOffset = abs(y1 - y2) // 2
          y = min(y1, y2) + yOffset
          # 시작 위치, 끝나는 위치 다시 구하기)
          realStartPos = 0
          realEndPos = 0
          if startPos > endPos:
            realStartPos = room.left
            realEndPos = target.right
          else:
            realStartPos = room.right
            realEndPos = target.left
          # 업데이트
          for x in range(startPos, endPos): game_map[y][x] = ROAD
          paths.append((startPos, endPos))
        elif abs(x1 - x2) < min(target.width, room.width):
          # 시작 위치, 목표 위치
          startPos = min(y1, y2)
          endPos = max(y1, y2)
          # 중복 path 무시
          if (startPos, endPos) in paths: continue
          # x 좌표 구하기
          xOffset = abs(x1 - x2) // 2
          x = min(x1, x2) + xOffset
          # 시작 위치, 끝나는 위치 다시 구하기)
          realStartPos = 0
          realEndPos = 0
          if startPos > endPos:
            realStartPos = room.top
            realEndPos = target.bottom
          else:
            realStartPos = room.bottom
            realEndPos = target.top
          # 업데이트
          bywayRooms:list[BinaryRoom] = []
          for y in range(realStartPos, realEndPos):
            game_map[y][x] = ROAD
            for r in self.rooms:
              if room == r or target == r: continue
              if room in bywayRooms: continue
              if abs(r.top - y) < 3:
                bx = r.left if r.left - x > 0 else r.right
                s = min(x, bx)
                e = max(x, bx)
                for x in range(s, e): game_map[y][x] = ROAD
                bywayRooms.append(room)
          paths.append((startPos, endPos))

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
              game_map[y][x] = WALL
            else:
              game_map[y][x] = ROOM

  def inRoom(self, rooms:list[BinaryRoom])->bool:
    for room in rooms:
      if self.top <= room.bottom - room.trim and self.bottom >= room.top + room.trim and\
        self.left <= room.right - room.trim and self.right >= room.left + room.trim:
        return True
    return False

  def calculateCenter(self)->tuple[int,int]:
    return (self.left + self.right) // 2, (self.top + self.bottom) // 2
