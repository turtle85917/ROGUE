from random import randint
from math import ceil
import time

from object.position import Position
from _types.direction import Direction
from object.enemy.enemies import enemies

from rendering.types.prop import Prop
from rendering.types.cell import Cell
from rendering.layer import Layer
from rendering.utils import prop2cell

from scene.schema import Scene
from scene.manager import SceneManager
from scene.constants import WIDTH, HEIGHT

from scene.MiniMap.node import BinaryRoom, Node
from scene.MiniMap.utils import drawNode

from scene.Room.types.order import LayerOrder
from scene.Room.types.bubble import Bubble

class Room(Scene):
  __room:BinaryRoom

  __height = HEIGHT - 2

  # 버블 세팅
  __bubble = ['O', 'o']
  __bubbleColors = [21, 22, 10, 18]
  # 버블 목록
  __bubbles:list[Bubble] = []
  __bubbleQueues:list[Bubble] = []
  # 발사 시간
  __shout_time = 0

  __directions:dict[Direction, Position] = {
    Direction.Up: Position(0, -1),
    Direction.Down: Position(0, 1),
    Direction.Left: Position(-1, 0),
    Direction.Right: Position(1, 0)
  }

  manager:SceneManager

  def __init__(self):
    super().__init__()

    self.sceneName = "Room"

  def render(self):
    background = Node(WIDTH, HEIGHT - 1, 0, 0)
    drawNode(self.manager.layers[LayerOrder.Background], background)

    self.__room = self.manager.getGlobalVariable("inRoom")
    # 들어온 방 설정하기
    ratio = self.__room.width / self.__room.height
    if ratio < 2:
      ratio *= 2.4
    else:
      ratio *= 1.6
    self.__room.width = ceil(self.__room.width * ratio)
    self.__room.height = ceil(self.__room.height * ratio)
    self.__room.repos(self.__height // 2 - self.__room.height // 2, WIDTH // 2 - self.__room.width // 2)

    # 방 그리기
    drawNode(self.manager.layers[LayerOrder.Rooms], self.__room, prop2cell(Prop.Room), prop2cell(Prop.Wall))

    # 적 놓기
    enemyCount = randint(2, 5) # 2 ~ 5 적 배치
    if self.__room.width *  self.__room.height > 60:
      enemyCount = randint(4, 8)
    for _ in range(enemyCount):
      position = Position(0, 0)
      while True:
        position = Position(randint(self.__room.left + 1, self.__room.right - 1), randint(self.__room.top + 1, self.__room.bottom - 1))
        overlaps = list(filter(lambda x:x[1] == position, self.__room.enemies))
        if len(overlaps) == 0 and self.manager.player.position != position:
          break
      enemy = enemies[randint(0, len(enemies) - 1)]
      self.__room.enemies.append((enemy(), position))
      self.manager.layers[LayerOrder.Objects].setPixelByPosition(position, Cell(prop=enemy.icon, color=enemy.color))

    # 플레이어 놓기
    self.manager.player.enterRoom(self.__room)
    self.manager.layers[LayerOrder.Player].setPixelByPosition(self.manager.player.position, Layer.PLAYER)

    # 출력
    self.__printPlayer()
  def update(self):
    self.manager.player.movePlayer(self.manager.pressedKey, lambda: self.__printPlayer(), room=self.__room)
    match self.manager.player.getMovement(self.manager.pressedKey):
      case "attack-up":
        self.__shoutBubble(Direction.Up)
      case "attack-down":
        self.__shoutBubble(Direction.Down)
      case "attack-left":
        self.__shoutBubble(Direction.Left)
      case "attack-right":
        self.__shoutBubble(Direction.Right)
    # 버블 업데이트
    self.manager.layers[LayerOrder.Bubbles].clear()
    for bubble in self.__bubbles:
      if bubble in self.__bubbleQueues: continue
      if time.time() - bubble.life > .8:
        self.__bubbleQueues.append(bubble)
        continue
      sh = self.__bubble[0]
      # 색상 업데이트
      if time.time() - bubble.life > .3:
        bubble.color = self.__bubbleColors[1]
      if time.time() - bubble.life > .5:
        bubble.color = self.__bubbleColors[2]
        sh = self.__bubble[1]
      if time.time() - bubble.life > .7:
        bubble.color = self.__bubbleColors[3]
      # 위치 업데이트
      self.manager.layers[LayerOrder.Bubbles].setPixelByPosition(bubble.position, Cell(prop=sh, color=bubble.color))
      bubble.position += self.__directions.get(bubble.direction)
      # 제한
      if self.__room.top + 1 > bubble.position.y or bubble.position.y > self.__room.bottom - 1 or self.__room.left + 1 > bubble.position.x or bubble.position.x > self.__room.right - 1:
        bubble.position -= self.__directions.get(bubble.direction)
        self.__bubbleQueues.append(bubble)
        continue
    # 큐에 올라와진 버블 제거
    for bubble in self.__bubbleQueues:
      self.__bubbles.remove(bubble)
    else:
      self.__bubbleQueues = []

  def __printPlayer(self):
    self.manager.layers[LayerOrder.Player].clear()
    self.manager.layers[LayerOrder.Player].setPixelByPosition(self.manager.player.position, Layer.PLAYER)
    self.manager.layers[LayerOrder.UI].writeText(
      f"Lv. {self.manager.player.stats.level: <10} Curse {self.manager.player.stats.curse: <10} $ {self.manager.player.stats.money: <5} Hp. {self.manager.player.stats.health: <5} Pw. {self.manager.player.stats.power: <5} Def. {self.manager.player.stats.defense: <5} Energy {self.manager.player.stats.energy: <5} Xp {self.manager.player.stats.exp} / {self.manager.player.stats.nextExp}",
      (0, 41)
    )

  def __shoutBubble(self, direction:Direction):
    if time.time() - self.__shout_time < .2: return
    self.__shout_time = time.time()
    self.__bubbles.append(Bubble(life=time.time(), direction=direction, position=self.manager.player.position, color=self.__bubbleColors[0]))
