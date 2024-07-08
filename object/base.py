from object.types.stats import BaseStats

class BaseObject():
  id:str
  icon:str
  color:int

class BaseEnemy(BaseObject):
  stats:BaseStats
