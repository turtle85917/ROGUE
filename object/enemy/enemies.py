from object.enemy.base import BaseEnemy, BaseStats

class Bat(BaseEnemy):
  id = "Bat"
  icon = "b"
  stats = BaseStats()

  def __init__(self):
    self.stats.level = 1
    self.stats.health = 10
    self.stats.power = 2
    self.stats.defense = 1

enemis:list[BaseEnemy] = [Bat]
