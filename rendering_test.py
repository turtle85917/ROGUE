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

WIDTH = 80
HEIGHT = 20

def printLayer(layer:list[list[Pixel]])->str:
  text = ''
  for y in layer:
    for x in y:
      text += getProps(x)
    text += '\n'
  print(text)

def getProps(pixel:Pixel):
  match pixel:
    case Pixel.Test1:
      return Props.COLORED_BLOCK
    case Pixel.Test2:
      return Props.COLORED_BLOCK2
    case _:
      return Props.CELL

def getDominantColor(layer:list[list[Pixel]])->Pixel:
  colorPalettes:dict[Pixel, int] = {}
  for y in layer:
    for x in y:
      if colorPalettes.get(x) == None:
        colorPalettes[x] = 0
      colorPalettes[x] += 1
  colorPalettes = {k: v for k, v in sorted(colorPalettes.items(), key=lambda x: x[1], reverse=True)}
  return list(colorPalettes)[0]

layer6 = Layer(WIDTH, HEIGHT)
layer5 = Layer(WIDTH, HEIGHT)

layer6.fill(Pixel.Test1)
layer5.fill(Pixel.Test2)

layer6.drawRect(10, 6, 7, 5)

print(layer6.shape)
print(layer5.shape)

# printLayer(layer6)
# printLayer(layer5)

# layers = [layer5, layer6]
# result = [[Pixel.Empty for _ in range(WIDTH)] for _ in range(HEIGHT)]

# for layer in layers:
#   for y in range(HEIGHT):
#     for x in range(WIDTH):
#       if layer[y][x ] != Pixel.Empty:
#         result[y][x] = layer[y][x]

# printLayer(result)

# substractOrigin = layer5
# substractClip = layer6
# result = [[Pixel.Empty for _ in range(WIDTH)] for _ in range(HEIGHT)]
# for layer in [substractOrigin, substractClip]:
#   for y in range(HEIGHT):
#     for x in range(WIDTH):
#       if layer == substractClip:
#         if layer[y][x] != Pixel.Empty:
#           result[y][x] = Props.CELL
#       else:
#         result[y][x] = layer[y][x]

# printLayer(result)

# result = [[Pixel.Empty for _ in range(WIDTH)] for _ in range(HEIGHT)]
# for y in range(HEIGHT):
#   for x in range(WIDTH):
#     if layer[y][x] == Pixel.Empty:
#       result[y][x] = getDominantColor(layer6)
#     else:
#       result[y][x] = Props.CELL

# printLayer(result)
