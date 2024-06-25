from math import ceil

from scene.schema import Scene

from rendering.main import Render
from rendering.types.prop import Prop

from player.core import Player

from scene.manager import SceneManager
from scene.constants import WIDTH, HEIGHT
from scene.utils import clearConsole, getKey

from scene.MiniMap.node import BinaryRoom, Node
from scene.MiniMap.utils import drawNode

from scene.Room.types.order import LayerOrder

class Room(Scene):
  __room:BinaryRoom
  __player:Player

  __height = HEIGHT - 2

  manager:SceneManager

  def __init__(self):
    super().__init__()

    self.sceneName = "Room"
    self.updatable = False

  def render(self):
    clearConsole()

    background = Node(WIDTH, HEIGHT - 1, 0, 0)
    drawNode(self.manager.layers[LayerOrder.Background], background)

    self.__room = self.manager.getGlobalVariable("inRoom")
    # 들어온 방 설정하기
    ratio = self.__room.width / self.__room.height
    ratio *= 3
    self.__room.width = ceil(self.__room.width * ratio)
    self.__room.height = ceil(self.__room.height * ratio)
    self.__room.repos(self.__height // 2 - self.__room.height // 2, WIDTH // 2 - self.__room.width // 2)

    # 방 그리기
    drawNode(self.manager.layers[LayerOrder.Room], self.__room, Prop.Room)

    # 플레이어 놓기
    self.__player = Player(self.__room)
    self.manager.layers[LayerOrder.Player].setPixel(self.__player.position.x, self.__player.position.y, Prop.Player)

    # 출력
    self.__printPlayer()
    self.manager.listen()

  def __printPlayer(self):
    clearConsole()
    self.manager.layers[LayerOrder.Player].clear()
    self.manager.layers[LayerOrder.Player].setPixel(self.__player.position.x, self.__player.position.y, Prop.Player)
    self.manager.layers[LayerOrder.UI].writeText(
      f"Lv. {self.__player.stats.level: <10} Curse {self.__player.stats.curse: <10} $ {self.__player.stats.money: <5} Hp. {self.__player.stats.health: <5} Pw. {self.__player.stats.power: <5} Def. {self.__player.stats.defense: <5} Energy {self.__player.stats.energy: <5} Xp {self.__player.stats.exp} / {self.__player.stats.nextExp}",
      (0, 41)
    )
    self.manager.print()

  def _onPress(self, key):
    key = getKey(key)
    self.__player.movePlayer(key, lambda: self.__printPlayer())
