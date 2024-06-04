from pynput.keyboard import Key, Listener

from rendering.core import Layer

class Player:
  running = True

  def __init__(self, initialPosition:tuple[int,int], layer:Layer):
    self.position = initialPosition
    self.layer = layer

  def run(self):
    while self.running:
      listener = Listener(on_press=self.onRealese)
      listener.start()

  def onRealese(self, key:Key):
    if key == Key.esc:
      self.running = False
