from room import Room
from constants import *

game_map = []

for y in range(HEIGHT):
  game_map.append([])
  for x in range(WIDTH):
    game_map[y].append(CELL)

rooms = Room(MAX_ROOM)
rooms.connectRooms(game_map)
rooms.drawRooms(game_map)

p = ''
for y in range(HEIGHT):
  for x in range(WIDTH):
    p += game_map[y][x]
  p += '\n'

print(p)
