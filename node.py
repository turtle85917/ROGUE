from __future__ import annotations

from constants import *

class Node:
  otherNode1:Node
  otherNode2:Node
  room:BinaryRoom

  def __init__(self, width:int, height:int, top:int, left:int):
    self.width = width
    self.height = height
    self.top = top
    self.left = left

class BinaryRoom:
  right = 0
  bottom = 0

  def __init__(self, width:int, height:int, left:int, top:int):
    self.width = width
    self.height = height
    self.left = left
    self.top = top

    self.right = self.width + self.left - 1
    self.bottom = self.height + self.top - 1

  def calculateCenter(self)->tuple[int,int]:
    return (self.left + self.right) // 2, (self.top + self.bottom) // 2
