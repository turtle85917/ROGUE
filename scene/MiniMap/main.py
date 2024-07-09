from random import uniform, choice

from scene.schema import Scene
from scene.manager import SceneManager

from scene.constants import WIDTH, HEIGHT
from scene.MiniMap.constants import MAX_DEPTH

from scene.MiniMap.node import BinaryRoom, Node
from scene.MiniMap.types.order import LayerOrder
from scene.MiniMap.utils import drawNode

from rendering.types.prop import Prop
from rendering.types.cell import Cell
from rendering.layer import Layer
from rendering.utils import prop2cell

class MiniMap(Scene):
  # 디버깅용
  __debugging__ = False

  # BSP 알고리즘에 사용할 자원
  __minimum_divide_rate = 0.39
  __maximum_divide_rate = 0.61

  __max_depth = 0

  __activeRoom:BinaryRoom
  __latestRoom:BinaryRoom

  __rooms:list[BinaryRoom] = []

  manager:SceneManager

  def __init__(self):
    super().__init__()

    self.sceneName = "MiniMap"

  def render(self):
    # 루트 생성하기
    self.__max_depth = MAX_DEPTH
    treeNode = Node(WIDTH, HEIGHT - 1, 0, 0)
    if self.__debugging__:
      drawNode(self.manager.layers[LayerOrder.Roads], treeNode)

    # 공간 분할하기
    self.__divideMap(treeNode, 0)
    self.__createRoom(treeNode, 0)
    self.__generateRoad(treeNode, 0)
    self.__spawnDoors(treeNode, 0)
    self.__spawnDoorsFromBywayRooms(treeNode, 0)

    self.__spawnPlayer()
    self.__printMap()
  def update(self):
    if self.manager.pressedKey == "enter" and self.__activeRoom != None:
      self.manager.setGlobalVariable("inRoom", self.__activeRoom)
      self.manager.setGlobalVariable("rooms", self.__rooms)
      self.manager.player.stats.energy -= 4
      self.manager.player.isDisarmed = True
      self.manager.changeScene(1)
    # 움직이기 코드
    self.manager.player.movePlayer(self.manager.pressedKey, lambda: self.__printMap())

  '''
  BSP 알고리즘을 사용하여 랜덤하게 맵을 생성함.
  1. 공간 생성
  2. 방 생성
  3. 길 생성 (방 연결)
  4. 방 생성
  '''
  # 1. 가장 긴쪽을 계속 나누어 공간을 만듦
  def __divideMap(self, tree:Node, n:int):
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
          self.manager.layers[LayerOrder.Roads].setPixel(tree.left + split, y, prop2cell(Prop.Wall))
    # height이 더 길다면
    else:
      # 세로 분할하여 생긴 두 노드 구하기
      tempNode1 = Node(tree.width, split, tree.top, tree.left)
      tempNode2 = Node(tree.width, tree.height - split, tree.top + split, tree.left)
      # 선긋기
      if self.__debugging__:
        for x in range(tree.left, tree.left + tree.width):
          self.manager.layers[LayerOrder.Roads].setPixel(x, tree.top + split, prop2cell(Prop.Wall))
    ################
    tempNode1.parentNode = tree
    tempNode2.parentNode = tree
    # 두 노드 상속하기
    tree.otherNode1 = tempNode1
    tree.otherNode2 = tempNode2
    tree.isRowDivided = tree.width >= tree.height
    # 2개의 노드를 더 분할하기
    self.__divideMap(tempNode1, n + 1)
    self.__divideMap(tempNode2, n + 1)
  # 2. 나뉘어진 공간에 방을 랜덤하게 놓음
  def __createRoom(self, tree:Node, n:int)->BinaryRoom:
    room:BinaryRoom
    # 최하위 깊이일 경우,
    if n == self.__max_depth:
      width = min(tree.width - 2, round(uniform(10, tree.width / 2 - 1))) # 최소 너비 10
      height = round(uniform(5, tree.height / 2 - 1)) # 최소 높이 5
      top = tree.top + round(uniform(1, tree.height - height - 1))
      left = tree.left + round(uniform(1, tree.width - width - 1))
      room = BinaryRoom(width, height, left, top)
      room.node = tree
      self.__rooms.append(room)
    else:
      # 최하위 깊이가 아닐 때, 반환할 방 방향 정하기
      tree.otherNode1.room = self.__createRoom(tree.otherNode1, n + 1)
      tree.otherNode2.room = self.__createRoom(tree.otherNode2, n + 1)
      room = tree.otherNode2.room
    return room
  # 3. 길 연결하기
  def __generateRoad(self, tree:Node, n:int):
    if n == self.__max_depth: return # 최하위 노드는 무시
    # 두 방의 중앙 구하기
    x1, y1 = tree.otherNode1.room.calculateCenter()
    x2, y2 = tree.otherNode2.room.calculateCenter()
    endX = max(x1, x2)
    endY = max(y1, y2)
    if endX == tree.otherNode2.room.right or endX == tree.otherNode2.room.left:
      endX -= 1
    if endY == tree.otherNode2.room.top or endY == tree.otherNode2.room.bottom:
      endY -= 1
    # x 축을 먼저 연결 후, y 축 연결
    for x in range(min(x1, x2), endX + 1):
      self.manager.layers[LayerOrder.Roads].setPixel(x, y1, Cell(prop=Prop.Road, color=240))
    for y in range(min(y1, y2), max(y1, y2) + 1):
      self.manager.layers[LayerOrder.Roads].setPixel(x2, y, Cell(prop=Prop.Road, color=240))

    drawNode(self.manager.layers[LayerOrder.Rooms], tree.otherNode1.room, prop2cell(Prop.Room))
    drawNode(self.manager.layers[LayerOrder.Rooms], tree.otherNode2.room, prop2cell(Prop.Room))

    self.__generateRoad(tree.otherNode1, n + 1)
    self.__generateRoad(tree.otherNode2, n + 1)
  # 4. 길과 방이 맞닿은 위치에 방 놓음
  def __spawnDoors(self, tree:Node, n:int):
    if n == self.__max_depth: return # 최하위 노드는 무시
    room1 = tree.otherNode1.room
    room2 = tree.otherNode2.room
    x1, y1 = room1.calculateCenter()
    x2, y2 = room2.calculateCenter()
    # 가로 분할
    if tree.isRowDivided:
      # 방1의 중앙 혹은 방2의 중앙이 방2 혹은 방1 안에 있는지
      if -room2.height / 2 <= abs(y1 - y2) <= room2.height / 2:
        self.manager.layers[LayerOrder.Doors].setPixel(room1.right, y1, prop2cell(Prop.Door))
        self.manager.layers[LayerOrder.Doors].setPixel(room2.left, y1, prop2cell(Prop.Door))
      else:
        if y1 > y2:
          self.manager.layers[LayerOrder.Doors].setPixel(room1.right, y1, prop2cell(Prop.Door))
          self.manager.layers[LayerOrder.Doors].setPixel(x2, room2.bottom, prop2cell(Prop.Door))
        else:
          self.manager.layers[LayerOrder.Doors].setPixel(room1.right, y1, prop2cell(Prop.Door))
          self.manager.layers[LayerOrder.Doors].setPixel(x2, room2.top, prop2cell(Prop.Door))
    # 세로 분할
    if not tree.isRowDivided:
      # 방1의 중앙 혹은 방2의 중앙이 방2 혹은 방1 안에 있는지
      if -room1.width / 2 <= abs(x1 - x2) <= room1.width / 2:
        self.manager.layers[LayerOrder.Doors].setPixel(x2, room1.bottom, prop2cell(Prop.Door))
        self.manager.layers[LayerOrder.Doors].setPixel(x2, room2.top, prop2cell(Prop.Door))
      else:
        if x1 > x2:
          self.manager.layers[LayerOrder.Doors].setPixel(room1.left, y1, prop2cell(Prop.Door))
          self.manager.layers[LayerOrder.Doors].setPixel(x2, room2.top, prop2cell(Prop.Door))
        else:
          self.manager.layers[LayerOrder.Doors].setPixel(room1.right, y1, prop2cell(Prop.Door))
          self.manager.layers[LayerOrder.Doors].setPixel(x2, room2.top, prop2cell(Prop.Door))

    self.__spawnDoors(tree.otherNode1, n + 1)
    self.__spawnDoors(tree.otherNode2, n + 1)
  def __spawnDoorsFromBywayRooms(self, tree:Node, n:int):
    if n == self.__max_depth: return # 최하위 노드는 무시
    # 두 방의 중앙 구하기
    x1, y1 = tree.otherNode1.room.calculateCenter()
    x2, y2 = tree.otherNode2.room.calculateCenter()
    goalNode1 = tree.otherNode2 if x2 > x1 else tree.otherNode1
    goalNode2 = tree.otherNode2 if y2 > y1 else tree.otherNode1
    for x in range(min(x1, x2), max(x1, x2) + 1):
      rs = self.__checkOverlappingRooms(x, y1)
      if tree.otherNode1.room in rs: rs.remove(tree.otherNode1.room)
      if tree.otherNode2.room in rs: rs.remove(tree.otherNode2.room)
      for r in rs:
        if r.node.parentNode == goalNode1.parentNode: continue
        self.manager.layers[LayerOrder.Doors].setPixel(r.left, y1, prop2cell(Prop.Door))
        self.manager.layers[LayerOrder.Doors].setPixel(r.right, y1, prop2cell(Prop.Door))
    for y in range(min(y1, y2), max(y1, y2) + 1):
      rs = self.__checkOverlappingRooms(x2, y)
      if tree.otherNode1.room in rs: rs.remove(tree.otherNode1.room)
      if tree.otherNode2.room in rs: rs.remove(tree.otherNode2.room)
      for r in rs:
        if r.node.parentNode == goalNode2.parentNode: continue
        self.manager.layers[LayerOrder.Doors].setPixel(x2, r.top, prop2cell(Prop.Door))
        self.manager.layers[LayerOrder.Doors].setPixel(x2, r.bottom, prop2cell(Prop.Door))
    self.__spawnDoorsFromBywayRooms(tree.otherNode1, n + 1)
    self.__spawnDoorsFromBywayRooms(tree.otherNode2, n + 1)

  # 플레이어 관련
  def __spawnPlayer(self):
    self.__activeRoom = self.__latestRoom = choice(self.__rooms)
    self.manager.player.enterRoom(self.__activeRoom)
  def __drawPlayer(self):
    if self.__activeRoom != None:
      drawNode(self.manager.layers[LayerOrder.Rooms], self.__activeRoom, prop2cell(Prop.Room), Cell(prop=Prop.Wall, color=13))
    elif self.__latestRoom != None:
      drawNode(self.manager.layers[LayerOrder.Rooms], self.__latestRoom, prop2cell(Prop.Room), prop2cell(Prop.Wall))
    # 플레이어 표기
    self.manager.layers[LayerOrder.Player].clear()
    self.manager.layers[LayerOrder.Player].setPixelByPosition(self.manager.player.position, Layer.PLAYER)
  def __movePlayer(self):
    def getRoomInPlayer()->BinaryRoom|None:
      filterdRooms = list(filter(lambda x:x.top < self.manager.player.position.y < x.bottom and x.left < self.manager.player.position.x < x.right, self.__rooms))
      if(len(filterdRooms) == 0):
        return None
      return list(filterdRooms)[0]
    if self.manager.player.lastMovement == None:
      return
    direction = self.manager.player.directions[self.manager.player.lastMovement]
    # 방 안에 있는 상황이며, 방 외곽에 있을 경우, 안으로 들어오게 함
    if self.manager.player.isInRoom and self.__activeRoom != None and (self.__activeRoom.top + 1 > self.manager.player.position.y or self.manager.player.position.y > self.__activeRoom.bottom - 1 or self.__activeRoom.left + 1 > self.manager.player.position.x or self.manager.player.position.x > self.__activeRoom.right - 1):
      self.manager.player.position -= direction
    # 들어온 방 확인하기
    room = getRoomInPlayer()
    if self.__activeRoom != None:
      self.__latestRoom = self.__activeRoom
    self.__activeRoom = room
    # 문 있는지 체크하기
    forward = self.manager.player.position + direction

    forwardPixel = self.manager.layers[LayerOrder.Doors].getPixelByPosition(forward).prop
    pixel = self.manager.layers[LayerOrder.Doors].getPixelByPosition(self.manager.player.position).prop
    pixel2 = self.manager.layers[LayerOrder.Roads].getPixelByPosition(self.manager.player.position).prop
    pixel3 = self.manager.layers[LayerOrder.Rooms].getPixelByPosition(self.manager.player.position).prop

    # 앞에 있는 픽셀 혹은 위에 있는 픽셀이 문일 경우
    if forwardPixel == Prop.Door or pixel == Prop.Door:
      self.manager.player.isInRoom = False
    # 플레이어가 길 위에 없을 경우
    elif not self.manager.player.isInRoom and pixel2 != Prop.Road and pixel3 != Prop.Room:
      self.manager.player.position -= direction
    # 방 안에 있는 상황이 아니며, 플레이어가 문 위에 있지 않으면 방 안에 있음을 확정
    elif not self.manager.player.isInRoom and self.__activeRoom != None and pixel != Prop.Door:
      self.manager.player.isInRoom = True
  def __updatePlayerUI(self):
    self.manager.layers[LayerOrder.UI].clear()
    if self.__activeRoom != None:
      self.manager.layers[LayerOrder.UI].writeText([("To enter the room press 'Enter'", 0)], (0, 40))
    self.manager.layers[LayerOrder.UI].writeText([(f"Lv. {self.manager.player.stats.level: <10} Curse {self.manager.player.stats.curse: <10} $ {self.manager.player.stats.money: <5} Hp. {self.manager.player.stats.health: <5} Pw. {self.manager.player.stats.power: <5} Def. {self.manager.player.stats.defense: <5} Energy {self.manager.player.stats.energy: <5} Xp {self.manager.player.stats.exp} / {self.manager.player.stats.nextExp}", 0)], (0, 41))

  # 게임 맵 초기화
  def __printMap(self):
    self.__movePlayer()
    self.__drawPlayer()
    self.__updatePlayerUI()

  def __checkOverlappingRooms(self, x:int, y:int)->list[BinaryRoom]:
    return list(filter(lambda i:i.top <= y <= i.bottom and i.left <= x <= i.right, self.__rooms))
