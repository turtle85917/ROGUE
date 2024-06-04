from rendering.types.prop import Prop

def getDominantColor(layer:list[list[Prop]])->Prop:
  colorPalettes:dict[Prop, int] = {}
  for y in layer:
    for x in y:
      if colorPalettes.get(x) == None:
        colorPalettes[x] = 0
      colorPalettes[x] += 1
  colorPalettes = {k: v for k, v in sorted(colorPalettes.items(), key=lambda x: x[1], reverse=True)}
  return list(colorPalettes)[0]
