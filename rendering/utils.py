from rendering.types.prop import Prop
from rendering.types.cell import Cell

def getDominantColor(layer:list[list[Cell]])->Cell:
  colorPalettes:dict[Cell, int] = {}
  for y in layer:
    for x in y:
      if colorPalettes.get(x) == None:
        colorPalettes[x] = 0
      colorPalettes[x] += 1
  colorPalettes = {k: v for k, v in sorted(colorPalettes.items(), key=lambda x: x[1], reverse=True)}
  return list(colorPalettes)[0]

def prop2cell(prop:Prop):
  return Cell(prop=prop, color=0)
