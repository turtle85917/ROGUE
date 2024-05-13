from __future__ import annotations
from constants import *
from enum import IntEnum
from random import uniform

class Direction(IntEnum):
  LEFT = 0
  RIGHT = 1
  TOP = 2
  BOTTOM = 3

# BSP 알고리즘을 활용하여 방을 만듦

class Room:
  # 디버깅용
  __debugging__ = False

  # BSP 알고리즘에 사용할 자원
  __minimum_divide_rate__ = 0.4
  __maximum_divide_rate__ = 0.6

  __max_depth__ = 0
  __nodes__:list[Node] = []

  game_map:list[list[str]] = []

  def __init__(self, maxDepth:int):
    # 맵 초기화
    self.__initMap__()

    # 루트 생성하기
    self.__max_depth__ = maxDepth
    treeNode = Node(WIDTH, HEIGHT, 0, 0)
    if self.__debugging__:
      treeNode.draw(self.game_map)

    # 공간 분할하기
    self.divideMap(treeNode, 0)
    self.createRoom(treeNode, 0)
    self.connectRooms(treeNode, 0)

  # 1. 가장 긴쪽을 계속 나누어 공간을 만듦
  def divideMap(self, tree:Node, n:int):
    if n == self.__max_depth__:
      self.__nodes__.append(tree)
      return
    maxLine = max(tree.width, tree.height)
    split = round(uniform(maxLine * self.__minimum_divide_rate__, maxLine * self.__maximum_divide_rate__))
    tempNode1:Node
    tempNode2:Node
    # width가 더 길다면
    if tree.width >= tree.height:
      # 가로 분할하여 생긴 두 노드 구하기
      tempNode1 = Node(split, tree.height, tree.top, tree.left)
      tempNode2 = Node(tree.width - split, tree.height, tree.top, tree.left + split)
      # 선긋기
      if self.__debugging__:
        for y in range(tree.top, tree.top + tree.height):
          self.game_map[y][tree.left + split] = WALL
    # height이 더 길다면
    else:
      # 세로 분할하여 생긴 두 노드 구하기
      tempNode1 = Node(tree.width, split, tree.top, tree.left)
      tempNode2 = Node(tree.width, tree.height - split, tree.top + split, tree.left)
      # 선긋기
      if self.__debugging__:
        for x in range(tree.left, tree.left + tree.width):
          self.game_map[tree.top + split][x] = WALL
    # 두 노드 상속하기
    tree.otherNode1 = tempNode1
    tree.otherNode2 = tempNode2
    # 2개의 노드를 더 분할하기
    self.divideMap(tempNode1, n + 1)
    self.divideMap(tempNode2, n + 1)
  # 2. 나뉘어진 공간에 방을 랜덤하게 놓음
  def createRoom(self, tree:Node, n:int)->BinaryRoom:
    room:BinaryRoom
    if n == self.__max_depth__:
      width = round(uniform(tree.width / 2, tree.width - 1)) # 최소 너비 크기는 width / 2
      height = round(uniform(5, tree.height / 2))
      top = tree.top + round(uniform(1, tree.height - height))
      left = tree.left + round(uniform(1, tree.width - width))
      room = BinaryRoom(width, height, left, top)
    else:
      tree.otherNode1.room = self.createRoom(tree.otherNode1, n + 1)
      tree.otherNode2.room = self.createRoom(tree.otherNode2, n + 1)
      room = tree.otherNode1.room
    return room
  # 3. 길 연결하기
  def connectRooms(self, tree:Node, n:int):
    if n == self.__max_depth__: return # 최하위 노드는 무시
    x1 = tree.otherNode1.room.left + tree.otherNode1.room.width // 2
    x2 = tree.otherNode2.room.left + tree.otherNode2.room.width // 2
    y1 = tree.otherNode1.room.top + tree.otherNode1.room.height // 2
    y2 = tree.otherNode2.room.top + tree.otherNode2.room.height // 2

    for x in range(x1, x2):
      self.game_map[y1][x] = ROAD
    for y in range(y1, y2):
      self.game_map[y][x1] = ROAD

    tree.otherNode1.room.draw(self.game_map)
    tree.otherNode2.room.draw(self.game_map)

    self.connectRooms(tree.otherNode1, n + 1)
    self.connectRooms(tree.otherNode2, n + 1)

  # 게임 맵 초기화
  def __initMap__(self):
    for y in range(HEIGHT):
      self.game_map.append([])
      for _ in range(WIDTH):
        self.game_map[y].append(CELL)
  def printMap(self):
    txt = ''
    for y in range(HEIGHT):
      for x in range(WIDTH):
        txt += self.game_map[y][x]
      txt += '\n'

    print(txt)

class Node:
  otherNode1:Node
  otherNode2:Node
  room:BinaryRoom

  def __init__(self, width:int, height:int, top:int, left:int):
    self.width = width
    self.height = height
    self.top = top
    self.left = left

  def draw(self, game_map:list[list[str]]):
    right = self.width + self.left - 1
    bottom = self.height + self.top - 1
    for y in range(len(game_map)):
      if y >= self.top and bottom >= y:
        for x in range(len(game_map[y])):
          if x >= self.left and right >= x:
            if x == self.left or x == right or y == self.top or y == bottom:
              game_map[y][x] = WALL
            else:
              game_map[y][x] = CELL

class BinaryRoom:
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
