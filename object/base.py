from object.types.stats import BaseStats
from rendering.types.ansi import AnsiColor

class BaseObject():
  id:str
  icon:str
  color:AnsiColor

class BaseEnemy(BaseObject):
  stats:BaseStats
