import time
import curses

window = curses.initscr()
window.keypad(True)
window.nodelay(True)
curses.noecho()
curses.cbreak()

while True:
  key = window.getch()
  if key == curses.KEY_RIGHT: print("right")
  elif key == curses.KEY_LEFT: print("left")
  elif key == curses.KEY_UP: print("up")
  elif key == curses.KEY_DOWN: print("down")
  else: print(f"press: {key}")
  time.sleep(0.01)
