'''

레이어가 있음

레이어 6

레이어 5

레이어 4

레이어 3

레이어 2

레이어 1

'''

from __future__ import annotations

from rendering.types.pixel import Pixel
from rendering.constants import Props
from rendering.layer import Layer
from rendering.core import Rendering
from rendering.utils import getProps

WIDTH = 80
HEIGHT = 20

def printLayer(layer:list[list[Pixel]])->str:
  text = ''
  for y in layer:
    for x in y:
      text += getProps(x)
    text += '\n'
  print(text)

render = Rendering()

layer6 = Layer(WIDTH, HEIGHT)
layer5 = Layer(WIDTH, HEIGHT)

layer6.fill(Pixel.Test1)
layer5.fill(Pixel.Test2)

layer6.drawRect(10, 6, 7, 5)

render.pushLayers([layer5, layer6])

print(layer6.shape)
print(layer5.shape)

printLayer(render.addLayers(layer6.width, layer6.height))
printLayer(render.subtractLayers(layer6.width, layer6.height, layer5, layer6))

printLayer(render.reverseLayer(layer6))
