from random import uniform, choice

from constants import *
from node import BinaryRoom, Node
from utils import drawNode

from rendering.types.prop import Prop
from rendering.layer import Layer
from rendering.core import Rendering

from player.core import Player

class Game:
  # 디버깅용
  __debugging__ = False

  # BSP 알고리즘에 사용할 자원
  __minimum_divide_rate = 0.35
  __maximum_divide_rate = 0.65

  __max_depth = 0

  '''
  레이어 안내
  - 레이어 1
  - 레이어 2: 디버그 노드, 길 용
  - 레이어 3: 방
  - 레이어 4
  - 레이어 5: 문, 플레이어
  '''
  __layers:list[Layer] = []

  __activeRoom:BinaryRoom

  rooms:list[BinaryRoom] = []

  def __init__(self, maxDepth:int):
    # 레이어 초기화
    Layer.createNewLayers(self.__layers, 6, WIDTH, HEIGHT)

    # 루트 생성하기
    self.__max_depth = maxDepth
    treeNode = Node(WIDTH, HEIGHT, 0, 0)
    if self.__debugging__:
      drawNode(self.__layers[2], treeNode)

    # 공간 분할하기
    self.divideMap(treeNode, 0)
    self.createRoom(treeNode, 0)
    self.generateRoad(treeNode, 0)
    self.spawnDoors(treeNode, 0)
    self.spawnDoorsFromBywayRooms(treeNode, 0)

  def run(self):
    self.__spawnPlayer()
    self.printMap()

  '''
  BSP 알고리즘을 사용하여 랜덤하게 맵을 생성함.
  1. 공간 생성
  2. 방 생성
  3. 길 생성 (방 연결)
  4. 방 생성
  '''
  # 1. 가장 긴쪽을 계속 나누어 공간을 만듦
  def divideMap(self, tree:Node, n:int):
    if n == self.__max_depth: return # 최하위 노드는 무시
    maxLine = max(tree.width, tree.height)
    split = round(uniform(maxLine * self.__minimum_divide_rate, maxLine * self.__maximum_divide_rate))
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
          self.__layers[1].setPixel(tree.left + split, y, Prop.Wall)
    # height이 더 길다면
    else:
      # 세로 분할하여 생긴 두 노드 구하기
      tempNode1 = Node(tree.width, split, tree.top, tree.left)
      tempNode2 = Node(tree.width, tree.height - split, tree.top + split, tree.left)
      # 선긋기
      if self.__debugging__:
        for x in range(tree.left, tree.left + tree.width):
          self.__layers[1].setPixel(x, tree.top + split, Prop.Wall)
    # 두 노드 상속하기
    tree.otherNode1 = tempNode1
    tree.otherNode2 = tempNode2
    tree.isRowDivided = tree.width >= tree.height
    # 2개의 노드를 더 분할하기
    self.divideMap(tempNode1, n + 1)
    self.divideMap(tempNode2, n + 1)
  # 2. 나뉘어진 공간에 방을 랜덤하게 놓음
  def createRoom(self, tree:Node, n:int, isLeft:bool = None)->BinaryRoom:
    room:BinaryRoom
    # 최하위 깊이일 경우,
    if n == self.__max_depth:
      width = min(tree.width - 2, round(uniform(10, tree.width - 1))) # 최소 너비 10
      height = round(uniform(5, tree.height - 1)) # 최소 높이 5
      top = tree.top + round(uniform(1, tree.height - height - 1))
      left = tree.left + round(uniform(1, tree.width - width - 1))
      room = BinaryRoom(width, height, left, top)
      self.rooms.append(room)
    else:
      # 최하위 깊이가 아닐 때, 반환할 방 방향 정하기
      isLeft1 = False
      isLeft2 = True
      if tree.isRowDivided:
        if tree.otherNode1.width >= tree.otherNode2.width:
          isLeft1 = True
          isLeft2 = False
        else:
          isLeft1 = False
          isLeft2 = True
      else:
        if tree.otherNode1.height >= tree.otherNode2.height:
          isLeft1 = True
          isLeft2 = False
        else:
          isLeft1 = False
          isLeft2 = True
      tree.otherNode1.room = self.createRoom(tree.otherNode1, n + 1, isLeft1)
      tree.otherNode2.room = self.createRoom(tree.otherNode2, n + 1, isLeft2)
      room = tree.otherNode1.room if isLeft else tree.otherNode2.room
    return room
  # 3. 길 연결하기
  def generateRoad(self, tree:Node, n:int):
    if n == self.__max_depth: return # 최하위 노드는 무시
    # 두 방의 중앙 구하기
    x1, y1 = tree.otherNode1.room.calculateCenter()
    x2, y2 = tree.otherNode2.room.calculateCenter()
    # x 축을 먼저 연결 후, y 축 연결
    for x in range(min(x1, x2), max(x1, x2) + 1):
      self.__layers[1].setPixel(x, y1, Prop.Road)
    for y in range(min(y1, y2), max(y1, y2) + 1):
      self.__layers[1].setPixel(x2, y, Prop.Road)

    drawNode(self.__layers[2], tree.otherNode1.room, Prop.Room)
    drawNode(self.__layers[2], tree.otherNode2.room, Prop.Room)

    self.generateRoad(tree.otherNode1, n + 1)
    self.generateRoad(tree.otherNode2, n + 1)
  # 4. 길과 방이 맞닿은 위치에 방 놓음
  def spawnDoors(self, tree:Node, n:int):
    if n == self.__max_depth: return # 최하위 노드는 무시
    room1 = tree.otherNode1.room
    room2 = tree.otherNode2.room
    x1, y1 = room1.calculateCenter()
    x2, y2 = room2.calculateCenter()
    # 가로 분할
    if tree.isRowDivided:
      # 방1의 중앙 혹은 방2의 중앙이 방2 혹은 방1 안에 있는지
      if -room2.height / 2 <= abs(y1 - y2) <= room2.height / 2:
        self.__layers[4].setPixel(room1.right, y1, Prop.Door)
        self.__layers[4].setPixel(room2.left, y1, Prop.Door)
      else:
        if y1 > y2:
          self.__layers[4].setPixel(room1.right, y1, Prop.Door)
          self.__layers[4].setPixel(x2, room2.bottom, Prop.Door)
        else:
          self.__layers[4].setPixel(room1.right, y1, Prop.Door)
          self.__layers[4].setPixel(x2, room2.top, Prop.Door)
    # 세로 분할
    if not tree.isRowDivided:
      # 방1의 중앙 혹은 방2의 중앙이 방2 혹은 방1 안에 있는지
      if -room1.width / 2 <= abs(x1 - x2) <= room1.width / 2:
        self.__layers[4].setPixel(x2, room1.bottom, Prop.Door)
        self.__layers[4].setPixel(x2, room2.top, Prop.Door)
      else:
        if x1 > x2:
          self.__layers[4].setPixel(room1.left, y1, Prop.Door)
          self.__layers[4].setPixel(x2, room2.top, Prop.Door)
        else:
          self.__layers[4].setPixel(room1.right, y1, Prop.Door)
          self.__layers[4].setPixel(x2, room2.top, Prop.Door)

    self.spawnDoors(tree.otherNode1, n + 1)
    self.spawnDoors(tree.otherNode2, n + 1)
  def spawnDoorsFromBywayRooms(self, tree:Node, n:int):
    if n == self.__max_depth: return # 최하위 노드는 무시
    # 두 방의 중앙 구하기
    x1, y1 = tree.otherNode1.room.calculateCenter()
    x2, y2 = tree.otherNode2.room.calculateCenter()
    for x in range(min(x1, x2), max(x1, x2) + 1):
      rs = self.checkOverlappingRooms(x, y1)
      if tree.otherNode1.room in rs: rs.remove(tree.otherNode1.room)
      if tree.otherNode2.room in rs: rs.remove(tree.otherNode2.room)
      for r in rs:
        self.__layers[4].setPixel(r.left, y1, Prop.Door)
        self.__layers[4].setPixel(r.right, y1, Prop.Door)
    for y in range(min(y1, y2), max(y1, y2) + 1):
      rs = self.checkOverlappingRooms(x2, y)
      if tree.otherNode1.room in rs: rs.remove(tree.otherNode1.room)
      if tree.otherNode2.room in rs: rs.remove(tree.otherNode2.room)
      for r in rs:
        self.__layers[4].setPixel(x2, r.top, Prop.Door)
        self.__layers[4].setPixel(x2, r.bottom, Prop.Door)
    self.spawnDoorsFromBywayRooms(tree.otherNode1, n + 1)
    self.spawnDoorsFromBywayRooms(tree.otherNode2, n + 1)

  def __spawnPlayer(self):
    self.__activeRoom = choice(self.rooms)
    left, top = self.__activeRoom.calculateCenter()
    self.__layers[4].setPixel(left, top, Prop.Player)

    drawNode(self.__layers[2], self.__activeRoom, Prop.Room, Prop.ActiveWall)

    player = Player((left, top), self.__layers[4])
    player.run()

  # 게임 맵 초기화
  def printMap(self):
    render = Rendering()
    render.print(render.addLayers(WIDTH, HEIGHT, self.__layers))

  def checkOverlappingRooms(self, x:int, y:int)->list[BinaryRoom]:
    return list(filter(lambda i:i.top <= y <= i.bottom and i.left <= x <= i.right, self.rooms))
