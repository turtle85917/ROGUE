from __future__ import annotations

from object.base import BaseEnemy
from object.position import Position

from scene.MiniMap.constants import *

class Node:
  otherNode1:Node
  otherNode2:Node
  parentNode:Node

  room:BinaryRoom

  isRowDivided:bool # 가로로 나뉘어져 있는가?

  def __init__(self, width:int, height:int, top:int, left:int):
    self.width = width
    self.height = height
    self.top = top
    self.left = left

class BinaryRoom:
  right = 0
  bottom = 0

  enemies:list[tuple[BaseEnemy, Position]]

  node:Node

  def __init__(self, width:int, height:int, left:int, top:int):
    self.width = width
    self.height = height
    self.left = left
    self.top = top

    self.enemies = []

    self.right = self.width + self.left - 1
    self.bottom = self.height + self.top - 1

  def repos(self, top:int, left:int):
    '''
    위치를 초기화홥니다.
    '''
    self.top = top
    self.left = left
    self.right = self.width + self.left - 1
    self.bottom = self.height + self.top - 1

  def calculateCenter(self)->tuple[int,int]:
    return (self.left + self.right) // 2, (self.top + self.bottom) // 2
