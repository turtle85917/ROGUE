from rendering.types.pixel import Pixel
from rendering.constants import Props

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
