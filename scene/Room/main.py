from math import ceil

from scene.schema import Scene

from rendering.layer import Layer
from rendering.main import Render
from rendering.types.prop import Prop

from scene.MiniMap.node import BinaryRoom
from scene.MiniMap.utils import drawNode, clearConsole

from scene.manager import SceneManager

class Room(Scene):
  __room:BinaryRoom
  __layers:list[Layer] = []

  __width = 140
  __height = 50
  __margin = 10

  manager:SceneManager

  def __init__(self):
    super().__init__()

    self.sceneName = "Room"
    Layer.createNewLayers(self.__layers, 1, self.__width, self.__height)

  def render(self):
    clearConsole()
    self.__room = self.manager.getGlobalVariable("inRoom")
    # 들어온 방 설정하기
    self.__room.width = ceil(self.__room.width * 5)
    self.__room.height = ceil(self.__room.height * 5)

    self.__room.repos(self.__height / 2, self.__width / 2)

    # 방 그리기
    drawNode(self.__layers[0], self.__room, Prop.Room)

    # 출력
    render = Render()
    render.printLayer(self.__layers[0])
