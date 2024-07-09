from object.types.stats import BaseStats

from rendering.types.cell import Cell

class BaseObject():
  id:str
  icon:str
  color:int

  @property
  def cell(self)->Cell:
    return Cell(prop=self.icon, color=self.color)

class BaseEnemy(BaseObject):
  stats:BaseStats
