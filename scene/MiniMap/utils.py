from rendering.types.prop import Prop
from rendering.layer import Layer

from scene.MiniMap.node import BinaryRoom, Node

def drawNode(layer:Layer, node:Node|BinaryRoom, fill_cell:Prop = Layer.EMPTY, border_cell:Prop = Prop.Wall):
  '''
  노드를 그립니다.
  '''
  right = node.width + node.left - 1
  bottom = node.height + node.top - 1
  for y in range(layer.height):
    if y >= node.top and bottom >= y:
      for x in range(layer.width):
        if x >= node.left and right >= x:
          if x == node.left or x == right or y == node.top or y == bottom:
            layer.setPixel(x, y, border_cell)
          else:
            layer.setPixel(x, y, fill_cell)
