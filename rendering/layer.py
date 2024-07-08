from __future__ import annotations

from object.position import Position

from rendering.types.prop import Prop
from rendering.types.cell import Cell
from rendering.utils import prop2cell

class Layer:
  __map:list[list[Cell]] = []

  EMPTY  = prop2cell(Prop.Cell)
  PLAYER = prop2cell(Prop.Player)

  def __init__(self, width:int, height:int):
    self.width = width
    self.height = height
    self.__map = [[Layer.EMPTY for _ in range(self.width)] for _ in range(self.height)]

  @staticmethod
  def createNewLayers(layers:list[Layer], layerLength:int, width:int, height:int):
    for i in range(layerLength):
      layers.append(Layer(width, height))
      layers[i].fill(Layer.EMPTY)

  def getPixel(self, x:int, y:int)->Cell|None:
    return self.getPixelByPosition(Position(x, y))
  def getPixelByPosition(self, position:Position):
    if position.y >= len(self.__map):
      return None
    if position.x >= len(self.__map[position.y]):
      return None
    return self.__map[position.y][position.x]
  def setPixel(self, x:int, y:int, cell:Cell):
    self.__map[y][x] = cell
  def setPixelByPosition(self, position:Position, cell:Cell):
    self.__map[position.y][position.x] = cell

  def writeText(self, txt:str, pos:tuple[int,int]):
    x = pos[0]
    y = pos[1]
    for char in txt:
      self.__map[y][x] = Cell(prop=char, color=0)
      x += 1
      if x >= self.width: break
      if char == "\n":
        x = pos[0]
        y += 1
        if y >= self.height: break

  def load(self, cells:list[list[Cell]]):
    self.__map = cells
  def clear(self, row:int = -1):
    if row != -1:
      for index in range(len(self.__map[row])):
        self.__map[row][index] = Layer.EMPTY
    else:
      self.fill(Layer.EMPTY)

  def fill(self, cell:Cell):
    for y in range(self.height):
      for x in range(self.width):
        self.__map[y][x] = cell

  def drawRect(self, width:int, height:int, top:int, left:int):
    for y in range(self.height):
      if y >= top and top + height - 1 >= y:
        for x in range(self.width):
          if x >= left and left + width - 1 >= x:
            self.__map[y][x] = Layer.EMPTY

  @property
  def pixels(self)->list[list[Cell]]:
    return self.__map
