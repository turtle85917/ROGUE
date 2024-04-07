class BinaryRoom:
  __min_width = 3
  __max_width = 10
  __min_height = 4
  __max_height = 7

  def __init__(self, width:int, height:int, left:int, top:int):
    self.width = width
    self.height = height
    self.left = left
    self.top = top

  def draw(self, game_map:list[list[int]]):
    for y in range(len(game_map)):
      if y >= self.top and self.height + self.top - 1 >= y:
        for x in range(len(game_map[y])):
          if x >= self.left and self.width + self.left - 1 >= x:
            game_map[y][x] = '#'
