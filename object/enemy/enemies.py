from object.base import BaseEnemy, BaseStats
from rendering.types.ansi import AnsiColor

class Bat(BaseEnemy):
  id = "Bat"
  icon = "b"
  color = AnsiColor.TextBlue
  stats = BaseStats(
    level = 1,
    health = 10,
    power = 2,
    defense = 1
  )

class Slime(BaseEnemy):
  id = "Slime"
  icon = "s"
  color = AnsiColor.TextGreen
  stats = BaseStats(
    level = 1,
    health = 5,
    power = 1,
    defense = 0
  )

enemies:list[BaseEnemy] = [Bat, Slime]
