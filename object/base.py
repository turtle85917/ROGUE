from object.types.stats import BaseStats

class BaseObject():
  id: str
  icon: str

class BaseEnemy(BaseObject):
  stats:BaseStats
