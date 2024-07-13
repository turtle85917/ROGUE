from rendering.types.prop import Prop
from rendering.types.cell import Cell

def prop2cell(prop:Prop):
  return Cell(prop=prop, color=0)
