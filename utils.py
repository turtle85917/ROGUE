from constants import Props
from node import BinaryRoom, Node

def drawNode(game_map:list[list[str]], node:Node | BinaryRoom, fill_cell:Props = Props.CELL):
  right = node.width + node.left - 1
  bottom = node.height + node.top - 1
  for y in range(len(game_map)):
    if y >= node.top and bottom >= y:
      for x in range(len(game_map[y])):
        if x >= node.left and right >= x:
          if x == node.left or x == right or y == node.top or y == bottom:
            game_map[y][x] = Props.WALL
          else:
            game_map[y][x] = fill_cell
