from __future__ import annotations

from rendering.types.prop import Prop
from rendering.utils import *

class Layer:
  __map:list[list[Prop]] = []
  EMPTY = Prop.Cell

  def __init__(self, width:int, height:int):
    self.width = width
    self.height = height
    self.__map = [[Layer.EMPTY for _ in range(self.width)] for _ in range(self.height)]

  @staticmethod
  def createNewLayers(layers:list[Layer], layerLength:int, width:int, height:int):
    for i in range(layerLength):
      layers.append(Layer(width, height))
      layers[i].fill(Layer.EMPTY)

  def getPixel(self, x:int, y:int):
    return self.__map[y][x]
  def setPixel(self, x:int, y:int, prop:Prop):
    self.__map[y][x] = prop

  def load(self, props:list[list[Prop]]):
    self.__map = props
  def clear(self):
    self.fill(Prop.Cell)

  def fill(self, prop:Prop):
    for y in range(self.height):
      for x in range(self.width):
        self.__map[y][x] = prop

  def drawRect(self, width:int, height:int, top:int, left:int):
    for y in range(self.height):
      if y >= top and top + height - 1 >= y:
        for x in range(self.width):
          if x >= left and left + width - 1 >= x:
            self.__map[y][x] = Layer.EMPTY

  @property
  def pixels(self)->list[list[Prop]]:
    return self.__map

  @property
  def shape(self)->str:
    text = ''
    for y in self.__map:
      for x in y:
        text += x
      text += '\n'
    return text
