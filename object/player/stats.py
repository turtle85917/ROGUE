from object.types.stats import BaseStats

class Stats(BaseStats):
  curse:int
  money:int
  energy:int
  exp:int
  nextExp:int

  def __init__(self):
    self.level = 1
    self.curse = 0
    self.money = 50
    self.health = 40
    self.power = 5
    self.defense = 1
    self.energy = 10
    self.exp = 0
    self.nextExp = 50
