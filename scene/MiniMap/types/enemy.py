from dataclasses import dataclass

from object.base import BaseEnemy
from object.position import Position

@dataclass
class Enemy:
  uuid:str
  health:int
  enemy:BaseEnemy
  position:Position
