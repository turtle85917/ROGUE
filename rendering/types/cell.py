from dataclasses import dataclass

from rendering.types.prop import Prop

@dataclass
class Cell():
  prop:Prop|str
  color:int
  isText:bool = False
