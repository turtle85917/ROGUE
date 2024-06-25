from object.base import BaseEnemy, BaseStats
from rendering.style import Style, AnsiColor

class Bat(BaseEnemy):
  id = "Bat"
  icon = Style("b", AnsiColor.TextBlue)
  stats = BaseStats()

  def __init__(self):
    self.stats.level = 1
    self.stats.health = 10
    self.stats.power = 2
    self.stats.defense = 1

enemis:list[BaseEnemy] = [Bat]
