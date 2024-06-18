from typing import Union, Literal
from random import uniform, choice

from pynput.keyboard import Key, KeyCode, Listener

from scene.manager import SceneManager
from scene.schema import Scene

from scene.MiniMap.constants import *

from scene.MiniMap.node import BinaryRoom, Node
from scene.MiniMap.types.layerOrder import LayerOrder
from scene.MiniMap.utils import clearConsole, setCursorShow, drawNode

from rendering.types.prop import Prop
from rendering.layer import Layer
from rendering.main import Render

from player.core import Player

class MiniMap(Scene):
  # 디버깅용
  __debugging__ = False

  # BSP 알고리즘에 사용할 자원
  __minimum_divide_rate = 0.39
  __maximum_divide_rate = 0.61

  __max_depth = 0

  '''
  레이어 안내
  - 레이어 1: 디버그 노드, 길 용
  - 레이어 2: 방
  - 레이어 3: 문
  - 레이어 4: 플레이어
  - 레이어 5: ???
  - 레이어 6: UI
  '''
  __layers:list[Layer] = []

  __activeRoom:BinaryRoom
  __latestRoom:BinaryRoom

  __running__ = True
  __listener:Listener

  __movementKeys:dict[str, list[Key]] = {
    "up": [KeyCode.from_char('w'), Key.up],
    "down": [KeyCode.from_char('s'), Key.down],
    "left": [KeyCode.from_char('a'), Key.left],
    "right": [KeyCode.from_char('d'), Key.right]
  }
  __pressedMovements:list[Union[None, Literal["up", "down", "left", "right"]]]

  rooms:list[BinaryRoom] = []
  player:Player

  manager:SceneManager

  def __init__(self):
    super().__init__()

    self.sceneName = "MiniMap"

    # 레이어 초기화
    Layer.createNewLayers(self.__layers, 6, WIDTH, HEIGHT)
    self.__layers[LayerOrder.UI] = Layer(WIDTH, UI_HEIGHT)

    # 값 초기화
    self.__pressedMovements = []

    # 루트 생성하기
    self.__max_depth = MAX_DEPTH
    treeNode = Node(WIDTH, HEIGHT, 0, 0)
    if self.__debugging__:
      drawNode(self.__layers[LayerOrder.Road], treeNode)

    # 공간 분할하기
    self.__divideMap(treeNode, 0)
    self.__createRoom(treeNode, 0)
    self.__generateRoad(treeNode, 0)
    self.__spawnDoors(treeNode, 0)
    self.__spawnDoorsFromBywayRooms(treeNode, 0)

  def render(self):
    self.__spawnPlayer()
    self.__printMap()

    try:
      with Listener(
        on_press=self.__onPress,
        on_release=self.__onRelease,
        suppress=True
      ) as listener:
        self.__listener = listener
        self.__listener.join()
    except:
      pass

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
          self.__layers[LayerOrder.Road].setPixel(tree.left + split, y, Prop.Wall)
    # height이 더 길다면
    else:
      # 세로 분할하여 생긴 두 노드 구하기
      tempNode1 = Node(tree.width, split, tree.top, tree.left)
      tempNode2 = Node(tree.width, tree.height - split, tree.top + split, tree.left)
      # 선긋기
      if self.__debugging__:
        for x in range(tree.left, tree.left + tree.width):
          self.__layers[LayerOrder.Road].setPixel(x, tree.top + split, Prop.Wall)
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
  def __createRoom(self, tree:Node, n:int, isLeft:bool = None)->BinaryRoom:
    room:BinaryRoom
    # 최하위 깊이일 경우,
    if n == self.__max_depth:
      width = min(tree.width - 2, round(uniform(10, tree.width / 2 - 1))) # 최소 너비 10
      height = round(uniform(5, tree.height / 2 - 1)) # 최소 높이 5
      top = tree.top + round(uniform(1, tree.height - height - 1))
      left = tree.left + round(uniform(1, tree.width - width - 1))
      room = BinaryRoom(width, height, left, top)
      room.node = tree
      self.rooms.append(room)
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
      self.__layers[LayerOrder.Road].setPixel(x, y1, Prop.Road)
    for y in range(min(y1, y2), max(y1, y2) + 1):
      self.__layers[LayerOrder.Road].setPixel(x2, y, Prop.Road)

    drawNode(self.__layers[LayerOrder.Room], tree.otherNode1.room, Prop.Room)
    drawNode(self.__layers[LayerOrder.Room], tree.otherNode2.room, Prop.Room)

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
        self.__layers[LayerOrder.Door].setPixel(room1.right, y1, Prop.Door)
        self.__layers[LayerOrder.Door].setPixel(room2.left, y1, Prop.Door)
      else:
        if y1 > y2:
          self.__layers[LayerOrder.Door].setPixel(room1.right, y1, Prop.Door)
          self.__layers[LayerOrder.Door].setPixel(x2, room2.bottom, Prop.Door)
        else:
          self.__layers[LayerOrder.Door].setPixel(room1.right, y1, Prop.Door)
          self.__layers[LayerOrder.Door].setPixel(x2, room2.top, Prop.Door)
    # 세로 분할
    if not tree.isRowDivided:
      # 방1의 중앙 혹은 방2의 중앙이 방2 혹은 방1 안에 있는지
      if -room1.width / 2 <= abs(x1 - x2) <= room1.width / 2:
        self.__layers[LayerOrder.Door].setPixel(x2, room1.bottom, Prop.Door)
        self.__layers[LayerOrder.Door].setPixel(x2, room2.top, Prop.Door)
      else:
        if x1 > x2:
          self.__layers[LayerOrder.Door].setPixel(room1.left, y1, Prop.Door)
          self.__layers[LayerOrder.Door].setPixel(x2, room2.top, Prop.Door)
        else:
          self.__layers[LayerOrder.Door].setPixel(room1.right, y1, Prop.Door)
          self.__layers[LayerOrder.Door].setPixel(x2, room2.top, Prop.Door)

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
        self.__layers[LayerOrder.Door].setPixel(r.left, y1, Prop.Door)
        self.__layers[LayerOrder.Door].setPixel(r.right, y1, Prop.Door)
    for y in range(min(y1, y2), max(y1, y2) + 1):
      rs = self.__checkOverlappingRooms(x2, y)
      if tree.otherNode1.room in rs: rs.remove(tree.otherNode1.room)
      if tree.otherNode2.room in rs: rs.remove(tree.otherNode2.room)
      for r in rs:
        if r.node.parentNode == goalNode2.parentNode: continue
        self.__layers[LayerOrder.Door].setPixel(x2, r.top, Prop.Door)
        self.__layers[LayerOrder.Door].setPixel(x2, r.bottom, Prop.Door)
    self.__spawnDoorsFromBywayRooms(tree.otherNode1, n + 1)
    self.__spawnDoorsFromBywayRooms(tree.otherNode2, n + 1)

    # 플레이어 관련

  # 플레이어 관련
  def __spawnPlayer(self):
    self.__activeRoom = self.__latestRoom = choice(self.rooms)
    self.player = Player(self.__activeRoom)
    self.player.isInRoom = True
  def __drawPlayer(self):
    if self.__activeRoom != None:
      self.__layers[LayerOrder.UI].writeText("Enter 키를 눌러 방에 입장하기", (0, 40))
      drawNode(self.__layers[LayerOrder.Room], self.__activeRoom, Prop.Room, Prop.ActiveWall)
    elif self.__latestRoom != None:
      self.__layers[LayerOrder.UI].clear(40)
      drawNode(self.__layers[LayerOrder.Room], self.__latestRoom, Prop.Room)
    # 플레이어 표기
    self.__layers[LayerOrder.Player].clear()
    self.__layers[LayerOrder.Player].setPixel(self.player.position.x, self.player.position.y, Prop.Player)
  def __movePlayer(self, movement:str):
    def getRoomInPlayer()->BinaryRoom|None:
      filterdRooms = list(filter(lambda x:x.top < self.player.position.y < x.bottom and x.left < self.player.position.x < x.right, self.rooms))
      if(len(filterdRooms) == 0):
        return None
      return list(filterdRooms)[0]
    self.player.movePlayer(movement)
    direction = self.player.directions[self.player.lastDirection]
    # 방 안에 있는 상황이며, 방 외곽에 있을 경우, 안으로 들어오게 함
    if self.player.isInRoom and self.__activeRoom != None and (self.__activeRoom.top + 1 > self.player.position.y or self.player.position.y > self.__activeRoom.bottom - 1 or self.__activeRoom.left + 1 > self.player.position.x or self.player.position.x > self.__activeRoom.right - 1):
      self.player.position -= direction
    # 들어온 방 확인하기
    room = getRoomInPlayer()
    if self.__activeRoom != None:
      self.__latestRoom = self.__activeRoom
    self.__activeRoom = room
    # 문 있는지 체크하기
    forward = self.player.position + direction

    forwardPixel = self.__layers[LayerOrder.Door].getPixel(forward.x, forward.y)
    pixel = self.__layers[LayerOrder.Door].getPixel(self.player.position.x, self.player.position.y)
    pixel2 = self.__layers[LayerOrder.Road].getPixel(self.player.position.x, self.player.position.y)

    # 앞에 있는 픽셀 혹은 위에 있는 픽셀이 문일 경우
    if forwardPixel == Prop.Door or pixel == Prop.Door:
      self.player.isInRoom = False
    # 플레이어가 길 위에 없을 경우
    elif not self.player.isInRoom and pixel2 != Prop.Road:
      self.player.position -= direction
    # 방 안에 있는 상황이 아니며, 플레이어가 문 위에 있지 않으면 방 안에 있음을 확정
    elif not self.player.isInRoom and self.__activeRoom != None and pixel != Prop.Door:
      self.player.isInRoom = True
  def __updatePlayerUI(self):
    self.__layers[LayerOrder.UI].writeText(
      f"Lv. {self.player.stats.level: <10} Curse {self.player.stats.curse: <10} $ {self.player.stats.money: <5} Hp. {self.player.stats.health: <5} Pw. {self.player.stats.power: <5} Def. {self.player.stats.defense: <5} Energy {self.player.stats.energy: <5} Xp {self.player.stats.exp} / {self.player.stats.nextExp}",
      (0, 41)
    )

  # 게임 맵 초기화
  def __printMap(self):
    clearConsole()
    self.__drawPlayer()
    self.__updatePlayerUI()
    render = Render()
    render.print(render.addLayers(WIDTH, UI_HEIGHT, self.__layers))

  def __checkOverlappingRooms(self, x:int, y:int)->list[BinaryRoom]:
    return list(filter(lambda i:i.top <= y <= i.bottom and i.left <= x <= i.right, self.rooms))

  def __onPress(self, key:Key):
    if key == KeyCode.from_char('q'):
      self.__processQuit()
    # 방 입장 코드
    if key == Key.enter and self.__activeRoom != None:
      self.__running__ = False
      self.__listener.stop()
      self.manager.setGlobalVariable("inRoom", self.__activeRoom)
      self.manager.setGlobalVariable("rooms", self.rooms)
      self.manager.changeScene(1)
    # 움직이기 코드
    movement = self.__getMovement(key)
    if movement != None and movement not in self.__pressedMovements:
      self.__pressedMovements.append(movement)
      if len(self.__pressedMovements) > 3:
        self.__pressedMovements = []
  def __onRelease(self, key:Key):
    movement = self.__getMovement(key)
    if movement != None and movement in self.__pressedMovements:
      self.__pressedMovements.remove(movement)
      self.__movePlayer(movement)
      self.__printMap()

  def __getMovement(self, key:Key)->str|None:
    for k, v in self.__movementKeys.items():
      if key in v:
        return k
    return None

  def __processQuit(self):
    self.__running__ = False
    setCursorShow(True)
    self.__listener.stop()
