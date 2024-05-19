from rendering.types.pixel import Pixel
from rendering.layer import Layer

class Rendering:
  __layers:list[Layer]

  def __init__(self, layers:list[Layer] = []):
    self.__layers = layers

  def pushLayer(self, layer:Layer):
    self.__layers.append(layer)
  def pushLayers(self, layers:list[Layer]):
    self.__layers += layers

  def removeLayer(self, layer:Layer):
    self.__layers.remove(layer)

  def addLayers(self, width:int, height:int)->list[list[Pixel]]:
    result = self.__newEmptyLayer(width, height)
    for layer in self.__layers:
      for y in range(height):
        for x in range(width):
          if layer.getPixel(x, y) != Pixel.Empty:
            result[y][x] = layer.getPixel(x, y)
    return result

  def subtractLayers(self, width:int, height:int, subtractOrigin:Layer, subtractClip:Layer)->list[list[Pixel]]:
    result = self.__newEmptyLayer(width, height)
    for layer in [subtractOrigin, subtractClip]:
      for y in range(height):
        for x in range(width):
          if layer == subtractClip:
            if layer.getPixel(x, y) != Pixel.Empty:
              result[y][x] = Pixel.Empty
          else:
            result[y][x] = layer.getPixel(x, y)
    return result

  def __newEmptyLayer(self, width:int, height:int)->list[list[Pixel]]:
    return [[Pixel.Empty for _ in range(width)] for _ in range(height)]
