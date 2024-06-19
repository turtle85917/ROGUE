from math import ceil

from scene.schema import Scene

from rendering.layer import Layer
from rendering.main import Render
from rendering.types.prop import Prop

from player.core import Player
from scene.manager import SceneManager
from scene.utils import clearConsole, getKey

from scene.MiniMap.node import BinaryRoom, Node
from scene.MiniMap.utils import drawNode

from scene.Room.types.order import LayerOrder

class Room(Scene):
  __room:BinaryRoom
  __layers:list[Layer] = []

  __player:Player

  __width = 140
  __height = 50

  manager:SceneManager

  def __init__(self):
    super().__init__()

    self.sceneName = "Room"
    Layer.createNewLayers(self.__layers, 4, self.__width, self.__height)

  def render(self):
    clearConsole()

    background = Node(self.__width, self.__height, 0, 0)
    drawNode(self.__layers[LayerOrder.Background], background)

    self.__room = self.manager.getGlobalVariable("inRoom")
    # 들어온 방 설정하기
    ratio = self.__room.width / self.__room.height # if self.__room.width > self.__room.height else self.__room.height / self.__room.width
    ratio *= 3
    self.__room.width = ceil(self.__room.width * ratio)
    self.__room.height = ceil(self.__room.height * ratio)
    self.__room.repos(self.__height // 2 - self.__room.height // 2, self.__width // 2 - self.__room.width // 2)

    # 방 그리기
    drawNode(self.__layers[LayerOrder.Room], self.__room, Prop.Room)

    # 플레이어 놓기
    self.__player = Player(self.__room)
    self.__layers[LayerOrder.Player].setPixel(self.__player.position.x, self.__player.position.y, Prop.Player)

    # 출력
    render = Render()
    render.print(
      render.addLayers(self.__width, self.__height, self.__layers)
    )
    self.manager.listen()

  def __printPlayer(self):
    clearConsole()
    self.__layers[LayerOrder.Player].clear()
    self.__layers[LayerOrder.Player].setPixel(self.__player.position.x, self.__player.position.y, Prop.Player)
    render = Render()
    render.print(
      render.addLayers(self.__width, self.__height, self.__layers)
    )
    self.__layers[LayerOrder.UI].writeText(
      f"Lv. {self.__player.stats.level: <10} Curse {self.__player.stats.curse: <10} $ {self.__player.stats.money: <5} Hp. {self.__player.stats.health: <5} Pw. {self.__player.stats.power: <5} Def. {self.__player.stats.defense: <5} Energy {self.__player.stats.energy: <5} Xp {self.__player.stats.exp} / {self.__player.stats.nextExp}",
      (0, 41)
    )

  def _onPress(self, key):
    key = getKey(key)
    self.__player.checkMovement(key)
    self.__player.movePlayer(key, lambda: self.__printPlayer())
  def _onRelease(self, key):
    key = getKey(key)
    # self.__player.movePlayer(key)

