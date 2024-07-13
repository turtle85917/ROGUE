from dataclasses import dataclass

@dataclass
class BaseStats:
  level:int
  maxHealth:int
  power:int
  defense:int
  exp:int
  penetrate:int
