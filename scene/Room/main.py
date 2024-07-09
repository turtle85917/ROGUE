from random import randint, choice
from math import ceil
import time
import uuid

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
from scene.MiniMap.types.enemy import Enemy

from scene.Room.types.bubble import Bubble
from scene.Room.types.timing import Timing
from scene.Room.types.order import LayerOrder

class Room(Scene):
  __room:BinaryRoom

  __height = HEIGHT - 3

  # 버블 세팅
  __bubble = ['O', 'o']
  # 버블 목록
  __bubbles:list[Bubble] = []
  __bubbleQueues:list[Bubble] = []
  # 발사 시간
  __shout_time = 0

  # 로그
  __log:list[tuple[str, int]] = []
  __loggedAt:int = 0

  __enemyQueues:list[Enemy] = []

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
    background = Node(WIDTH, HEIGHT - 2, 0, 0)
    drawNode(self.manager.layers[LayerOrder.Background], background)

    self.__room = self.manager.getGlobalVariable("inRoom")
    # 들어온 방 설정하기
    ratio = self.__room.width / self.__room.height
    if ratio < 2:
      ratio *= 2.2
    else:
      ratio *= 1.6
    self.__room.width = ceil(self.__room.width * ratio)
    self.__room.height = ceil(self.__room.height * ratio)
    self.__room.repos(self.__height // 2 - self.__room.height // 2 + 1, WIDTH // 2 - self.__room.width // 2 + 1)

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
        overlaps = list(filter(lambda x:x.position == position, self.__room.enemies))
        if len(overlaps) == 0 and self.manager.player.position != position:
          break
      enemy = enemies[randint(0, len(enemies) - 1)]
      self.__room.enemies.append(Enemy(uuid=uuid.uuid4(), enemy=enemy(), position=position))
      self.manager.layers[LayerOrder.Objects].setPixelByPosition(position, enemy.cell)

    # 플레이어 놓기
    self.manager.player.enterRoom(self.__room)
    self.manager.layers[LayerOrder.Player].setPixelByPosition(self.manager.player.position, Layer.PLAYER)

    # 출력
    self.__printScreen()
  def update(self):
    # 레이어 초기화
    self.manager.layers[LayerOrder.Effects].clear()
    self.manager.layers[LayerOrder.Player].clear()
    self.manager.layers[LayerOrder.UI].clear()

    self.manager.player.movePlayer(self.manager.pressedKey, room=self.__room)
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
      if time.time() - bubble.life > .4:
        self.__bubbleQueues.append(bubble)
        continue
      sh = self.__bubble[0]
      # 버블 업데이트
      if time.time() - bubble.life > .25:
        sh = self.__bubble[1]
      # 위치 업데이트
      self.manager.layers[LayerOrder.Bubbles].setPixelByPosition(bubble.position, Cell(prop=sh, color=22))
      bubble.position += self.__directions.get(bubble.direction)
      # 공격하기
      for data in self.__room.enemies:
        if bubble in self.__bubbleQueues: break
        if data.position == bubble.position and data not in self.__enemyQueues:
          pow = self.manager.player.stats.power
          data.enemy.stats.health -= pow
          self.__log = [(f"Attacked {data.enemy.id}! ", 0), (f"HP -{pow} ", 5)]
          self.__bubbleQueues.append(bubble)
          # 적이 죽었는지 확인
          if data.enemy.stats.health <= 0:
            self.__enemyQueues.append(data)
            self.__loggedAt = time.time()
            self.__log.append((f"EXP -{data.enemy.stats.exp}", 11))
            self.manager.player.stats.exp += data.enemy.stats.exp
          self.__loggedAt = time.time()
          break
      # 움직임 제한
      if self.__room.top + 1 > bubble.position.y or bubble.position.y > self.__room.bottom - 1 or self.__room.left + 1 > bubble.position.x or bubble.position.x > self.__room.right - 1:
        bubble.position -= self.__directions.get(bubble.direction)
        self.__bubbleQueues.append(bubble)
        continue
    # 큐에 올라와진 버블 제거
    for bubble in self.__bubbleQueues:
      self.__bubbles.remove(bubble)
    else:
      self.__bubbleQueues = []

    # 적 관련
    self.manager.layers[LayerOrder.Objects].clear()
    for data in self.__room.enemies:
      # 적 AI 관련 제어
      self.__processEnemyAI(data)
      # 재위치-
      self.manager.layers[LayerOrder.Objects].setPixelByPosition(data.position, data.enemy.cell)
    # 큐에 올라와진 적 제거
    for data in self.__enemyQueues:
      self.__room.enemies.remove(data)
    else:
      self.__enemyQueues = []

    # 출력
    self.__printScreen()

  def __printScreen(self):
    self.manager.layers[LayerOrder.Player].setPixelByPosition(self.manager.player.position, Layer.PLAYER)
    self.manager.layers[LayerOrder.UI].writeText([(f"Lv. {self.manager.player.stats.level: <10} Curse {self.manager.player.stats.curse: <10} $ {self.manager.player.stats.money: <5} Hp. {self.manager.player.stats.health: <5} Pw. {self.manager.player.stats.power: <5} Def. {self.manager.player.stats.defense: <5} Energy {self.manager.player.stats.energy: <5} Xp {self.manager.player.stats.exp} / {self.manager.player.stats.nextExp}", 0)], (0, 41))
    if time.time() - self.__loggedAt < 1.2:
      self.manager.layers[LayerOrder.UI].writeText(self.__log, (0, 40))

  def __shoutBubble(self, direction:Direction):
    if time.time() - self.__shout_time < .2: return
    self.__shout_time = time.time()
    self.__bubbles.append(Bubble(life=time.time(), direction=direction, position=self.manager.player.position))

  __light_colors:list[int] = [7, 191, 221, 229, 230]
  __attack_timings:list[Timing] = []
  __cooldown_queues:list[Timing] = []
  def __processEnemyAI(self, data:Enemy):
    match data.enemy.id:
      case "bat":
        direction = self.manager.player.position - data.position
        if (direction.x == 0 or direction.y == 0) and self.checkCooldown(data.uuid, 1.4):
          self.setTiming(data.uuid)
          if time.time() - self.getTiming(data.uuid).startedAt > 1.:
            self.manager.layers[LayerOrder.Effects].drawLine(data.position, self.manager.player.position, Cell(prop=Prop.Light, color=choice(self.__light_colors)))
            self.removeTiming(data.uuid)
          else:
            self.manager.layers[LayerOrder.Effects].setPixelByPosition(data.position + Position(0, -1), Cell(prop='!', color=197))
        else:
          self.removeTiming(data.uuid)

  def getTiming(self, uuid:str)->Timing|None:
    for timing in self.__attack_timings:
      if timing.uuid == uuid:
        return timing
    return None
  def setTiming(self, uuid:str):
    self.__attack_timings.append(Timing(uuid=uuid, startedAt=time.time()))
  def removeTiming(self, uuid:str)->bool:
    timing = self.getTiming(uuid)
    if not timing:
      return False
    self.__attack_timings.remove(timing)
    self.__cooldown_queues.append(Timing(uuid=uuid, startedAt=time.time()))
    return True

  def checkCooldown(self, uuid:str, expired:int)->bool:
    cooldown = list(filter(lambda x:x.uuid == uuid and time.time() - x.startedAt > expired, self.__cooldown_queues))
    if self.getTiming(uuid) == None:
      return True
    return len(cooldown) > 0
