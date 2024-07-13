import curses
from _types.CurseWindow import CursesWindow

from rendering.types.cell import Cell
from rendering.layer import Layer

class Render:
  __layers:list[Layer]
  __window:CursesWindow

  def __init__(self, window:CursesWindow, layers:list[Layer] = []):
    self.__layers = layers
    self.__window = window

  def print(self, cells:list[list[Cell]]):
    for y in range(0, len(cells)):
      for x in range(0, len(cells[0])):
        self.__window.addstr(y, x, cells[y][x].prop, curses.color_pair(cells[y][x].color))

  def pushLayer(self, layer:Layer):
    self.__layers.append(layer)
  def pushLayers(self, layers:list[Layer]):
    self.__layers += layers

  def removeLayer(self, layer:Layer):
    self.__layers.remove(layer)

  def addLayers(self, width:int, height:int, layers:list[Layer] = None)->list[list[Cell]]:
    result = self.__newEmptyLayer(width, height)
    _layers = layers if layers != None else self.__layers
    for layer in _layers:
      for y in range(height):
        for x in range(width):
          pixel = layer.getPixel(x, y)
          if pixel == None:
            result[y][x] = Layer.EMPTY
          elif pixel != Layer.EMPTY:
            result[y][x] = pixel
    return result
  def subtractLayers(self, width:int, height:int, subtractOrigin:Layer, subtractClip:Layer)->list[list[Cell]]:
    result = self.__newEmptyLayer(width, height)
    for layer in [subtractOrigin, subtractClip]:
      for y in range(height):
        for x in range(width):
          if layer == subtractClip:
            if layer.getPixel(x, y) != Layer.EMPTY:
              result[y][x] = Layer.EMPTY
          else:
            result[y][x] = layer.getPixel(x, y)
    return result

  def __newEmptyLayer(self, width:int, height:int)->list[list[Cell]]:
    return [[Layer.EMPTY for _ in range(width)] for _ in range(height)]
