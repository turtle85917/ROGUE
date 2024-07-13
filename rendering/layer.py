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

  def writeText(self, texts:list[tuple[str,int]], pos:tuple[int,int]):
    x = pos[0]
    y = pos[1]
    for text, color in texts:
      for char in text:
        self.__map[y][x] = Cell(prop=char, color=color, isText=True)
        x += 1
        if x >= self.width: break
        if char == "\n":
          x = pos[0]
          y += 1
          if y >= self.height: break
  def clear(self, row:int = -1):
    if row != -1:
      for index in range(0, self.width):
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
  def drawLine(self, start:Position, end:Position, cell:Cell):
    start_y = max(start.y, end.y)
    end_y = min(start.y, end.y)
    start_x = max(start.x, end.x)
    end_x = min(start.x, end.x)
    for y in range(0, self.height):
      for x in range(0, self.width):
        if start.x == end.x and x == start.x and start_y > y > end_y:
          self.__map[y][x] = cell
        if start.y == end.y and y == start.y and start_x > x > end_x:
          self.__map[y][x] = cell

  @property
  def pixels(self)->list[list[Cell]]:
    return self.__map
