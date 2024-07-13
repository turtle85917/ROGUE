from object.base import BaseEnemy, BaseStats

class Bat(BaseEnemy):
  id = "bat"
  icon = "b"
  color = 4
  stats = BaseStats(
    level = 1,
    maxHealth = 10,
    power = 2,
    defense = 1,
    exp = 10,
    penetrate = 0
  )

class Slime(BaseEnemy):
  id = "slime"
  icon = "s"
  color = 37
  stats = BaseStats(
    level = 1,
    maxHealth = 14,
    power = 1,
    defense = 0,
    exp = 0,
    penetrate = 0
  )

enemies:list[BaseEnemy] = [Bat, Slime]
