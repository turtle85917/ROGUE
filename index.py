from room import BinaryRoom

game_map = []

WIDTH = 40
HEIGHT = 20

for y in range(HEIGHT):
  game_map.append([])
  for x in range(WIDTH):
    game_map[y].append('.')

room = BinaryRoom(6, 4, 2, 2)
room.draw(game_map)

p = ''
for y in range(HEIGHT):
  for x in range(WIDTH):
    p += game_map[y][x]
  p += '\n'

print(p)
