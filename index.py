from room import Room

game_map = []

WIDTH = 100
HEIGHT = 40

for y in range(HEIGHT):
  game_map.append([])
  for x in range(WIDTH):
    game_map[y].append('.')

rooms = Room(10)
rooms.drawRooms(game_map)

p = ''
for y in range(HEIGHT):
  for x in range(WIDTH):
    p += game_map[y][x]
  p += '\n'

print(p)
