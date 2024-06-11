from rendering.types.prop import Prop
from rendering.layer import Layer
from rendering.utils import *

class Rendering:
  __layers:list[Layer]

  def __init__(self, layers:list[Layer] = []):
    self.__layers = layers

  def printLayer(self, layer:Layer)->str:
    print(layer.shape)
  def print(self, props:list[list[Prop]])->str:
    text = ''
    for y in props:
      for x in y:
        text += x
      text += '\n'
    print(text)

  def pushLayer(self, layer:Layer):
    self.__layers.append(layer)
  def pushLayers(self, layers:list[Layer]):
    self.__layers += layers

  def removeLayer(self, layer:Layer):
    self.__layers.remove(layer)

  def addLayers(self, width:int, height:int, layers:list[Layer] = None)->list[list[Prop]]:
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
  def subtractLayers(self, width:int, height:int, subtractOrigin:Layer, subtractClip:Layer)->list[list[Prop]]:
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

  def reverseLayer(self, layer:Layer)->Layer:
    result = self.__newEmptyLayer(layer.width, layer.height)
    pixel = getDominantColor(layer.pixels)
    for y in range(layer.height):
      for x in range(layer.width):
        if layer.getPixel(x, y) != Layer.EMPTY:
          result[y][x] = pixel
        else:
          result[y][x] = Layer.EMPTY
    newLayer = Layer(layer.width, layer.height)
    newLayer.load(result)
    return newLayer

  def __newEmptyLayer(self, width:int, height:int)->list[list[Prop]]:
    return [[Layer.EMPTY for _ in range(width)] for _ in range(height)]
