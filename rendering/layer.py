from dataclasses import dataclass

from types.pixel import Pixel
from rendering.utils import *

@dataclass
class Layer:
  width:int
  height:int
  top:int
  left:int

  _map:list[list[Pixel]] = []

  def __init__(self):
    self._map = [[Pixel.Empty for _ in range(self.width)] for _ in range(self.height)]

  @property
  def to_string(self)->str:
    text = ''
    for y in self._map:
      for x in y:
        text += getProps(x)
      text += '\n'
    return text
