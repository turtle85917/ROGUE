import time
import curses

window = curses.initscr()
window.keypad(True)
window.nodelay(True)

curses.noecho()
curses.cbreak()

curses.start_color()
curses.use_default_colors()

for i in range(0, 255):
  curses.init_pair(i + 1, i, i)

pressed = ''
_time = 0
frame = 0

while True:
  key = window.getch()
  window.erase()
  window.addstr(f"{pressed}\nframne: {frame}\n", 0)
  for i in range(0, 255):
    window.addstr(f"{i:5}", curses.color_pair(i))
    if i % 10 == 0:
      window.addstr('\n', 0)
  window.refresh()
  if key == curses.KEY_RIGHT: pressed = "right"
  elif key == curses.KEY_LEFT: pressed = "left"
  elif key == curses.KEY_UP: pressed = "up"
  elif key == curses.KEY_DOWN: pressed = "down"
  elif key != -1:
    pressed = chr(key)
    if pressed == '\n':
      pressed = 'enter'
    if key == ord('q'):
      break
  _time += 1
  frame = _time // 10
  time.sleep(0.01)

curses.endwin()
