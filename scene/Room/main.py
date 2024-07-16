from random import randint, choice
from math import ceil
import time
import uuid

from object.position import Position
from _types.direction import Direction

from object.base import BaseStats
from object.enemy.enemies import enemies, Slime

from rendering.types.prop import Prop
from rendering.types.cell import Cell
from rendering.layer import Layer

from scene.schema import Scene
from scene.manager import SceneManager
from scene.constants import WIDTH, HEIGHT

from scene.MiniMap.node import BinaryRoom, Node
from scene.MiniMap.types.enemy import Enemy

from scene.Room.types.bubble import Bubble
from scene.Room.types.timing import Timing
from scene.Room.types.order import LayerOrder

from object.utils import getSpawnPos
from rendering.utils import prop2cell
from scene.MiniMap.utils import drawNode

class Room(Scene):
  __room:BinaryRoom
  __isClear:bool

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
  __notGoneLog:bool = False

  __enemyQueues:list[Enemy] = []

  __directions:dict[Direction, Position] = {
    Direction.Up: Position(0, -1),
    Direction.Down: Position(0, 1),
    Direction.Left: Position(-1, 0),
    Direction.Right: Position(1, 0)
  }
  __compassDirections:list[Position] = [
    Position(-1, -1),
    Position(0, -1),
    Position(1, -1),
    Position(-1, 0),
    Position(1, 0),
    Position(-1, 1),
    Position(0, 1),
    Position(1, 1)
  ]

  manager:SceneManager

  def __init__(self):
    super().__init__()

    self.sceneName = "Room"

  def render(self):
    background = Node(WIDTH, HEIGHT - 2, 0, 0)
    drawNode(self.manager.layers[LayerOrder.Background], background, border_cell=Cell(prop=Prop.Wall, color=240))

    self.__isClear = False

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
    drawNode(self.manager.layers[LayerOrder.Rooms], self.__room, prop2cell(Prop.Cell), prop2cell(Prop.Wall))

    # 적 놓기
    enemyCount = randint(2, 5) # 2 ~ 5 적 배치
    if self.__room.width *  self.__room.height > 60:
      enemyCount = randint(4, 14)
    for _ in range(enemyCount):
      position = getSpawnPos(self.manager, self.__room)
      enemy = enemies[randint(0, len(enemies) - 1)]
      self.__room.enemies.append(Enemy(uuid=uuid.uuid4(), enemy=enemy(), health=enemy.stats.maxHealth, position=position))
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
      case "exit":
        self.manager.changeScene(0)
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
          data.health -= pow
          self.__log = [(f"Attacked {data.enemy.id}! ", 0), (f"HP -{pow} ", 5)]
          self.__notGoneLog = False
          self.__bubbleQueues.append(bubble)
          # 적이 죽었는지 확인
          if data.health <= 0:
            self.__enemyQueues.append(data)
            self.__loggedAt = time.time()
            self.__log[0] = (f"Killed {data.enemy.id}! ", 0)
            self.__log.append((f"EXP -{data.enemy.stats.exp}", 11))
            self.manager.player.stats.exp += data.enemy.stats.exp
            self.__processKilledEnemy(data)
            self.__notGoneLog = True
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

    # 플레이어 레벨업 처리
    if self.manager.player.stats.exp >= self.manager.player.stats.nextExp:
      isLevelUp = self.manager.player.levelUp()
      if isLevelUp:
        self.__log = [("Congratulation! Level Up! ", 0), (f"Lv: {self.manager.player.stats.level} ", 230), (f"Exp: {self.manager.player.stats.exp} ", 195), (f"Next Exp: {self.manager.player.stats.nextExp}", 196)]
        self.__loggedAt = time.time()
        self.__notGoneLog = True

    # 출력
    self.__printScreen()

  def __printScreen(self):
    self.manager.layers[LayerOrder.Player].setPixelByPosition(self.manager.player.position, Layer.PLAYER)
    self.manager.layers[LayerOrder.UI].writeText([(f"Lv. {self.manager.player.stats.level: <10} Curse {self.manager.player.stats.curse: <10} $ {self.manager.player.stats.money: <5} Hp. {self.manager.player.health: <5} Pw. {self.manager.player.stats.power: <5} Def. {self.manager.player.stats.defense: <5} Energy {self.manager.player.stats.energy: <5} Xp {self.manager.player.stats.exp} / {self.manager.player.stats.nextExp}", 0)], (0, 41))
    if self.__isClear:
      self.manager.layers[LayerOrder.UI].writeText([("To exit the room press 'Enter'", 0)], (0, 40))
    elif time.time() - self.__loggedAt < 1.6 or self.__notGoneLog:
      self.manager.layers[LayerOrder.UI].writeText(self.__log, (0, 40))

  def __shoutBubble(self, direction:Direction):
    if time.time() - self.__shout_time < .2: return
    self.__shout_time = time.time()
    self.__bubbles.append(Bubble(life=time.time(), direction=direction, position=self.manager.player.position))

  __slime_colors:list[int] = [41, 155, 227] # 37
  __light_colors:list[int] = [7, 191, 221, 229, 230]
  __cooldown_queues:list[Timing] = []
  def __processEnemyAI(self, data:Enemy):
    match data.enemy.id:
      case "bat":
        direction = self.manager.player.position - data.position
        if direction.x == 0 or direction.y == 0:
          if self.checkCooldown(data.uuid, 5.):
            self.manager.layers[LayerOrder.Effects].setPixelByPosition(data.position + Position(0, -1), Cell(prop='!', color=197))
            return
          self.manager.layers[LayerOrder.Effects].drawLine(data.position, self.manager.player.position, Cell(prop=Prop.Light, color=choice(self.__light_colors)))
          if not self.checkCooldown(data.uuid, 6.5):
            self.setCooldown(data.uuid)
        else:
          self.removeCooldown(data.uuid)
  def __processKilledEnemy(self, data:Enemy):
    match data.enemy.id:
      case "slime":
        if data.enemy.stats.penetrate == 3: return
        slime1 = Slime()
        slime2 = Slime()

        slime1.color = self.__slime_colors[data.enemy.stats.penetrate]
        slime2.color = slime1.color

        stats = BaseStats(
          level = data.enemy.stats.level,
          maxHealth = round(data.enemy.stats.maxHealth * 0.7),
          power = round(data.enemy.stats.power * 1.1),
          defense = data.enemy.stats.defense + 1,
          exp = data.enemy.stats.exp + 1,
          penetrate = data.enemy.stats.penetrate + 1
        )

        slime1.stats = stats
        slime2.stats = stats

        position1 = getSpawnPos(self.manager, self.__room, self.__compassDirections, data.position)
        position2 = getSpawnPos(self.manager, self.__room, self.__compassDirections, data.position, lambda pos:pos != position1)

        self.__room.enemies.append(Enemy(uuid=uuid.uuid4(), enemy=slime1, health=slime1.stats.maxHealth, position=position1))
        self.__room.enemies.append(Enemy(uuid=uuid.uuid4(), enemy=slime2, health=slime2.stats.maxHealth, position=position2))

  def checkCooldown(self, uuid:str, expired:int)->bool:
    cooldown = list(filter(lambda x:x.uuid == uuid, self.__cooldown_queues))
    if len(cooldown) == 0:
      self.setCooldown(uuid)
      return True
    return time.time() - cooldown[0].startedAt <= expired
  def setCooldown(self, uuid:str):
    self.removeCooldown(uuid)
    self.__cooldown_queues.append(Timing(uuid=uuid, startedAt=time.time()))
  def removeCooldown(self, uuid:str):
    cooldown = list(filter(lambda x:x.uuid == uuid, self.__cooldown_queues))
    if len(cooldown) > 0:
      self.__cooldown_queues.remove(cooldown[0])
