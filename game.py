from random import uniform

from constants import *
from node import BinaryRoom, Node
from utils import drawNode

class Room:
  # 디버깅용
  __debugging__ = False

  # BSP 알고리즘에 사용할 자원
  __minimum_divide_rate__ = 0.35
  __maximum_divide_rate__ = 0.65

  __max_depth__ = 0

  game_map:list[list[str]] = []
  rooms:list[BinaryRoom] = []

  def __init__(self, maxDepth:int):
    # 맵 초기화
    self.__initMap()

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
    if n == self.__max_depth__: return
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
          self.game_map[y][tree.left + split] = Props.WALL
    # height이 더 길다면
    else:
      # 세로 분할하여 생긴 두 노드 구하기
      tempNode1 = Node(tree.width, split, tree.top, tree.left)
      tempNode2 = Node(tree.width, tree.height - split, tree.top + split, tree.left)
      # 선긋기
      if self.__debugging__:
        for x in range(tree.left, tree.left + tree.width):
          self.game_map[tree.top + split][x] = Props.WALL
    # 두 노드 상속하기
    tree.otherNode1 = tempNode1
    tree.otherNode2 = tempNode2
    # 2개의 노드를 더 분할하기
    self.divideMap(tempNode1, n + 1)
    self.divideMap(tempNode2, n + 1)
  # 2. 나뉘어진 공간에 방을 랜덤하게 놓음
  def createRoom(self, tree:Node, n:int)->BinaryRoom:
    room:BinaryRoom
    # 최하위 노드일 경우,
    if n == self.__max_depth__:
      width = round(uniform(10, tree.width - 1)) # 최소 너비 10
      height = round(uniform(5, tree.height - 1)) # 최소 높이 5
      top = tree.top + round(uniform(1, tree.height - height - 1))
      left = tree.left + round(uniform(1, tree.width - width - 1))
      room = BinaryRoom(width, height, left, top)
      self.rooms.append(room)
    else:
      tree.otherNode1.room = self.createRoom(tree.otherNode1, n + 1)
      tree.otherNode2.room = self.createRoom(tree.otherNode2, n + 1)
      room = tree.otherNode1.room
    return room
  # 3. 길 연결하기
  def connectRooms(self, tree:Node, n:int):
    if n == self.__max_depth__: return # 최하위 노드는 무시
    tree.otherNode1.room
    x1, y1 = tree.otherNode1.room.calculateCenter()
    x2, y2 = tree.otherNode2.room.calculateCenter()

    for x in range(min(x1, x2), max(x1, x2) + 1):
      self.game_map[y1][x] = Props.ROAD
    for y in range(min(y1, y2), max(y1, y2) + 1):
      self.game_map[y][x2] = Props.ROAD

    drawNode(self.game_map, tree.otherNode1.room, Props.ROOM)
    drawNode(self.game_map, tree.otherNode2.room, Props.ROOM)

    self.connectRooms(tree.otherNode1, n + 1)
    self.connectRooms(tree.otherNode2, n + 1)

  # 게임 맵 초기화
  def __initMap(self):
    for y in range(HEIGHT):
      self.game_map.append([])
      for _ in range(WIDTH):
        self.game_map[y].append(Props.CELL)
  def printMap(self):
    txt = ''
    for y in range(HEIGHT):
      for x in range(WIDTH):
        txt += self.game_map[y][x]
      txt += '\n'

    print(txt)
