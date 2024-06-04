from __future__ import annotations

class Position:
  __x:int
  __y:int

  def __init__(self, x:int, y:int):
    self.__x = x
    self.__y = y

  def __add__(self, other:Position)->Position:
    '''
    두 위치를 합한 새로운 위치를 반환합니다.
    '''
    return Position(self.x + other.x, self.y + other.y)

  @property
  def x(self):
    return self.__x
  @property
  def y(self):
    return self.__y
