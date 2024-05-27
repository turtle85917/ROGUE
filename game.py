from random import uniform, choice

from constants import *
from node import BinaryRoom, Node
from utils import drawNode

class Game:
  # 디버깅용
  __debugging__ = True

  # BSP 알고리즘에 사용할 자원
  __minimum_divide_rate = 0.35
  __maximum_divide_rate = 0.65

  __max_depth = 0
  __banned_rooms:list[BinaryRoom] = []

  game_map:list[list[str]] = []
  rooms:list[BinaryRoom] = []

  def __init__(self, maxDepth:int):
    # 맵 초기화
    self.__initMap()

    # 루트 생성하기
    self.__max_depth = maxDepth
    treeNode = Node(WIDTH, HEIGHT, 0, 0)
    if self.__debugging__:
      drawNode(self.game_map, treeNode)

    # 공간 분할하기
    self.divideMap(treeNode, 0)
    self.createRoom(treeNode, 0)
    self.generateRoad(treeNode, 0)
    self.spawnDoors(treeNode, 0)

  def run(self):
    self._spawnPlayer()
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
      if n < self.__max_depth - 1:
        if tree.otherNode1.isRowDivided and not tree.otherNode2.isRowDivided:
          isLeft1 = False
          isLeft2 = True
        elif not tree.otherNode1.isRowDivided and tree.otherNode2.isRowDivided:
          isLeft1 = True
          isLeft2 = False
        else: #if not tree.otherNode1.isRowDivided and not tree.otherNode2.isRowDivided:
          isLeft1 = False
          isLeft2 = False
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

    for x in range(min(x1, x2), max(x1, x2) + 1):
      rs = list(filter(lambda i: i.left <= x <= i.right and i.top <= y1 <= i.bottom, self.rooms))
      if tree.otherNode1.room in rs: rs.remove(tree.otherNode1.room)
      if tree.otherNode2.room in rs: rs.remove(tree.otherNode2.room)
      if len(rs) > 0:
        self.__banned_rooms.append([tree.otherNode1, tree.otherNode2])
        break

    if [tree.otherNode1, tree.otherNode2] not in self.__banned_rooms:
      # x 축을 먼저 연결 후, y 축 연결
      for x in range(min(x1, x2), max(x1, x2) + 1):
        self.game_map[y1][x] = Props.ROAD
      for y in range(min(y1, y2), max(y1, y2) + 1):
        self.game_map[y][x2] = Props.ROAD

    drawNode(self.game_map, tree.otherNode1.room, Props.ROOM)
    drawNode(self.game_map, tree.otherNode2.room, Props.ROOM)

    self.generateRoad(tree.otherNode1, n + 1)
    self.generateRoad(tree.otherNode2, n + 1)
  # 4. 길과 방이 맞닿은 위치에 방 놓음
  def spawnDoors(self, tree:Node, n:int):
    if n == self.__max_depth: return # 최하위 노드는 무시
    room1 = tree.otherNode1.room
    room2 = tree.otherNode2.room
    if [tree.otherNode1, tree.otherNode2] not in self.__banned_rooms:
      x1, y1 = room1.calculateCenter()
      x2, y2 = room2.calculateCenter()
      # 가로 분할
      if tree.isRowDivided:
        # 방1의 중앙 혹은 방2의 중앙이 방2 혹은 방1 안에 있는지
        if -room2.height / 2 <= abs(y1 - y2) <= room2.height / 2:
          self.game_map[y1][room1.right] = Props.DOOR
          self.game_map[y1][room2.left] = Props.DOOR
        else:
          if y1 > y2:
            self.game_map[y1][room1.right] = Props.DOOR
            self.game_map[room2.bottom][x2] = Props.DOOR
          else:
            self.game_map[y1][room1.right] = Props.DOOR
            self.game_map[room2.top][x2] = Props.DOOR
      # 세로 분할
      if not tree.isRowDivided:
        # 방1의 중앙 혹은 방2의 중앙이 방2 혹은 방1 안에 있는지
        if -room1.width / 2 <= abs(x1 - x2) <= room1.width / 2:
          self.game_map[room1.bottom][x2] = Props.DOOR
          self.game_map[room2.top][x2] = Props.DOOR
        else:
          if x1 > x2:
            self.game_map[y1][room1.left] = Props.DOOR
            self.game_map[room2.top][x2] = Props.DOOR
          else:
            self.game_map[y1][room1.right] = Props.DOOR
            self.game_map[room2.top][x2] = Props.DOOR

    self.spawnDoors(tree.otherNode1, n + 1)
    self.spawnDoors(tree.otherNode2, n + 1)

  def _spawnPlayer(self):
    room = choice(self.rooms)
    left, top = room.calculateCenter()
    self.game_map[top][left] = Props.PLAYER

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
