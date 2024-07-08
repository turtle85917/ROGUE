from object.base import BaseEnemy, BaseStats

class Bat(BaseEnemy):
  id = "Bat"
  icon = "b"
  color = 4
  stats = BaseStats(
    level = 1,
    health = 10,
    power = 2,
    defense = 1
  )

class Slime(BaseEnemy):
  id = "Slime"
  icon = "s"
  color = 37
  stats = BaseStats(
    level = 1,
    health = 5,
    power = 1,
    defense = 0
  )

enemies:list[BaseEnemy] = [Bat, Slime]
