from rendering.types.pixel import Pixel
from rendering.utils import *

class Layer:
  __map:list[list[Pixel]] = []

  def __init__(self, width:int, height:int):
    self.width = width
    self.height = height
    self.__map = [[Pixel.Empty for _ in range(self.width)] for _ in range(self.height)]

  def getPixel(self, x:int, y:int):
    return self.__map[y][x]
  def setPixel(self, x:int, y:int, pixel:Pixel):
    self.__map[y][x] = pixel

  def fill(self, pixel:Pixel):
    for y in range(self.height):
      for x in range(self.width):
        self.__map[y][x] = pixel

  def drawRect(self, width:int, height:int, top:int, left:int):
    for y in range(self.height):
      if y >= top and top + height - 1 >= y:
        for x in range(self.width):
          if x >= left and left + width - 1 >= x:
            self.__map[y][x] = Pixel.Empty

  @property
  def shape(self)->str:
    text = ''
    for y in self.__map:
      for x in y:
        text += getProps(x)
      text += '\n'
    return text
